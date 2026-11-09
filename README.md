# workshops.de Claude Code plugins

Claude Code plugin marketplace for creating and maintaining workshops.de trainings.

## Plugins

### `workshops-courses`: for every training repository

Lessons and tasks in `lessons/`, whether the slides are in Slidev or Google Slides
(e.g. `angular-workshop-slides`, `workshop-claude-code` and all Slidev slide repositories).

| Skill               | Use it to …                                                          |
| ------------------- | -------------------------------------------------------------------- |
| `course-content`    | follow the lesson and task conventions (lesson.yml, task.yml, …)     |
| `translate-task-de` | translate tasks into German (`*.de.md`), or update stale ones        |
| `git-conventions`   | write Conventional Commits and branch names                          |

### `workshops-slidev`: additionally for Slidev slide repositories

Repositories created from [`workshop-slides-template`](https://github.com/workshops-de/workshop-slides-template)
and single-deck Slidev repositories. Depends on `workshops-courses`.

| Skill                      | Use it to …                                                       |
| -------------------------- | ----------------------------------------------------------------- |
| `slidev-authoring`         | follow the slide conventions (4-MAT, layouts, code blocks)        |
| `lesson-section-interview` | define one lesson section in an interview with the trainer       |
| `lesson-migration`         | migrate raw Slidev slides into a 4-MAT lesson                    |
| `lesson-review`            | review a lesson for duplicates, tone, examples and slide quality |

Skills load automatically when they fit the task, or explicitly with `/<plugin>:<skill>`, e.g.
`/workshops-courses:translate-task-de` or `/workshops-slidev:lesson-review`.

## Usage

Every training repository enables the plugins in its committed `.claude/settings.json`. Slidev
repositories enable both, Google Slides workshops only `workshops-courses`:

```json
{
  "extraKnownMarketplaces": {
    "workshops-de": {
      "source": { "source": "github", "repo": "workshops-de/claude-plugins" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "workshops-courses@workshops-de": true,
    "workshops-slidev@workshops-de": true
  }
}
```

Clone the repository, start Claude Code in it (terminal, desktop app or IDE) and trust the folder
when asked. The plugins are then available and update automatically.

Outside a training repository, add them yourself:

```
/plugin marketplace add workshops-de/claude-plugins
/plugin install workshops-courses@workshops-de
/plugin install workshops-slidev@workshops-de
```

**Cloud sessions** (claude.ai/code) do not load plugins from a repository's `.claude/settings.json`.

## Cursor

Cursor reads `.cursor/rules/*.mdc`, not Claude Code plugins. Generate the Cursor rules from the skills
so both tools follow the same conventions:

```bash
node scripts/export-cursor-rules.mjs ../ki-software-engineer-slides ../spring-boot-slides
```

Lesson repositories get `slidev-rules.mdc` and `course-content-rules.mdc`, single-deck repositories
`slidev-rules.mdc`. Run it after changing `slidev-authoring` or `course-content` and commit the result
in each slide repository.

## Updating

Change files under `plugins/` and push to `main`. There is no version field: every commit is a new
version, and repositories with `autoUpdate` pick it up automatically.
