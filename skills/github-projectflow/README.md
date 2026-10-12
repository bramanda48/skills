# github-projectflow

Skill for managing the vibe-coding workflow with GitHub as the source of truth.

## Mapping

- **IDEAS** → draft issues in a GitHub Project v2 board (invisible in the repo Issues tab)
- **PLAN** → issue (labels: `plan`, `package: <name>`, assignee: @me)
- **TASK** → sub-issue (labels: `task`, `package: <name>`, assignee: @me)
- **STATUS** → board Status field: Todo / In Progress / Need Review / Done
- **STATE/CHECKPOINT** → uteke memory (skill `uteke-memory`)
- **CANONICAL BOARD** → `.github/projectflow.json` in the repo (written by `create-board.py`, read by the other scripts)
- **Branches & PRs** → skill `github-flow-branching`; commits → `conventional-commits`

## Install

1. Copy this folder (`SKILL.md`, `scripts/`, `templates/`) into your agent's skills folder.
2. Make sure `gh` has the project scope: `gh auth refresh -s project`
3. From the repo root, run the 3 Python scripts (stdlib only, no pip install):

   ```bash
   python3 scripts/detect-board.py    # detect repo (user/org) & existing boards
   python3 scripts/create-board.py --title "<name>" --description "<about the project>"   # create board + description + README + link repo
   python3 scripts/create-status.py          # verify the Status field (board number from .github/projectflow.json)
   ```

4. If anything is missing: `python3 scripts/create-status.py --number <N> --fix`

## Daily usage (inside the agent session)

```
projectflow: setup                    # detect → create → status
projectflow: status                   # resume from where you left off
projectflow: park idea dark mode      # save an idea, stay focused
projectflow: start plan export-csv    # issue + sub-issues + branch
projectflow: convert idea dark mode   # draft → plan + task breakdown
projectflow: checkpoint               # manual checkpoint
```

## Required companion skills

- `uteke-memory` — REQUIRED, for checkpoints
- `github-flow-branching` — REQUIRED, for branches/PRs
- `conventional-commits` — REQUIRED, for commit messages
