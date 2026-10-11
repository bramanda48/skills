---
name: github-projectflow
description: "Manage the vibe-coding workflow via GitHub: ideas=draft issues in a Project v2 board, plans=issues, tasks=sub-issues, status via the board's Status field. Session state/checkpoints are stored in uteke memory. Use when starting a plan, parking an idea, updating task status, or resuming work. Trigger: 'projectflow: ...'."
---

# Github ProjectFlow

Skill for staying focused while vibe coding with GitHub as the source of truth.
Works alongside: `uteke-memory` (state/checkpoints), `github-flow-branching` (branches & PRs), `conventional-commits` (commit messages).

All paths below (`scripts/`, `templates/`) are relative to this skill's folder.

## Entity Mapping

| Concept | GitHub representation |
| --- | --- |
| IDEAS | **Draft issue** in Project v2 (board-only item, no issue number, does not appear in repo Issues tab) |
| PLAN | Regular **issue**, body follows `templates/plan-issue.md` |
| TASK | **Sub-issue** of the plan issue, body follows `templates/sub-issue.md` |
| STATE/CHECKPOINT | **uteke memory** (type `procedure`, tags `project:<repo>` + `checkpoint`) |

### Status Mapping

Status is a **board field**, not an entity — but it is the contract every status change must follow, and the most error-prone part of the workflow:

- Board: field **Status** on Project v2
- Options (exactly these): `Todo` → `In Progress` → `Done`, plus `Blocked`
- Every board item (draft, plan, task) MUST carry one of these statuses at all times
- `Blocked` MUST come with a blocker comment on the issue

## Labels & Assignment

Every issue created by this skill (plan or sub-issue) MUST have:

1. **Auto-assignee**: the repo owner / current user → `--assignee @me`
2. **Kind label**: `plan` for plans, `task` for sub-issues
3. **Package label**: `package: <package-name>` — scope of the work
4. **Idea drafts** get no labels (drafts do not support them); prefix title with `[IDEA]`

### Resolving the package name

- Monorepo (has `packages/*` or `apps/*`): use the directory name being worked on, e.g. `package: api`, `package: web`
- Single-package repo: use the repo name, e.g. `package: myrepo`
- Work that spans the whole repo: `package: root`

### Ensure labels exist (idempotent)

```bash
# Run once per package scope before creating issues
gh label create "plan" --color 0E8A16 --description "Active plan issue" 2>/dev/null || true
gh label create "task" --color 1D76DB --description "Task sub-issue" 2>/dev/null || true
gh label create "package: api" --color FBCA04 --description "Scope: api package" 2>/dev/null || true
```

### Creating issues from templates

The templates contain `<...>` placeholders and an HTML comment. **Never pass a template to `--body-file` as-is.** Copy it to a temp file, fill it in, then use the filled copy:

```bash
cp templates/plan-issue.md /tmp/plan-body.md   # fill in, delete the HTML comment
gh issue create --title "PLAN: <title>" --assignee @me \
  --label "plan,package: api" --body-file /tmp/plan-body.md
# prints the issue URL; the number is the last path segment
```

## Core Rules

1. **One active plan.** Session focus = one plan issue with Status `In Progress`. Everything else goes to draft ideas.
2. **Park ideas, don't switch context.** When an idea pops up mid-session → create a draft issue, keep working on the active plan.
3. **Auto-checkpoint (MANDATORY).** Every sub-issue status change → (a) update Status on the board, (b) store a checkpoint in uteke. Protection against network errors / out-of-tokens / session crashes.
4. **One branch per plan** per `github-flow-branching`: descriptive branch off the default branch, push regularly, open PR, merge, delete branch. **Never commit directly to the default branch.**
5. **Commits follow `conventional-commits`** with a `Refs #<sub-issue-number>` footer for automatic linking.
6. **Plan done** → all sub-issues `Done`, plan issue closed (`gh issue close`), PR merged per github-flow.

## Setup & Detection (3 Python scripts, stdlib only)

Never assume user-level or org-level — scripts detect it via `gh repo view --json isInOrganization`. The `gh` token needs the `project` scope (`gh auth refresh -s project`); the scripts check this.

### Setup flow

Run `scripts/detect-board.py` first, then follow the case that matches:

1. **No board and no `.github/projectflow.json`** → `detect-board.py` finds no board → ask the user for the board name → `create-board.py --title "<name>"` → `create-status.py`.
2. **Board exists and `.github/projectflow.json` exists** → `detect-board.py` confirms the board → done, nothing to create.
3. **`.github/projectflow.json` exists but the board is gone or no longer linked to this repo** (`detect-board.py` warns about it) → delete the current `.github/projectflow.json` and run the setup again as in case 1.

### 1. `scripts/detect-board.py` — detect repo & boards

```bash
python3 scripts/detect-board.py
```

JSON output: `owner`, `repo`, `is_org`, `config` (contents of `.github/projectflow.json` if present — this is the **canonical board** for this repo), and a list of `projects` — only the boards **linked to this repo** (number, title, shortDescription, url).

### 2. `scripts/create-board.py` — create/set up the board

```bash
python3 scripts/create-board.py --title "My Board"   # always creates a new board
python3 scripts/create-board.py --number 3           # use an existing board
```

**There is no default board name.** During `projectflow: setup`, always ask the user what the board should be called (or whether to use an existing one) before running this script. `--title` is required unless `--number` is given.

Does: create a new Project v2 (no check for existing boards with the same name) → set **short description** + **board README** → link the repo → ensure the Status field is complete (existing options are preserved) → write `.github/projectflow.json` (`owner` + `project_number`) to the repo (creating `.github/` if needed), marking this board as canonical.

