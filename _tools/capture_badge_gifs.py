"""
Captures the actual CSS-animated badges from the local HTML pages
using a headless Chromium browser (Playwright), then assembles GIFs.

Outputs:
  images/rnamint_fresh_ideas.gif
  images/kis_keep_it_simple.gif
"""

import asyncio, os, math
from pathlib import Path
from PIL import Image
from playwright.async_api import async_playwright

ROOT = Path(__file__).parent
OUT  = ROOT / 'images'

# ── helpers ──────────────────────────────────────────────────────────

async def capture_frames(page, selector, n_frames, interval_ms, scale=2):
    """Screenshot the bounding box of `selector` n_frames times."""
    frames = []
    elem = page.locator(selector)
    for i in range(n_frames):
        png = await elem.screenshot(type='png', scale='device')
        from io import BytesIO
        img = Image.open(BytesIO(png)).convert('RGBA')
        frames.append(img)
        if i < n_frames - 1:
            await page.wait_for_timeout(interval_ms)
    return frames

def save_gif(frames, path, frame_ms):
    rgb = [f.convert('RGB') for f in frames]
    rgb[0].save(
        path, save_all=True, append_images=rgb[1:],
        duration=frame_ms, loop=0, optimize=False,
    )
    print(f'  ✓  {path}  ({len(frames)} frames, {frame_ms} ms/frame)')


# ── Badge 1: RNA MINT — Fresh ideas ──────────────────────────────────

FRESH_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#fff; display:flex; align-items:center;
       justify-content:flex-start; padding:14px 18px;
       font-family:'Plus Jakarta Sans',sans-serif; }

.mint-tagline {
  display: inline-flex; align-items: center; gap: .45rem;
  padding: .3rem .9rem .3rem .7rem;
  border-radius: 20px;
  background: rgba(102,168,158,.10);
  border: 1.5px solid rgba(102,168,158,.35);
  font-size: .82rem; font-weight: 700;
  color: #66a89e;
  animation: mint-glow 4s ease-in-out infinite;
  white-space: nowrap;
}
.mint-leaf { display:inline-block; animation: leaf-sway 2.5s ease-in-out infinite; }
@keyframes mint-glow {
  0%,100%{ box-shadow:0 0 0 rgba(102,168,158,0); }
  50%     { box-shadow:0 0 12px rgba(102,168,158,.35); }
}
@keyframes leaf-sway {
  0%,100%{ transform:rotate(-12deg); }
  50%    { transform:rotate(12deg); }
}
</style></head>
<body>
<div class="mint-tagline" id="badge">
  <span class="mint-leaf">🌿</span>
  <span id="typed"></span>
</div>
<script>
const msg = 'RNA MINT — Fresh ideas';
let i = 0;
function type() {
  if (i <= msg.length) {
    document.getElementById('typed').textContent = msg.slice(0, i++);
    if (i <= msg.length) setTimeout(type, 65);
  }
}
setTimeout(type, 400);
</script>
</body></html>"""

# ── Badge 2: KIS ─────────────────────────────────────────────────────

KIS_HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { background:#fff; display:flex; align-items:center;
       justify-content:flex-start; padding:14px 18px;
       font-family:'Plus Jakarta Sans',sans-serif; }

.kis-badge {
  display: inline-flex; align-items: center; gap: .35rem;
  padding: .25rem .75rem;
  background: #e4f2f0;
  color: #4a8880;
  border: 1.5px solid #66a89e;
  border-radius: 20px;
  font-size: .72rem; font-weight: 800; letter-spacing: .04em;
  white-space: nowrap;
  opacity: 1;
}
.kis-emoji {
  font-size: 1em;
  animation: kis-spin 6s linear infinite;
  display: inline-block;
}
@keyframes kis-spin {
  0%,90%,100%{ transform:rotate(0deg); }
  50%         { transform:rotate(360deg); }
}
</style></head>
<body>
<div class="kis-badge" id="badge">
  <span class="kis-emoji">✨</span>
  <span>KIS</span>
</div>
</body></html>"""


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()

        # ── Fresh ideas GIF ──────────────────────────────────────────
        print('Capturing: RNA MINT — Fresh ideas …')
        ctx = await browser.new_context(
            viewport={'width': 600, 'height': 90},
            device_scale_factor=2,
        )
        page = await ctx.new_page()
        await page.set_content(FRESH_HTML)
        # Wait for font to load
        await page.wait_for_timeout(800)

        # Capture typewriter phase: 22 chars × 65 ms ≈ 1430 ms → sample every 65 ms
        # Then capture glow + sway for another 4 s (one glow cycle)
        FRAME_MS = 65
        N_TYPE   = 24   # slightly more than the 22 chars to catch the end
        N_HOLD   = 62   # ~4 s of looping glow (62 × 65 ms ≈ 4 s)

        frames = await capture_frames(page, '#badge', N_TYPE + N_HOLD, FRAME_MS)
        await ctx.close()

        save_gif(frames, OUT / 'rnamint_fresh_ideas.gif', FRAME_MS)

        # ── KIS GIF ──────────────────────────────────────────────────
        print('Capturing: KIS badge …')
        ctx = await browser.new_context(
            viewport={'width': 300, 'height': 80},
            device_scale_factor=2,
        )
        page = await ctx.new_page()
        await page.set_content(KIS_HTML)
        await page.wait_for_timeout(600)

        # One full 6-second spin cycle sampled at 60 ms → 100 frames
        FRAME_MS_K = 60
        N_K        = 100

        frames_k = await capture_frames(page, '#badge', N_K, FRAME_MS_K)
        await ctx.close()

        save_gif(frames_k, OUT / 'kis_keep_it_simple.gif', FRAME_MS_K)

        await browser.close()
    print('Done.')

asyncio.run(main())
