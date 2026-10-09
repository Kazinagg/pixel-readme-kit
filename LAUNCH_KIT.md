# 🚀 PIXEL README KIT — LAUNCH & PROMOTION KIT (v5.0)

Этот документ содержит готовые тексты и сценарии анонсов для запуска проекта на ключевых площадках разработчиков: **Hacker News**, **Reddit**, **Product Hunt** и **Twitter / X**.

---

## 1. Show HN (Hacker News)

**Target**: [news.ycombinator.com/show](https://news.ycombinator.com/show)  
**Title**:  
`Show HN: Pixel Readme Kit – Zero-dependency SVG design system & HUD studio for GitHub`

**Body**:
```markdown
Hey HN,

I built Pixel Readme Kit (https://github.com/Kazinagg/readme-kit) because I was tired of two things with GitHub README widgets and profile cards:
1. They almost always depend on third-party serverless endpoints (Vercel, Heroku) that frequently hit GitHub API rate limits, throw 504 gateway timeouts, or break when you visit the repo.
2. Most badges and cards look disjointed and template-generic.

Pixel Readme Kit is a complete design system and local visual studio that generates autonomous, standalone SVG assets directly inside your repository.

Key features:
- Zero external runtime dependencies: Written in pure Python standard library (no headless Chrome, Cairo, or Pillow). Renders vector SVGs in < 50ms.
- Tri-Paradigm Design: Supports retro-tech / cyberpunk HUD (radar, scanlines), modern clean vector (matte graphite, 1px borders), and corporate/academic blue.
- Adaptive Theming: SVGs adapt to GitHub dark/light mode using native SVG CSS `@media (prefers-color-scheme)`.
- Interactive Local Studio: Run `pipx run readme-kit studio --open` for an SSE live-reloading visual block builder.
- Star Growth & Profile Dossiers: Dynamic star growth curves and profile dossiers with auto-fetching via GitHub API.
- Reusable GitHub Action: A single scheduled cron workflow to auto-update stars and KPI metrics daily without server maintenance.
- AI Agent Native: Built-in Model Context Protocol (MCP) server for Cursor and Claude Desktop.

Try it in one line:
$ pipx run readme-kit studio --open

Repo: https://github.com/Kazinagg/readme-kit
Web Demo: https://kazinagg.github.io/readme-kit/

Feedback, aesthetic critique, and PRs are very welcome!
```

---

## 2. Reddit Posts

### Пост 1: r/Python
**Title**:  
`I built a zero-dependency SVG design system and local Web Studio for GitHub READMEs (pure standard library)`

**Body**:
```markdown
Hey everyone!

Wanted to share a project I've been working on: **Pixel Readme Kit** (https://github.com/Kazinagg/readme-kit).

### The Problem
Most dynamic GitHub README widgets (like star graphs, KPI counters, and profile banners) rely on hosted web endpoints. When those third-party servers experience downtime or hit GitHub rate limits, your repository displays broken image icons.

### The Solution: Offline Vector Generation in Standard Library
I wanted a toolkit that:
1. Has **ZERO external Python dependencies** — everything uses `urllib`, `xml.etree`, and vector math in `math`.
2. Generates standalone SVGs with adaptive `@media (prefers-color-scheme)` dark/light CSS.
3. Includes an interactive visual editor with Server-Sent Events (SSE) live reload.
4. Can run in CI/CD (GitHub Actions) to update stats on a daily cron schedule.

### How to test:
```bash
pipx run readme-kit studio --open
```

It opens a local web UI where you can tweak palettes (with WCAG contrast calculation), configure widgets (headers, timelines, developer dossier cards, star trend curves), and copy the resulting Markdown.

GitHub: https://github.com/Kazinagg/readme-kit

Would love to hear your thoughts on the code and architecture!
```

---

### Пост 2: r/github & r/webdev
**Title**:  
`Tired of broken README widgets? I made an autonomous SVG design system & browser studio for GitHub profiles and repos`

**Body**:
```markdown
Hey developers!

If you've ever had your GitHub profile cards or repo badges break because an external Vercel server was down or rate-limited, you might find this useful.

I built **Pixel Readme Kit**: a complete design system for GitHub READMEs that compiles directly into static SVG assets committed to your repo.

✨ **Highlights**:
- **3 Visual Styles**: Retro/Cyberpunk HUD, Clean Slate Vector, and Corporate Blue.
- **Developer Dossier Card**: Flagship identity header with status indicator, avatar, and manifesto.
- **Star History Curve**: Beautiful area-gradient star trajectory chart.
- **Auto-Sync via GitHub Action**: Schedule a daily cron job that updates stars and metrics with automatic GitHub Camo cache-busting.
- **Visual Studio**: Local WYSIWYG studio with instant preview.

One-command run:
`pipx run readme-kit studio --open`

GitHub: https://github.com/Kazinagg/readme-kit
Live showcase: https://kazinagg.github.io/readme-kit/
```

---

## 3. Product Hunt Launch Card

- **Product Name**: Pixel Readme Kit
- **Tagline**: The ultimate design system & visual studio for GitHub READMEs
- **Pricing**: Free & Open Source (MIT)
- **Topics**: Developer Tools, Open Source, GitHub, Design Tools
- **First Comment by Maker**:
```markdown
Hello Product Hunt! 👋

I'm Alex, creator of Pixel Readme Kit.

Most READMEs either look plain or use random, inconsistent badges from across the web. I wanted to give developers an authentic, cohesive design language — whether they want a futuristic retro-tech terminal, a clean minimal engineering dossier, or a corporate look.

Pixel Readme Kit is 100% open source, requires 0 external dependencies, and comes with a local visual studio.

Check it out and let me know what components or styles you'd like to see next!
```

---

## 4. Twitter / X Thread

1/5 🧵 Tired of ugly badges and 3rd-party README widgets that crash during GitHub API rate limits?

I built **Pixel Readme Kit** v5.0 — a zero-dependency vector design system and interactive studio for GitHub Profiles & Repositories! ⚡

2/5 🎨 **3 Visual Paradigms in 1 Toolkit**:
- 👾 Retro-Tech / Cyberpunk HUD (360° radar, scanlines)
- 🔲 Clean Modern Vector (1px slate borders, smooth geometry)
- 💼 Corporate & Academic (Deep navy, minimal typography)

3/5 🖥️ **Interactive Web Studio**:
Change colors, live-preview cards, and test GitHub dark/light mode with SSE live reload:
`pipx run readme-kit studio --open`

4/5 📈 **Auto-Updating Star Charts**:
Generate beautiful area-fill star trajectories and profile dossiers. Set up a 10-second GitHub Action cron to keep stats fresh daily!

5/5 🌟 100% Open Source under MIT.
Star the project on GitHub: https://github.com/Kazinagg/readme-kit
RTs appreciated! ❤️
