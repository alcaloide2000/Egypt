# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

There is no build, lint, or test tooling here. The git repo pushes to the public https://github.com/alcaloide2000/Egypt (branch `main`). The project is a set of standalone HTML pages (claude.ai Artifacts) about ancient Egypt, saved locally under `artifacts/`:

- `artifacts/ancient-egypt-history-main-points.html` is **the main deliverable**: a combined Nile locator map, search bar, info cards and timeline. Nearly all work goes here.
- `artifacts/nile-valley-timeline.html` is an earlier standalone timeline. It has been replaced by the combined page and kept as-is. Don't update it unless asked.
- `artifacts/chat-transcript.md` is the history of the original cloud session that built the pages. It records every site added and every design decision. Read it before changing content conventions.

To view a page, open the HTML file in a browser.

### Syncing with the published artifact

The live version is the claude.ai artifact **"Ancient Egypt History Main Points"** at https://claude.ai/artifact/5LEkwRrpG4KFAx377J5y7k. It is also edited from a separate Claude Code cloud session, so it can get ahead of the local file.

- **Pull** with Artifact `action: "read"` on that URL, then copy the saved HTML over `artifacts/ancient-egypt-history-main-points.html`. Put a dated copy of the old file in `artifacts/backup/` first.
- **Push** with Artifact `publish`, using `url` set to that link and `file_path` set to the local file. Always pull and merge before pushing, because publishing over a newer live version would discard the cloud session's work.

The saved files begin with a publish-time wrapper (`<!doctype html><html><head>…<body>`) followed by the authored `<title>`/`<style>`. Edit the authored content, not the wrapper.

## Architecture of the main page

It is one large file (~6,200 lines): inline CSS, inline SVG and one small script at the end. External loads are limited to Google Fonts (Fraunces, Public Sans, IBM Plex Mono). Images can't be loaded, so every "picture" is a hand-drawn inline SVG illustration.

Adding a site usually means touching **four places** that must stay consistent:

1. **Map marker**: a `<g class="site-marker" transform="translate(x,y)">` inside the map `<svg viewBox="0 0 600 860">`. It has a glyph plus `<text>` label and sub-label. Pyramids get triangle/step glyphs, people and temples get other shapes. Crowded clusters (Cairo–Giza–Saqqara corridor, Theban west bank) have been hand-respaced to stop labels overlapping.
2. **Hover illustration**: a `<button class="hotspot">` plus a `<div class="tooltip" id="…Tooltip">` holding an `<svg class="illustration" viewBox="0 0 100 128">`. Both are absolutely positioned with `left`/`top` percentages equal to the marker's map coordinates (`left = x/600`, `top = y/860`; Giza `translate(240,200)` → `left: 40%; top: 23.26%`). Colour comes from `style="--accent: var(--…)"` through one shared tooltip CSS system. Don't add per-site tooltip CSS.
3. **Info card**: `<div class="info-card" id="card-<slug>">`. Sites with no known findspot (Palermo Stone, Mentuhotep I, Netjerkare Siptah) use `class="info-card unlocated"` (dashed style) and get no map pin. Cards link to Wikipedia ("Read on Wikipedia ↗"). Alternate and ancient names (e.g. Abedyu for Abydos, Khnum-Khufu/Cheops for Khufu) go on the existing card rather than in a duplicate entry.
4. **Timeline entry**: inside the timeline `<svg viewBox="0 0 2252 480">`. The axis is broken (`<g class="tl-break">` marks the gaps) into segments. Only four have labelled `<rect>` era bands with a `tl-era-label`: Predynastic, Early Dynastic & Old Kingdom, New Kingdom and Ptolemaic. The Middle Kingdom and Second Intermediate segments have no band. Single-monument entries are wrapped in `<a href="#card-<slug>" class="tl-link">` so clicking one jumps to its card (`.info-card:target` flashes gold). Composite entries stay unlinked. Conventions: reigns and construction spans are bars, buildings are solid markers, and deaths are hollow dashed markers. Entries that span too many dynasties (e.g. Tombs of the Nobles) get no timeline mark.

When the timeline changes, also update the long `<desc id="tlDesc">` prose so it stays accurate. The masthead/timeline `.lede` text should describe the whole page.

### Theming

All colours are CSS custom properties on `:root`. Each one is defined three times: light defaults, `@media (prefers-color-scheme: dark) :root:not([data-theme="light"])`, and `:root[data-theme="dark"]`. A new colour must be added in **all three blocks**; a missing `--lapis` once broke dark mode. Dark mode uses warm grey (`#302f2c` / `#3a3936`), not black. Each site family has its own accent (ochre, gold, lapis, malachite, indigo, rose, solar, turquoise, kush…).

### Search script

The `<script>` at the bottom filters `.info-card` elements by full-text match and wraps hits in `<mark class="hit">` using safe DOM text nodes (no innerHTML). It dims non-matching `.site-marker` groups and scrolls to the first match. New cards and markers are picked up automatically as long as they use those classes.

## Working conventions

- Check for overlapping text after any change to the map or timeline. Most past bugs were label collisions or labels placed at the wrong date (e.g. Thutmose III's label had drifted ~130 years off). Render the page and check bounding boxes or a screenshot.
- Historical claims should be accurate and dated "c. … BC". When a name is ambiguous (which Thutmose, which Mentuhotep, a misspelled site), clarify or confirm before adding it.
- The user writes short, often misspelled or Spanish-influenced requests (e.g. "ajetaton" = Akhenaten, "nejen" = Nekhen). Work out what they mean, and check whether the item already exists on the page before adding it.
