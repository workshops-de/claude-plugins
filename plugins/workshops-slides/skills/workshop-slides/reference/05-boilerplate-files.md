# Boilerplate Files

These files come from the template and typically don't need modification.
They are included here for reference so you understand the full repository.

## package.json

The only field to customize is `name`. Build tooling, the deploy workflow, core dependencies
(Slidev, Playwright, TypeScript, Vue, the tldraw and window-mockup addons) and the Prettier config
come from `@workshops.de/slidev-toolkit`; the look comes from `@workshops.de/slidev-theme`.
Do not add these dependencies to the repository directly.

```json
{
  "name": "angular-workshop-slides",
  "type": "module",
  "engines": {
    "node": ">=24",
    "npm": ">=11"
  },
  "private": true,
  "scripts": {
    "dev": "workshop-slides dev",
    "build": "workshop-slides build",
    "export": "slidev export",
    "preview": "npx vite preview --outDir dist"
  },
  "prettier": "@workshops.de/slidev-toolkit/prettier",
  "dependencies": {
    "@workshops.de/slidev-theme": "2.3.0"
  },
  "devDependencies": {
    "@workshops.de/slidev-toolkit": "^1.1.0"
  }
}
```

Commands: `npm run dev` (lesson menu, `npm run dev -- 02` for lesson 02), `npm run build`
(all lessons into `dist/` with a PDF per lesson). Use npm 11 / Node 24 (`.nvmrc`).

## .github/workflows/deploy.yml

Deploys to GitHub Pages on push to main through the toolkit's reusable workflow. It builds all
lessons, exports PDFs and makes deep links like `/01-lesson/presenter/1` work.

```yaml
name: Deploy pages

on:
  workflow_dispatch:
  push:
    branches: [main]

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  deploy:
    uses: workshops-de/slidev-toolkit/.github/workflows/deploy.yml@v1
```

## .github/dependabot.yml

```yaml
# Dependabot keeps the workshops.de packages (@workshops.de/slidev-toolkit and
# @workshops.de/slidev-theme) up to date. They are grouped into a single PR per run.
# https://docs.github.com/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      workshops-de:
        patterns:
          - "@workshops.de/*"
    commit-message:
      prefix: "chore(deps)"
```

## .nvmrc

```
v24
```

## .gitignore

```
# Dependencies
node_modules/

# Build output
dist/
.output/

# Slidev cache
.slidev/

# IDE
.idea/
*.swp
*.swo
.vscode/

# OS
.DS_Store
Thumbs.db

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Generated PDFs (optional - remove if you want to track them)
# *.pdf
```

## Adding lessons

Nothing to register: the toolkit discovers every `lessons/*/*.md` with `base:` and `out:` in its
headmatter. Do not add a `scripts/`, `setup/` or `styles/` folder.

## Platform Integration

After pushing the repo to GitHub:

1. Set `github_course_url` on the course record in the workshops.de admin
2. Enable `synced_from_github` on the course
3. Trigger sync — the platform reads:
   - `lessons/*/lesson.yml` → creates/updates Lesson records
   - `lessons/*/tasks/*/task.yml` + `body.md` + `hint.md` etc. → creates/updates CourseTask records
   - PDF from GitHub Pages → attaches to lesson record
4. Slides are served directly from GitHub Pages at `https://org.github.io/repo-name/01-lesson/`