Known limitation: views cannot be created through the GitHub API. If a kanban view grouped by Status is wanted, add it once in the GitHub UI. The board title is intentionally not stored — it can be renamed freely.

### 3. `scripts/create-status.py` — verify the status mapping

```bash
python3 scripts/create-status.py              # board number taken from .github/projectflow.json
python3 scripts/create-status.py --number 3   # manual override
python3 scripts/create-status.py --fix         # auto-fix
```

Ensures the `Status` field has these options: `Todo`, `In Progress`, `Done`, `Blocked`. `--fix` adds missing options and keeps existing ones.

## Setting Status on a board item

Resolve IDs fresh each session (never hardcode):

```bash
N=<project-number>; OWNER=<owner>
PROJECT_ID=$(gh project view $N --owner $OWNER --format json --jq .id)
gh project field-list $N --owner $OWNER --format json   # find Status field id + option ids
gh project item-list $N --owner $OWNER --format json    # find the item id
gh project item-edit --id <item-id> --project-id $PROJECT_ID \
  --field-id <status-field-id> --single-select-option-id <option-id>
```

`gh project item-add ... --format json` also returns the new item's `id`.

## Daily SOP

### Resuming work (start of session)

1. `uteke_recall` with query "checkpoint", tags `["project:<repo>"]` → get active plan, branch, next step.
2. Quick verify: `gh issue view <plan-number>` + the plan's sub-issues → sync actual state.

### Parking an idea

```bash
gh project item-create <number> --owner <owner> --title "[IDEA] <title>" --body "<details>"
```

Then set Status = `Todo` (see "Setting Status on a board item").

### Converting an idea into a plan (+ task breakdown)

1. Read the draft item (`gh project item-list <number> --owner <owner> --format json`), extract title/body and the item id.
2. Create the plan issue from a filled copy of `templates/plan-issue.md`:

   ```bash
   gh issue create --title "PLAN: <title>" --assignee @me \
     --label "plan,package: <name>" --body-file /tmp/plan-body.md
   ```

3. Add it to the board: `gh project item-add <number> --owner <owner> --url <issue-url> --format json`, then set Status = `In Progress`.
4. Break the plan into sub-issues — one per task, from a filled copy of `templates/sub-issue.md`:

   ```bash
   gh issue create --title "<task>" --assignee @me \
     --label "task,package: <name>" --body-file /tmp/task-body.md
   # The sub-issues API needs the task's database id, NOT its issue number:
   TASK_ID=$(gh api repos/<owner>/<repo>/issues/<task-number> --jq .id)
   gh api -X POST repos/<owner>/<repo>/issues/<plan-number>/sub_issues -F sub_issue_id=$TASK_ID
   ```

   Add each task to the board with Status = `Todo`. (Fallback if the sub-issues endpoint fails: task-list checkboxes in the plan issue body.)

5. Remove the original draft item: `gh project item-delete <number> --owner <owner> --id <draft-item-id>`.
6. Create a branch off the default branch (github-flow skill): `git checkout -b <plan-slug>`.
7. `uteke_remember` the initial checkpoint (active plan, issue number, branch, next step).

### Starting a plan from scratch (no prior idea)

Same as above, skip steps 1 and 5.

### Daily work loop

1. Pick a sub-issue with Status `Todo` → set Status = `In Progress`.
2. Implement → conventional commit with `Refs #<sub-issue>` footer, push.
3. Sub-issue done → set Status = `Done` → **AUTO-CHECKPOINT**:
   - `uteke_remember`: type `procedure`, tags `["project:<repo>", "checkpoint"]`, content: active plan, branch, last commit, next step, gotchas.
   - Supersede the previous checkpoint for the same plan with `uteke_supersede` (never leave two active checkpoints).
4. Blocked → Status = `Blocked` + `gh issue comment <n> --body "Blocker: ..."` (a Blocked item MUST carry a blocker comment).

### Wrapping up a plan

All sub-issues `Done` → `gh issue close <plan>` → merge the PR (github-flow) → supersede the uteke checkpoint → store important decisions in uteke (type `decision`, tag `project:<repo>`).

## Trigger Phrases

| User says | Action |
| --- | --- |
| `projectflow: status` | `uteke_recall` checkpoint → summarize + verify with `gh` |
| `projectflow: park idea <X>` | Draft issue `[IDEA] X` |
| `projectflow: start plan <X>` | Plan issue + sub-issues + branch (with `package:` label, assignee @me) |
| `projectflow: convert idea <X>` | Draft → plan issue + task breakdown |
| `projectflow: checkpoint` | Manual `uteke_remember` checkpoint (auto-checkpoint still runs) |
| `projectflow: archive` | Close plan, wrap up uteke |
| `projectflow: setup` | Run `scripts/detect-board.py` → `create-board.py` → `create-status.py` |

## Technical Notes

- GraphQL IDs (project, Status field, options) **must be resolved fresh** each session via `gh project field-list/item-list --format json` or GraphQL — never hardcode them.
- `.github/projectflow.json` is the source of truth for the canonical board. Written by `create-board.py`, read by `detect-board.py` and `create-status.py`. A repo may link to several boards — always resolve the canonical one from this file first.
- Draft issues cannot be commented on or labeled — if an idea needs discussion, convert it to a regular issue first.
- Every `gh project ...` command needs the `--owner <owner>` flag.
- `gh label create ... 2>/dev/null || true` is the idempotent pattern — safe to re-run.
