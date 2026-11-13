---
name: solution-commits
description: "Plans, writes and integrates the sample solution for a workshops.de task as a solution--<topic> commit on the solution branch (rebase onto the base branch, conflict resolution, build check, tags). Use when a trainer wants to add, update, move or rename the solution of a task, or asks about solution commits, the solution branch or git_tag_completed."
---

# Solution commits

Workshops with a code repository keep one commit per task solution on a solution branch. Each commit becomes a git
tag, and `git_tag_completed` in the task's `task.yml` points to it (see the `course-content` skill).

## Configuration

Defaults below. If the repository's `CLAUDE.md` or README states other values, those win; if something is unclear
(e.g. no `.gitmodules` although mode is `submodule`), ask the trainer.

| Setting         | Default      | Description                                                                                                                   |
| --------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| solution prefix | `solution--` | commit message prefix of a commit that contains a task solution                                                               |
| solution branch | `solution`   | the branch where all task solutions live                                                                                      |
| base branch     | `main`       | the branch with the starting point for participants                                                                           |
| mode            | detect       | `submodule`: the slide repository has a git submodule with the code (see `.gitmodules`); `repository`: the code repo itself |
| build command   | detect       | from the code repository (`package.json` scripts, `ng build`, `npm run build`, `mvn verify`, `./gradlew build`, …)            |

## Preparation

- In `submodule` mode, locate the submodule via `.gitmodules`. If there is more than one, ask which to use.
- Update it before touching lessons or solutions: `git submodule update --init <submodule>` and make sure the
  solution branch is up to date with its remote.

## Locating the commit

- List all solution commits to help the trainer choose the right spot:
  `git log --oneline <solution branch> | grep "solution--"`
- You need to know which commit to update; it must start with the solution prefix.
- If no valid commit is given, ask whether a new solution commit should be created, and if so, between which commits
  of the solution branch.

## Solution commit messages

The commit message of a solution commit **is** the tag name (one tag per commit, e.g. created by
`tools/recreate-tags.sh`), and the tag is referenced by `git_tag_completed` in the task's `task.yml`. A wrong message
breaks the "What's changed" diff in the eClassroom.

- Format: `solution--<topic>[-<part>...]`, e.g. `solution--service`, `solution--router-guards-canMatch`
  - starts with `solution--` (two dashes)
  - segments separated by a single `-`, only letters and digits, camelCase allowed
  - the first segment starts with a lowercase letter
  - only the first line counts as tag name; put anything else (e.g. trailers) below an empty line
- The message must match `git_tag_completed` of the corresponding `task.yml` exactly.
- Renaming a solution commit means renaming the tag: update the `task.yml` in the same change.

## Defining the scope

Ask the trainer:

- what the participants should learn (learning outcome)
- what the solution should cover (scope)
- where the solution should be placed in the solution branch

## Implementing the solution

- Before coding, consult the framework's best-practice skill if the repository has one (e.g. `angular-developer`
  in Angular workshops) and follow the code style already used in earlier solution commits.
- Plan the solution and the code you want to write.
- Present the plan and wait for approval before you apply it.

## Integrating the solution

- After approval, write the code.
- Apply it by rebasing the solution branch onto the base branch and editing or inserting the solution commit:

```bash
git checkout solution
git rebase main --interactive
# edit or insert the solution commit
```

- Resolve merge conflicts. Explain each conflict in detail: why it occurred and how you resolved it.
- Run the build command at every changed solution commit and at the tip of the solution branch.
- A rebase rewrites the history of the already published solution branch. Publishing needs a force push and new tags.
  **Never do this without the trainer's explicit approval:**

```bash
git push --force-with-lease origin solution
tools/recreate-tags.sh --dry-run   # validates commit messages, lists moved, new and stale tags
tools/recreate-tags.sh --prune     # recreates and pushes all tags, deletes stale remote tags
```

  If the repository has no `tools/recreate-tags.sh`, list the tags that need to move and ask the trainer how they are
  published.

- Finally, switch back to the base branch: `git checkout main`
