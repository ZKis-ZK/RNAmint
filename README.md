# RNA MINT Website

**Live site:** [rnamint.com](https://rnamint.com)  
**GitHub repo:** [github.com/ZKis-ZK/RNAmint](https://github.com/ZKis-ZK/RNAmint)  
**Hosted via:** GitHub Pages (auto-deploys on every push to `main`)

---

## How updates work

```
Edit files locally  →  git commit  →  git push  →  GitHub Pages deploys  →  rnamint.com live
```

Changes only go live when pushed. GitHub Pages typically deploys within 1–2 minutes of a push.  
After deploying, do a hard refresh in your browser: **Cmd + Shift + R** (Mac).

---

## Folder structure

```
RNAmint/
│
├── index.html              ← Home / About page  (rnamint.com/)
│
├── research/
│   └── index.html          ← Research page      (rnamint.com/research/)
├── team/
│   └── index.html          ← Team page          (rnamint.com/team/)
├── contact/
│   └── index.html          ← Contact page       (rnamint.com/contact/)
│
├── research.html           ← Redirect stub: rnamint.com/research.html → /research/
├── team.html               ← Redirect stub: rnamint.com/team.html     → /team/
├── contact.html            ← Redirect stub: rnamint.com/contact.html  → /contact/
│   (These tiny files exist only to forward old links. Do not delete them.)
│
├── styles.css              ← Global stylesheet (used by all pages)
├── favicon.svg             ← Browser tab icon
├── robots.txt              ← Tells search engines which pages to index
├── sitemap.xml             ← List of pages submitted to Google
├── CNAME                   ← Custom domain config for GitHub Pages (rnamint.com)
│
├── images/                 ← All active images used by the live site
│   ├── [name].webp         ← Team photos (web-optimised WebP format)
│   ├── RNA_Mint_Logo_8.webp← Logo used in header and social sharing
│   ├── RNA_Mint_Logo_9.webp← Logo used in footer
│   ├── university-of-sheffield.webp
│   ├── rna-forge-logo.webp
│   ├── simulenta-logo.webp
│   ├── 1.webp … 3D9A*.webp ← Lab/group photos (home page carousel)
│   ├── awards/             ← Award ceremony photos
│   │   ├── icheme_zk_2024.webp
│   │   ├── icheme_zk_2025.webp
│   │   └── nobel_laureates.webp
│   ├── funders/            ← Funder logos (research page)
│   │   └── *.webp
│   ├── rnamint_fresh_ideas.gif  ← Animated badge (for PowerPoint use)
│   └── kis_keep_it_simple.gif   ← Animated badge (for PowerPoint use)
│
├── _archive/               ← Old/superseded files (not part of live site)
│   │   (GitHub Pages excludes _-prefixed folders from the public site)
│   ├── pages/
│   │   ├── staff.html      ← Superseded by team/index.html
│   │   └── students.html   ← Superseded by team/index.html
│   └── styles/
│       └── styles_green_backup.css
│
├── images/_archive/        ← Unused/original image files
│   ├── logos_old/          ← Old RNA MINT logo versions (PNG)
│   ├── photos_original/    ← High-resolution originals of team/lab photos
│   ├── awards_original/    ← Original award image files (JPEG/JPG)
│   ├── funders_original/   ← Original funder logo files (PNG/JPEG)
│   └── misc/               ← Miscellaneous unused images
│
└── _tools/                 ← Maintenance scripts (not part of live site)
    ├── capture_badge_gifs.py   ← Generates animated GIFs from live CSS animations
    └── make_badge_gifs.py      ← Earlier version of GIF generator
```

---

## Common update tasks

### Update a team member's photo
1. Add the new photo to `images/` as a `.webp` file (same filename as existing)
2. If converting from PNG/JPG: open Terminal and run:
   ```
   sips -s format webp images/"Name.png" --out images/"Name.webp"
   ```
3. Commit and push

### Add a new team member
1. Add their photo to `images/` as `Firstname Lastname.webp`
2. Edit `team/index.html` — copy an existing person card and update the details
3. Commit and push

### Update the research funding timeline
- Edit `research/index.html`
- Find the `<!-- Grant timeline -->` section
- Each grant is a `<div class="tl-bar ...">` with `data-start="YYYY-MM"` and `data-end="YYYY-MM"`
- Popup info (title, link) is in `data-link` and `title` attributes

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

## Git workflow (quick reference)

```bash
# See what has changed
git status
git diff

# Stage and commit changes
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
| This folder (`/Users/zoltan/RNAmint`) | Full project + complete git history |
| GitHub (`github.com/ZKis-ZK/RNAmint`) | Off-site backup, auto-updated on push |
| Google Drive / Time Machine | Manual/periodic backup of this folder |

**To restore on a new machine:**
```bash
git clone https://github.com/ZKis-ZK/RNAmint.git
```

---

## Technical notes

- All pages use **Plus Jakarta Sans** (Google Fonts) and a shared `styles.css`
- Images are served as **WebP** format for fast loading; originals kept in `images/_archive/photos_original/`
- The site has **JSON-LD structured data** on all main pages for Google search enrichment
- The funding timeline on the research page is a custom SVG-free Gantt chart built in vanilla JS
- `_archive/` and `_tools/` folders start with `_` so GitHub Pages/Jekyll excludes them from the public site
