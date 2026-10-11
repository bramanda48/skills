#!/usr/bin/env python3
"""detect-board.py — Detect the GitHub repo & project boards for gh-projectflow.

JSON output:
{
  "owner": "...", "repo": "...", "is_org": false,
  "config": {"owner": "...", "project_number": 3} | null,   # contents of .github/projectflow.json, if present
  "projects": [{"number": 1, "title": "...", "shortDescription": "...", "url": "..."}]
}

Usage:
  python3 scripts/detect-board.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import require_gh, repo_info, list_projects, load_config  # noqa: E402


def main():
    require_gh()
    info = repo_info()
    projects = list_projects(info["owner"], info["is_org"])
    config = load_config()
    print(json.dumps({**info, "config": config, "projects": projects}, indent=2))
    if config and config.get("project_number") not in [p["number"] for p in projects]:
        print(f"\nWARN: .github/projectflow.json points to board #{config.get('project_number')}, "
              "which no longer exists online. Delete .github/projectflow.json and run setup again.", file=sys.stderr)
    elif not projects:
        print("\nNo project board yet. Run: python3 scripts/create-board.py", file=sys.stderr)


if __name__ == "__main__":
    main()
