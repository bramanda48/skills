---

name: github-flow-branching
description: "GitHub Flow branching strategy (original, Scott Chacon/GitHub). Complete guidelines for coding agents when creating branches, commits, Pull Requests, and merges in a GitHub repo. Trigger: user asks to build a feature or fix, refactor, commit, open a PR, merge, or mentions branching strategy, github flow, feature branch, continuous deployment, main or master branch."
license: MIT
tags:

- git
- github-flow
- branching-strategy
- github
- workflow

---

# GitHub Flow Branching Strategy

This skill defines the branching rules that MUST be followed when making code changes in a GitHub repository. GitHub Flow is intentionally minimal and follows the original rules as published by GitHub (Scott Chacon):

1. **Anything in the `main` branch is deployable.**
2. **To work on something new, create a descriptively named branch off of `main`** (e.g. `new-oauth2-scopes`, `fix-login-redirect`).
3. **Commit to that branch locally, and regularly push your work** to the same-named branch on the server.
4. **When you need feedback, help, or think the branch is ready for merging, open a Pull Request.**
5. **After the PR has been reviewed and signed off on, merge it into `main`.**
6. **Once it is merged and pushed to `main`, deploy immediately.**

> **Default branch:** the rules above say `main`, but the default branch may be `main` **or** `master` depending on the repo. Throughout this skill, "the default branch" means whichever of the two the repo actually uses — always detect it first (see below) and use its real name in every command.

## Branch Structure

| Branch | Role | Rules |
| --- | --- | --- |
| `main` (or `master`) | Default branch; source of truth; anything in it is deployable | **Never commit directly.** Only receives merges via Pull Request. |
| topic branch (any name) | Where all work happens | Short-lived. Created from latest default branch. Deleted after merge. |

## Default Branch (`main` or `master`)

GitHub Flow has exactly one long-lived branch: the repo's **default branch**, named either `main` or `master`. Never assume — detect it first:

```bash
# Most reliable: ask the remote which branch HEAD points to
git remote show origin | grep 'HEAD branch'
# Fallback: check which one exists locally
git branch --list main master
```

Use the detected name everywhere this skill says `main` (checkout, pull, rebase target, PR base, merge target, deploy source). Do not rename the default branch on your own initiative.

That is the entire structure. GitHub Flow has **no** long-lived `develop`, `staging`, or `release` branches, and **no** special branch categories (no `feature/*`, `hotfix/*`, etc.). Deployment happens directly from `main` (via CI/CD). If the user explicitly asks for environment or categorized branches, that is GitLab Flow or Git Flow — confirm before deviating.

## Branch Naming

- Use a **short, descriptive name** that says what the work is about: `new-oauth2-scopes`, `fix-login-redirect`, `dark-mode`.
- Optionally prefix with the issue number to make tracking easy: `123-fix-login-redirect`, `42-dark-mode`.
- Lowercase, hyphen-separated. No type prefixes, no slashes required.
- A branch is a throwaway artifact — its name just needs to be clear to humans in the PR list.

## Workflow SOP (MANDATORY)

### 1. Sync before starting

First detect the default branch (see "Default Branch" above), then sync it:

```bash
git checkout main      # or: git checkout master
git pull origin main   # or: git pull origin master
```

Do NOT disturb the user's uncommitted changes. If the working tree is dirty, ask the user before stashing or committing anything.

### 2. Create a descriptively named branch off the default branch

```bash
git checkout -b fix-login-redirect
```

### 3. Commit locally and push regularly

Commit early and often to your branch, and push to the same-named remote branch regularly so the work is backed up and visible:

```bash
git push -u origin fix-login-redirect
```

Commit message style (GitHub Flow does not prescribe one; this repo uses Conventional Commits as an optional convention):

```javascript
<type>(<scope>): <short imperative description, max 72 chars>

feat(auth): add OAuth2 login with Google
fix(cart): correct total calculation for discounted items
```

- One commit = one logical change. Never commit unrelated files.
- Never use `--no-verify` or skip hooks (pre-commit, lint-staged).

### 4. Sync with the default branch before opening the PR

```bash
git fetch origin
git rebase origin/main        # or: git merge origin/main (use `master` if that is the default)
```

Use rebase for a clean history on personal, not-yet-shared branches. **Never rebase a branch that has been pushed and shared with others.**

### 5. Open a Pull Request to the default branch (`main` or `master`)

- Open the PR as soon as you need feedback/help, or when the branch is ready for merging — do not wait until the very end.
- Body must include at minimum: what changed, how to test it, linked issues (`Closes #123`).
- Keep PRs small and focused. Large change → split into multiple PRs.

### 6. Review, merge, deploy

- Wait for green CI and someone else's sign-off (or the user's explicit approval).
- Merge strategy follows repo settings (squash or merge commit).
- **Once merged to the default branch, deploy immediately from it** — do not let undeployed changes pile up.
- **After merging: delete the branch on remote and locally.**

```bash
git push origin --delete fix-login-redirect
git branch -d fix-login-redirect
```

## Urgent Production Fixes

There is no special hotfix flow in GitHub Flow — an urgent bug goes through the exact same steps, just fast-tracked:

1. Create a descriptively named branch from latest default branch (e.g. `fix-payment-timeout`).
2. Small, focused commits → push → open PR immediately.
3. Get fast-tracked review/approval, merge to the default branch.
4. Deploy immediately. No backporting needed — everything already lives on the default branch.

## Guardrails — STRICTLY FORBIDDEN

1. ❌ Committing directly to the default branch (`main`/`master`).
2. ❌ `git push --force` to the default branch.
3. ❌ Merging your own PR without user approval (unless the user explicitly asked for auto-merge).
4. ❌ Rebasing or force-pushing a branch shared with others.
5. ❌ Committing secrets, credentials, or `.env` files — verify `.gitignore` is correct.
6. ❌ Merging a PR while CI is red.
7. ❌ Letting merged-but-undeployed changes pile up on the default branch.
8. ❌ Inventing long-lived or categorized branches (`develop`, `staging`, `feature/*`) — that is not GitHub Flow.

## Visual Summary

```javascript
main ─────────────●───────────●──────────────────▶ (always deployable, deploy on merge)
                   \         / \
new-oauth2-scopes ──●──●──●──●   \
                                  \ PR + CI + review
fix-login-redirect ────●──●────────●
```

## Completion Checklist

- [ ] Default branch detected (`main` or `master`); branch created from its latest state, descriptively named
- [ ] Work committed locally and pushed regularly to the same-named remote branch
- [ ] No unrelated files or secrets committed
- [ ] Rebased/merged on latest default branch, conflicts resolved
- [ ] PR opened to the default branch with complete body, CI green, reviewed/signed off
- [ ] Merged, deployed immediately, branch deleted