# RNA MINT Website

**Live site:** [rnamint.com](https://rnamint.com)  
**GitHub repo:** [github.com/ZKis-ZK/RNAmint](https://github.com/ZKis-ZK/RNAmint)  
**Hosted via:** GitHub Pages (auto-deploys on every push to `main`)

---

## How updates work

```
Edit files locally  →  git commit  →  git push  →  GitHub Pages deploys  →  rnamint.com live
```

Changes only go live when pushed. GitHub Pages usually deploys within 1–2 minutes of a push, but it can occasionally take 15–20 minutes.  
After deploying, do a hard refresh in your browser: **Cmd + Shift + R** (Mac).

Before every commit, a Git hook runs `.githooks/update_docs.py`. It refreshes the **Site summary** section at the end of this README and sets the `<lastmod>` date in `sitemap.xml` for any page being committed, so neither needs updating by hand. When `styles.css` is committed, it also updates the version number on each page's stylesheet link (`styles.css?v=` plus a short fingerprint of the file), so visitors' browsers fetch the new styles straight away instead of using a saved copy.  
On a new computer, switch the hook on once with:
```bash
git config core.hooksPath .githooks
```

---

## Folder structure

```
RNAmint/
│
├── index.html              ← Home page            (rnamint.com/)
├── research/index.html     ← Research page        (rnamint.com/research/)
├── team/index.html         ← Team page            (rnamint.com/team/)
├── contact/index.html      ← Contact page         (rnamint.com/contact/)
├── zoltan/index.html       ← Virtual business card (rnamint.com/zoltan/) — not in the sitemap or menus
├── 404.html                ← "Page not found" page shown for mistyped addresses
│
├── research.html           ← Redirect stub: rnamint.com/research.html → /research/
├── team.html               ← Redirect stub: rnamint.com/team.html     → /team/
├── contact.html            ← Redirect stub: rnamint.com/contact.html  → /contact/
│   (These tiny files exist only to forward old links. Do not delete them.)
│
├── styles.css              ← Global stylesheet (used by all pages)
├── favicon.svg             ← Browser tab icon
├── apple-touch-icon.png    ← 180×180 icon used when the site is saved to an iPhone/iPad home screen
├── robots.txt              ← Tells search engines which pages to index
├── sitemap.xml             ← List of pages submitted to Google (dates updated automatically)
├── CNAME                   ← Custom domain config for GitHub Pages (rnamint.com)
├── _config.yml             ← Tells GitHub Pages not to publish this README
├── .githooks/              ← Pre-commit hook that updates this README and the sitemap
│
├── images/                 ← All active images used by the live site
│   ├── [name].webp         ← Team photos (web-optimised WebP format)
│   ├── RNA_Mint_Logo_8.webp← Logo used in the header
│   ├── RNA_Mint_Logo_9.webp← Logo used in the footer
│   ├── rnamint-social.jpg  ← 1200×630 preview image for LinkedIn/X/WhatsApp link previews
│   ├── 1.webp … 3D9A*.webp ← Lab/group photos (home page gallery), max 1600 px wide
│   ├── awards/             ← Award ceremony photos
│   ├── funders/            ← Funder logos (research page)
│   ├── rnamint_fresh_ideas.gif  ← Animated badge (for PowerPoint use)
│   └── kis_keep_it_simple.gif   ← Animated badge (for PowerPoint use)
│
│   Local only — kept on this computer, NOT pushed to GitHub (see .gitignore):
├── _archive/               ← Old/superseded pages and styles
├── _tools/                 ← Maintenance scripts, logo source files, email signature
├── images/_archive/        ← Original high-resolution photos, old logos, former members' photos
└── tmp/                    ← Draft pages
```

The local-only folders are not backed up by GitHub. Keep them in your Google Drive / Time Machine backup.

---

## Common update tasks

### Update a team member's photo
1. Add the new photo to `images/` as a `.webp` file (same filename as the existing one), ideally no more than about 800 px wide
2. Keep the high-resolution original in `images/_archive/photos_original/`
3. In `team/index.html`, update the `width` and `height` attributes on that person's `<img>` to the new photo's pixel size (this stops the page jumping while photos load)
4. Commit and push

### Add a new team member
1. Add their photo to `images/` as `Firstname Lastname.webp`
2. Edit `team/index.html` — copy an existing person card and update the details, including the `width`/`height` of the photo
3. Commit and push

### When someone leaves
1. Remove their card from the current team section of `team/index.html`
2. Add them to the alumni timeline **and** the "View full alumni list" (dates as `Mon YYYY`, e.g. `Sep 2022`)
3. Move their photo from `images/` to `images/_archive/photos_original/`

### Add a new grant (research page)
A grant must be added in **two places** in `research/index.html`:
1. **Timeline** — copy a `<div class="tl-row">` block. Set `data-start="YYYY-MM"` and `data-end="YYYY-MM"`. The `title` attribute is read as `Short title — Funder — Role — Amount — Dates` (separated by ` — `); `data-link` adds a "Further info" link to the popup.
2. **Table** — copy a `<tr data-start="YYYY-MM-DD" data-end="YYYY-MM-DD">` row into **Current grants**, with the exact start and end dates.

Everything else is automatic:
- When a grant's end date passes, the page moves it from Current to Previous grants for visitors.
- The **Active grants** counter counts the timeline bars that have not yet ended.
- The **Site summary** below warns if the timeline and tables disagree, or if ended grants are still under Current grants in the HTML.

The other counters (research funding, researchers, publications) are set by hand: edit `data-target` on the `stat-num` elements at the top of `research/index.html`.

### Add a new funder logo
1. Add the `.webp` logo to `images/funders/`
2. Add an `<img>` tag in the "We are grateful to our funders" section of `research/index.html`
3. Commit and push

### Regenerate the animated badge GIFs (for PowerPoint)
```bash
cd /Users/zoltan/RNAmint
python3 _tools/capture_badge_gifs.py
```
Output: `images/rnamint_fresh_ideas.gif` and `images/kis_keep_it_simple.gif`

---

## Style conventions

- UK spelling (modelling, optimisation, programme)
- `Prof` and `Dr` without full stops (University of Sheffield style)
- Dates in lists and timelines: three-letter months, e.g. `Sep 2022 – May 2026`
- Lower case for descriptions and headings unless a proper noun requires capitals (e.g. "MSc research students")
- "post-doctoral" (with hyphen); "Ltd" without a full stop

---

## Git workflow (quick reference)

```bash
# See what has changed
git status
git diff

# Stage and commit changes (the hook updates README + sitemap automatically)
git add filename.html
git commit -m "Brief description of what changed"

# Push live
git push origin main
```

All changes in this repo are managed via Claude Code (AI assistant).  
Commit history is at: [github.com/ZKis-ZK/RNAmint/commits/main](https://github.com/ZKis-ZK/RNAmint/commits/main)

---

## Backups

| Location | What it contains |
|---|---|
| This folder (`/Users/zoltan/RNAmint`) | Full project, including local-only archives, and complete git history |
| GitHub (`github.com/ZKis-ZK/RNAmint`) | Off-site backup of the live site files, auto-updated on push |
| Google Drive / Time Machine | Manual/periodic backup of this folder — the only backup of the local-only archives |

**To restore on a new machine:**
```bash
git clone https://github.com/ZKis-ZK/RNAmint.git
git config core.hooksPath .githooks
```

---

## Technical notes

- All pages use **Plus Jakarta Sans** (Google Fonts) and a shared `styles.css`
- Images are served as **WebP** for fast loading; team photos load lazily as visitors scroll
- The site has **JSON-LD structured data** on all main pages for Google search enrichment
- The funding timeline on the research page is a custom SVG-free Gantt chart built in vanilla JS
- `_`-prefixed folders are never published by GitHub Pages/Jekyll; `_config.yml` also excludes this README

---

## Site summary

<!-- AUTO:START (generated by .githooks/update_docs.py — do not edit by hand) -->

_Last generated: 2026-10-28_

### Pages

| Page | File | Last changed | In sitemap |
|---|---|---|---|
| https://rnamint.com/ | `index.html` | 2026-10-21 | yes |
| https://rnamint.com/research/ | `research/index.html` | 2026-10-28 | yes |
| https://rnamint.com/team/ | `team/index.html` | 2026-10-21 | yes |
| https://rnamint.com/contact/ | `contact/index.html` | 2026-10-21 | yes |
| https://rnamint.com/zoltan/ | `zoltan/index.html` | 2026-10-21 | no |
| https://rnamint.com/404.html | `404.html` | 2026-10-21 | no |

### Current grants (8) — as shown to visitors today

| Ends | Funder | Title |
|---|---|---|
| 2027-03-31 | Biotechnology and Biological Sciences Research Council (BBSRC) | Electrospun mucoadhesive matrices for polymersome-mediated mRNA vaccine delivery |
| 2027-06-30 | Royal Academy of Engineering | RNA Forge Ltd |
| 2027-07-03 | The Scientific and Technological Research Council of Türkiye (TÜBİTAK) | Development of a Circular RNA Vaccine Against Avian Influenza A (H5N1): Experimental De… |
| 2027-09-30 | Coalition for Epidemic Preparedness Innovations (CEPI) | RNAbox™: An automated continuous closed RNA platform process-in-a-box for rapid outbrea… |
| 2027-09-30 | Engineering and Physical Sciences Research Council (EPSRC) | Quantification of double-stranded mRNA impurities using microfluidics modulation spectr… |
| 2027-09-30 | Biotechnology and Biological Sciences Research Council (BBSRC) | Synthetic Biology-Based Polymerase and Promoter Engineering for Production of Next-Gene… |
| 2028-11-01 | UK Department of Health and Social Care & Engineering and Physical Sciences Research Council (EPSRC) | UK–South-East Asia Vaccine Manufacturing Research Hub |
| 2029-06-30 | Innovate UK | RNAbox™: Automated and digitalised RNA process-in-a-box for rapid outbreak-response dis… |

### Current team on the team page (14)

- Professor Zoltán Kis — Team Leader
- Dr Mabrouka Maamra — Project and Laboratory Manager
- Dr Caroline Evans — Senior Research Fellow
- Dr Adithya Nair — Research Associate
- Dr Manoj Pohare — Research Associate
- Dr Emma Welbourne — Academic Visitor
- Dr Prerna Bora — Research Associate
- Dr Stuart Archer — Senior Research Technician
- Dr Bojan Kopilovic — Research Associate
- Dr Pramuditha Mendis — Research Associate
- Dr Muhammet Ali Uygut — Visiting Researcher
- Shady Hamed — PhD Researcher
- Haitem Elmassoudi — PhD Researcher
- Joas Sterk — PhD Researcher

<!-- AUTO:END -->
