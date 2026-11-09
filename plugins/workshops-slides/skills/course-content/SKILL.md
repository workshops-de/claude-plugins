---
name: course-content
description: "Rules for workshops.de course content: lesson folders under lessons/, lesson.yml, task.yml, body.md, hint.md, bonus.md and trainer_hint.md. Use when creating or editing lessons or tasks in a workshops.de slide repository."
---

## Lesson Structure

Each lesson is a folder in `/lessons/` with a numeric prefix for ordering (e.g., `01-example-lesson`).

### Required Files

```
lessons/
└── 01-example-lesson/
    ├── lesson.yml              # Lesson configuration (required)
    ├── 01-example-lesson.md    # Main Slidev presentation (required)
    ├── slides/                 # 4-MAT slide files (optional)
    │   └── topic-name/
    │       ├── why.md
    │       ├── what.md
    │       ├── how.md
    │       └── what-if.md
    └── tasks/                  # Task folders (optional)
        └── 01-first-task/
            └── ...
```

### lesson.yml Configuration

```yaml
# Required
name: Lesson Title
position: 1

# Trainer (email or slug)
trainer: trainer@workshops.de

# Code repository
github_code_url: https://github.com/org/repo
git_tag_starting: main

# Presentation type: "google_slides" or "slidev"
slides_type: slidev

# For Google Slides only
# google_slide_id: "1NmeNH96Qj9jqwrHJ4axQEH7_1ptbkZPjQlLZ4jyWWg"

# PDF sync
pdf_generation_enabled: true

# Playground options
stackblitz_enabled: true
codesandbox_enabled: false

# Status
deprecated: false
```

## Task Structure

Each task is a folder in `/lessons/{lesson}/tasks/` with a numeric prefix for ordering.

### Required Files

```
tasks/
└── 01-first-task/
    ├── task.yml            # Task configuration (required)
    ├── body.md             # Main task description (required)
    ├── hint.md             # Hints for participants (optional)
    ├── bonus.md            # Bonus challenges (optional)
    ├── trainer_hint.md     # Notes for trainers only (optional)
    └── assets/             # Images and media (optional)
        └── screenshot.png
```

### task.yml Configuration

```yaml
# Required
title: "Task Title"
position: 1

# Optional metadata
category: "Basics"
preparation: false
estimated_time_in_minutes: 15
always_unlocked: false

# Git Integration (for code diffs)
git_tag_completed: solution-01-task-name
```

**Note**: Markdown content is loaded from separate `.md` files, NOT from the YAML file.

## Markdown Content Guidelines

### body.md - Main Task Description

- Start with a brief overview of what the participant will accomplish
- List prerequisites if any
- Provide clear, numbered steps
- Include code examples with proper syntax highlighting
- End with success criteria (checklist format)
- Add troubleshooting section for common issues

### hint.md - Hints

- Use collapsible `<details>` elements for progressive hints
- Number hints from easiest to most revealing
- Don't give away the full solution

```markdown
<details>
<summary>💡 Hint 1: Brief description</summary>

Hint content here...

</details>
```

### bonus.md - Bonus Challenges

- Provide optional advanced challenges
- Should extend the main task, not replace it
- Clearly mark difficulty level

### trainer_hint.md - Trainer Notes

- Include common issues and solutions
- Add time estimates for different skill levels
- List discussion points for the group
- Note any setup requirements

## Code Examples in Tasks

### Shiki Notation Transformers

Use inline comments for syntax highlighting features:

| Notation | Description |
|----------|-------------|
| `// [!code highlight]` | Highlights a line |
| `// [!code focus]` | Focuses a line (blurs others) |
| `// [!code ++]` | Shows as added line (green) |
| `// [!code --]` | Shows as removed line (red) |
| `// [!code warning]` | Marks as warning |
| `// [!code error]` | Marks as error |

### Examples

**Line Highlighting:**
```typescript
interface User {
  id: number;        // [!code highlight]
  name: string;
  email: string;     // [!code highlight]
}
```

**Diff Highlighting:**
```typescript
function greet(name: string) {
  console.log('Hello')           // [!code --]
  console.log(`Hello, ${name}!`) // [!code ++]
}
```

**Error & Warning:**
```typescript
const config = {
  apiUrl: process.env.API_URL,  // [!code warning]
  secret: 'hardcoded-secret',   // [!code error]
};
```

### Code Example Best Practices

- Annotate each code block with the correct language
- Keep examples concise (1-15 lines preferred)
- Use comments to explain important parts
- Avoid showing irrelevant boilerplate

## Images and Assets

### Referencing Images

Store images in the task's `assets/` folder and reference them with relative paths:

```markdown
![Screenshot](./assets/screenshot.png)
```

During sync, relative paths are automatically converted to absolute GitHub Raw URLs.

### Image Guidelines

- Use descriptive filenames (e.g., `step-3-result.png` not `image1.png`)
- Optimize images for web (compress, appropriate resolution)
- Prefer PNG for screenshots, JPG for photos
- Add alt text for accessibility

## Git Integration

### Git Tags for Solutions

Use `git_tag_completed` in `task.yml` to link to the solution state:

```yaml
git_tag_completed: solution-01-first-task
```

This enables:
- Code diffs between starting point and solution
- StackBlitz playground with solution code
- Easy navigation for trainers

### Naming Convention

- Format: `solution-{position}-{task-slug}`
- Example: `solution-01-first-task`, `solution-02-add-component`

## Quality Checklist

- [ ] All required files present (`task.yml`, `body.md`)
- [ ] Task title is clear and descriptive
- [ ] Steps are numbered and easy to follow
- [ ] Code examples have correct language annotation
- [ ] Images have alt text and are optimized
- [ ] Success criteria are specific and measurable
- [ ] Hints don't give away the solution immediately
- [ ] Trainer notes cover common issues
