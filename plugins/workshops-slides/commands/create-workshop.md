---
description: Generate a complete Slidev workshop repository with lessons, slides, and tasks
argument_description: "Workshop topic, type, duration, level, and any specific topics to cover"
---

# Create Workshop

Generate a complete Slidev workshop slide repository for workshops.de.

## Steps

1. **Read reference files first.** Before doing anything, read all files in `skills/workshop-slides/reference/` to understand the exact file formats and conventions.

2. **Gather requirements.** If the user hasn't specified all of these, ask:
   - Workshop topic (e.g., "Angular", "React", "Kubernetes")
   - Duration in days (e.g., 2, 3, 5)
   - Level: "Einsteiger" or "Fortgeschrittene"
   - Language: German (default) or English
   - Specific topics to cover (optional)
   - Code repository URL for exercises (optional)
   - Trainer email (optional, defaults to `trainer@workshops.de`)

3. **Plan the curriculum.** Create a table with lessons, topics, and tasks. Present it and wait for confirmation. Follow the planning rules from the `workshop-slides` skill.

4. **Generate all files.** Once confirmed, generate every file following the formats in the reference docs:
   - `00-index.md`
   - `slides.md`
   - `sources.md`
   - All lesson files (lesson.yml, entry .md, slides, tasks)

5. **Push to GitHub** (if ~~git hosting is connected):
   - Create a new repo from template `workshops-de/workshop-slides-template`
   - Name it: `{topic}-{type}-slides` (e.g., `angular-workshop-slides`)
   - Commit all generated files
   - Report the repo URL

6. **Report next steps:**
   - If pushed: provide the `github_course_url` to set in the admin
   - If not pushed: explain how to create the repo from template and copy files

## Output

A complete workshop repository with all lessons, slides, and tasks ready for deployment.
