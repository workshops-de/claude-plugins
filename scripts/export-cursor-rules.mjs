#!/usr/bin/env node
// Writes Cursor rules (.cursor/rules/*.mdc) generated from the plugins' skills into slide
// repositories, so Cursor and Claude Code follow the same conventions.
//
// Usage: node scripts/export-cursor-rules.mjs <repo-dir> [<repo-dir> ...]
//
// Lesson repositories (with a lessons/ folder) get slidev-rules.mdc and course-content-rules.mdc;
// single-deck repositories (slides.md + pages/) get slidev-rules.mdc only.
import fs from 'node:fs';
import path from 'node:path';

const pluginsDir = path.join(import.meta.dirname, '..', 'plugins');

const rules = [
  {
    file: 'slidev-rules.mdc',
    plugin: 'workshops-slidev',
    skill: 'slidev-authoring',
    frontmatter: 'description: Rules for creating slidev pages\nglobs:\nalwaysApply: true',
    lessonsOnly: false,
  },
  {
    file: 'course-content-rules.mdc',
    plugin: 'workshops-courses',
    skill: 'course-content',
    frontmatter:
      'description: Rules for creating course lessons and tasks\nglobs:\n  - "**/lessons/**"\n  - "**/tasks/**"\nalwaysApply: false',
    lessonsOnly: true,
  },
];

function skillBody(plugin, name) {
  const text = fs.readFileSync(path.join(pluginsDir, plugin, 'skills', name, 'SKILL.md'), 'utf8');
  return text.replace(/^---\n[\s\S]*?\n---\n+/, '');
}

const repos = process.argv.slice(2);
if (repos.length === 0) {
  console.error('Usage: node scripts/export-cursor-rules.mjs <repo-dir> [<repo-dir> ...]');
  process.exit(1);
}

for (const repo of repos) {
  const hasLessons = fs.existsSync(path.join(repo, 'lessons'));
  const target = path.join(repo, '.cursor', 'rules');
  fs.mkdirSync(target, { recursive: true });
  for (const rule of rules) {
    if (rule.lessonsOnly && !hasLessons) continue;
    const header = `<!-- Generated from the ${rule.skill} skill in https://github.com/workshops-de/claude-plugins. Edit it there and re-export. -->\n\n`;
    fs.writeFileSync(path.join(target, rule.file), `---\n${rule.frontmatter}\n---\n\n${header}${skillBody(rule.plugin, rule.skill)}`);
    console.log(`${repo}: ${rule.file}`);
  }
}
