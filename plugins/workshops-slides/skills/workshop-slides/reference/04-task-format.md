# Task Format — Complete Reference

Tasks are hands-on exercises that participants complete during the workshop.
Each task lives in its own directory under `lessons/NN-lesson/tasks/NN-task-name/`.

## File Structure per Task

```
tasks/01-first-task/
├── task.yml             # Metadata (required)
├── body.md              # Main task description (required)
├── hint.md              # Hints for participants (recommended)
├── bonus.md             # Bonus challenges for fast learners (optional)
└── trainer_hint.md      # Notes for trainers only (optional)
```

---

## task.yml — Example 1 (Preparation Task)

```yaml
title: 'First Task - Getting Started'
position: 1
category: 'Basics'
preparation: true
estimated_time_in_minutes: 10
always_unlocked: true
git_tag_completed: solution-01-first-task
```

## task.yml — Example 2 (Regular Task)

```yaml
title: 'Second Task - Implementation'
position: 2
category: 'Implementation'
preparation: false
estimated_time_in_minutes: 20
always_unlocked: false
git_tag_completed: solution-02-second-task
```

### Field Reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | yes | Display title of the task |
| `position` | integer | yes | Order within the lesson (must match directory prefix) |
| `category` | string | yes | Grouping category (e.g., "Basics", "Components") |
| `preparation` | boolean | no | `true` only for initial setup tasks |
| `estimated_time_in_minutes` | integer | no | Expected completion time |
| `always_unlocked` | boolean | no | `true` = visible from start; `false` = trainer unlocks |
| `git_tag_completed` | string | no | Git tag pointing to the solution branch |

---

## body.md — Example

```markdown
## Overview

In this task, you will set up your development environment and get familiar with the project structure.

## Prerequisites

- Node.js 18+ installed
- Code editor (VS Code recommended)
- Git installed

## Steps

### 1. Clone the Repository

```bash
git clone https://github.com/workshops-de/example-repo.git
cd example-repo
```

### 2. Install Dependencies

```bash
npm install
```

### 3. Start the Development Server

```bash
npm run dev
```

### 4. Verify Setup

Open your browser and navigate to `http://localhost:3000`. You should see the welcome page.

## Success Criteria

- [ ] Repository cloned successfully
- [ ] All dependencies installed without errors
- [ ] Development server running
- [ ] Welcome page visible in browser

## Troubleshooting

If you encounter issues:

- Make sure you're using the correct Node.js version (check `.nvmrc`)
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check the console for error messages
```

### body.md Guidelines

1. Start with `## Overview` — brief description of what they'll do
2. List prerequisites if needed
3. Use numbered steps with code examples
4. Include realistic, functional code (not pseudocode)
5. End with `## Success Criteria` using checkboxes
6. Optionally add `## Troubleshooting` for common issues
7. Use Shiki annotations in code blocks where helpful

---

## hint.md — Example

```markdown
## Hints

<details>
<summary>💡 Hint 1: Node Version</summary>

Make sure you're using the correct Node.js version. You can use `nvm` to switch versions:

```bash
nvm use
```

</details>

<details>
<summary>💡 Hint 2: Port Already in Use</summary>

If port 3000 is already in use, you can either:

- Stop the other process using that port
- Change the port in your environment variables

</details>

<details>
<summary>💡 Hint 3: Complete Solution</summary>

```typescript
export class ExampleService {
  process(input: string): string {
    if (!input) {
      throw new Error('Input is required');
    }
    return input.toUpperCase();
  }
}
```

</details>
```

### hint.md Guidelines

1. Use `<details>/<summary>` for collapsible hints
2. Start with general hints, progress to more specific
3. Use 💡 emoji in summary titles
4. The last hint can contain the near-complete solution
5. 2-4 hints per task is typical

---

## bonus.md — Example

```markdown
## Bonus Challenges

### Challenge 1: Multiple Transformations

Extend the service to support different transformation modes:

```typescript
type TransformMode = 'uppercase' | 'lowercase' | 'capitalize';

process(input: string, mode: TransformMode = 'uppercase'): string {
  // Implement all three modes
}
```

### Challenge 2: Unit Tests

Write proper unit tests using your preferred testing framework:

```typescript
describe('ExampleService', () => {
  it('should transform to uppercase', () => {
    const service = new ExampleService();
    expect(service.process('hello')).toBe('HELLO');
  });
});
```
```

### bonus.md Guidelines

1. For fast learners who finish early
2. Extend the main task with additional challenges
3. Should be self-contained and not required for the next task
4. Can introduce more advanced concepts

---

## trainer_hint.md — Example

```markdown
## Trainer Notes

### Common Issues

- Participants on Windows may need to use PowerShell instead of bash
- The API endpoint may be slow on conference WiFi — have a local mock ready

### Discussion Points

- Ask participants about their experience with similar patterns
- Highlight the trade-offs between approach A and B

### Time Management

- If running short on time, skip Steps 3-4 and demonstrate live
- The bonus challenges can be assigned as homework
```
