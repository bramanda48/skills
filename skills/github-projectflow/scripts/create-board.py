#!/usr/bin/env python3
"""create-board.py — Create a Project v2 board, set its description + README,
link the repo, and ensure the Status field (Todo/In Progress/Need Review/Done) exists.

Always creates a new board; it does not check for existing boards with the same name.

Usage:
  python3 scripts/create-board.py --title "My Board" --description "What this project is about"

There is no default title or description: --title and --description are required.
The description should describe the project itself
(generate it from AGENTS.md at the repo root or from the session context).
When run in an interactive terminal without --title, the script asks for the name.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import (  # noqa: E402
    REQUIRED_STATUSES, gh, gh_json, gh_text, repo_info,
    get_project, ensure_status_field, save_config, require_gh,
)

DEFAULT_README = """## How to Use This Board

| Item | Meaning |
| --- | --- |
| Draft issue `[IDEA] ...` | A parked idea, not being worked on yet |
| Issue labeled `plan` | An active plan (at most one `In Progress`) |
| Sub-issue | A task from the plan's breakdown |
| Status | `Todo` → `In Progress` → `Need Review` (set by the agent) → `Done` (set manually by the user after merging the PR) |

SOP: `projectflow: status` at the start of a session → work → auto-checkpoint after every finished task.
"""


def create_board(owner, is_org, title):
    endpoint = f"orgs/{owner}" if is_org else f"users/{owner}"
    node_id = gh_text("api", endpoint, "--jq", ".node_id")
    q = ("mutation($o:ID!,$t:String!){ createProjectV2(input:{ownerId:$o, title:$t})"
         "{ projectV2{ id number url } } }")
    data = gh_json("api", "graphql", "-f", f"query={q}", "-f", f"o={node_id}", "-f", f"t={title}")
    return data["data"]["createProjectV2"]["projectV2"]


def set_meta(project_id, description, readme):
    q = ("mutation($p:ID!,$d:String!,$r:String!){ updateProjectV2("
         "input:{projectId:$p, shortDescription:$d, readme:$r})"
         "{ projectV2{ id shortDescription } } }")
    r = gh("api", "graphql", "-f", f"query={q}", "-f", f"p={project_id}",
           "-f", f"d={description}", "-f", f"r={readme}", check=False)
    if r.returncode != 0:
        # Fallback: set the description only
        q2 = ("mutation($p:ID!,$d:String!){ updateProjectV2("
              "input:{projectId:$p, shortDescription:$d}){ projectV2{ id } } }")
        gh("api", "graphql", "-f", f"query={q2}", "-f", f"p={project_id}", "-f", f"d={description}")
        print("NOTE: board README could not be set via API, but the description was set.",
              file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Create/set up a Project v2 board for github-projectflow")
    ap.add_argument("--title", default=None, help="Board name (required)")
    ap.add_argument("--description", default=None, help="Short project description (required)")
    args = ap.parse_args()

    if not args.title and sys.stdin.isatty():
        args.title = input("Board name: ").strip()
    if not args.title:
        ap.error("--title is required (ask the user what to name the board)")
    if not args.description:
        ap.error("--description is required: write a short description of the project "
                 "(from AGENTS.md or the session context)")

    require_gh()
    info = repo_info()
    owner, repo, is_org = info["owner"], info["repo"], info["is_org"]
    print(f"Repo: {owner}/{repo} (org={is_org})")

    created = create_board(owner, is_org, args.title)
    number = created["number"]
    print(f"New board: #{number} — {created['url']}")
    set_meta(created["id"], args.description, DEFAULT_README)
    proj, status_field = get_project(owner, number, is_org)

    # Link the repo to the board. A failure here is fatal so the real error is visible.
    gh("project", "link", str(number), "--owner", owner, "--repo", f"{owner}/{repo}")
    print(f"Repo {owner}/{repo} linked to board #{number}.")

    # Set the Status field to exactly the required options (board defaults are replaced)
    ensure_status_field(proj["id"], status_field)
    print(f"Status field OK: {', '.join(REQUIRED_STATUSES)}")

    print("\n=== SUMMARY ===")
    print(json.dumps({"owner": owner, "project_number": number,
                      "project_url": proj.get("url", "")}, indent=2))

    # Write the canonical board config to the repo (no title: it can be renamed freely)
    cfg_path = save_config({"owner": owner, "project_number": number})
    print(f"\nConfig written: {cfg_path}")
    print("Next: in the agent session run 'projectflow: start plan <name>'")


if __name__ == "__main__":
    main()
