---
description: Plan and iterate on a workshop curriculum without generating files
argument_description: "Workshop topic, duration, level, and any constraints"
---

# Plan Curriculum

Plan a structured workshop curriculum that can later be used with `/create-workshop`.

## Steps

1. **Gather requirements.** Ask for:
   - Workshop topic
   - Duration in days
   - Level: "Einsteiger" or "Fortgeschrittene"
   - Any specific topics that must be covered
   - Any topics to exclude

2. **Create the curriculum plan.** Present a detailed table:

   | # | Directory | Lesson Name | Topics (4-MAT each) | Tasks | Est. Time |
   |---|-----------|-------------|---------------------|-------|-----------|
   | 1 | 01-... | ... | ... | ... | ... |

3. **Include a timeline.** Map lessons to training days:
   - Day 1 morning: Lesson 1
   - Day 1 afternoon: Lesson 2
   - etc.

4. **Iterate.** Refine based on user feedback:
   - Add/remove lessons
   - Reorder topics
   - Adjust task difficulty
   - Change time estimates

5. **Finalize.** Once the user is happy, suggest running `/create-workshop` with the finalized plan.

## Rules

- Each lesson = roughly half a training day
- Each lesson has 1-3 topics, each following 4-MAT (WHY/WHAT/HOW/WHAT-IF)
- Each lesson has 1-4 tasks that build progressively
- First lesson always starts with setup/environment
- 50%+ of time should be hands-on (tasks)
- Tasks should build on each other across lessons
