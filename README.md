# workshops.de Claude Code plugins

Claude Code plugin marketplace for creating and maintaining workshops.de trainings.

## Plugins

### `workshops-slides`

For the Slidev slide repositories (`*-slides`, created from
[`workshop-slides-template`](https://github.com/workshops-de/workshop-slides-template)).

| Skill                       | Use it to …                                                      |
| --------------------------- | ---------------------------------------------------------------- |
| `lesson-section-interview`  | define one lesson section in an interview with the trainer      |
| `lesson-migration`          | migrate raw Slidev slides into a 4-MAT lesson                   |
| `lesson-review`             | review a lesson for duplicates, tone, examples and slide quality|
| `slidev-authoring`          | follow the slide conventions (4-MAT, layouts, code blocks)      |
| `course-content`            | follow the lesson and task conventions (lesson.yml, task.yml, …)|
| `git-conventions`           | write Conventional Commits and branch names                     |

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

## Updating

Change files under `plugins/` and push to `main`. There is no version field: every commit is a new
version, and repositories with `autoUpdate` pick it up automatically.
