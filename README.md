# workshops.de Claude Code plugins

Claude Code plugin marketplace for creating and maintaining workshops.de trainings.

## Plugins

### `workshops-slides`

For the workshops.de training repositories: the Slidev slide repositories (created from
[`workshop-slides-template`](https://github.com/workshops-de/workshop-slides-template)) and the
Google Slides workshops with tasks in `lessons/` (e.g. `angular-workshop-slides`, `workshop-claude-code`).

| Skill                       | Use it to …                                                      |
| --------------------------- | ---------------------------------------------------------------- |
| `lesson-section-interview`  | define one lesson section in an interview with the trainer      |
| `lesson-migration`          | migrate raw Slidev slides into a 4-MAT lesson                   |
| `lesson-review`             | review a lesson for duplicates, tone, examples and slide quality|
| `slidev-authoring`          | follow the slide conventions (4-MAT, layouts, code blocks)      |
| `course-content`            | follow the lesson and task conventions (lesson.yml, task.yml, …)|
| `git-conventions`           | write Conventional Commits and branch names                     |
| `translate-task-de`         | translate tasks into German (`*.de.md`), or update stale ones   |

Skills load automatically when they fit the task, or explicitly with `/workshops-slides:<skill>`.

## Usage

Every slide repository enables the plugin in its committed `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "workshops-de": {
      "source": { "source": "github", "repo": "workshops-de/claude-plugins" },
      "autoUpdate": true
    }
  },
  "enabledPlugins": {
    "workshops-slides@workshops-de": true
  }
}
```

Clone a slide repository, start Claude Code in it (terminal, desktop app or IDE) and trust the folder
when asked. The plugin is then available and updates automatically.

Outside a slide repository, add it yourself:

```
/plugin marketplace add workshops-de/claude-plugins
/plugin install workshops-slides@workshops-de
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
