#!/usr/bin/env node
/* Measure how much the 3D atlas labels flicker while the camera moves.
 *
 *   node handoff/tools/label_flicker.js [--store key=JSON ...] [--steps 90] [--dx 3] [--dy 0] [--wait 2500]
 *
 * Loads #/atlas (localStorage 'ca.<key>' seeded from --store), drags the canvas slowly, keeps sampling while the
 * damping settles, and reports per label: how often it was hidden (or faded out) and shown again (blinks) and how often it moved by
 * more than 12 px between two frames (jumps).
 * quick counts blinks where the label came back within 5 frames, which reads as flicker. Natural motion per frame is reported as the median step, for scale.
 */
const path = require('path');
const { chromium } = require('playwright');
const ROOT = path.resolve(__dirname, '..', '..');
const opt = { store: { 'intro.dismissed': 'true' }, steps: 90, dx: 3, dy: 0, wait: 2500, size: [1400, 900] };
const args = process.argv.slice(2);
for (let i = 0; i < args.length; i++) {
  const a = args[i], v = () => args[++i];
  if (a === '--store') { const s = v(), k = s.indexOf('='); opt.store[s.slice(0, k)] = s.slice(k + 1); }
  else if (a === '--steps') opt.steps = +v();
  else if (a === '--dx') opt.dx = +v();
  else if (a === '--dy') opt.dy = +v();
  else if (a === '--wait') opt.wait = +v();
}

(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: opt.size[0], height: opt.size[1] }, deviceScaleFactor: 1 });
  const log = [];
  page.on('pageerror', (e) => log.push('pageerror: ' + e.message));
  page.on('console', (m) => { if (m.type() === 'error') log.push('error: ' + m.text()); });
  await page.addInitScript((store) => { for (const [k, v] of Object.entries(store)) localStorage.setItem('ca.' + k, v); }, opt.store);
  await page.goto('file://' + path.join(ROOT, 'index.html') + '#/atlas');
  await page.waitForTimeout(opt.wait);
  await page.evaluate(() => {
    window.__frames = [];
    const tick = () => {
      const f = {};
      document.querySelectorAll('.atlas-labels .alabel').forEach((e, i) => {
        const key = e.textContent + '#' + i;
        const r = e.getBoundingClientRect();
        f[key] = e.style.display === 'none' || e.classList.contains('off') || !r.width ? null : [Math.round(r.left), Math.round(r.top)];
      });
      window.__frames.push(f);
      if (!window.__stop) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  });
  const box = await page.locator('.atlas-canvas canvas').boundingBox();
  const x0 = box.x + box.width * 0.6, y0 = box.y + box.height * 0.5;
  await page.mouse.move(x0, y0);
  await page.mouse.down();
  for (let k = 1; k <= opt.steps; k++) { await page.mouse.move(x0 + k * opt.dx, y0 + k * opt.dy); await page.waitForTimeout(30); }
  await page.mouse.up();
  await page.waitForTimeout(1500);
  const frames = await page.evaluate(() => { window.__stop = true; return window.__frames; });
  await browser.close();

  const keys = new Set(frames.flatMap((f) => Object.keys(f)));
  let blinks = 0, jumps = 0, quick = 0;   // quick: shown again within 5 frames of being hidden (a visible flicker)
  const steps = [], worst = [];
  for (const k of keys) {
    let b = 0, j = 0;
    for (let i = 1; i < frames.length; i++) {
      const a = frames[i - 1][k], c = frames[i][k];
      if (a === undefined || c === undefined) continue;
      if (a && !c) {
        b++;
        for (let j = i + 1; j < Math.min(frames.length, i + 5); j++) if (frames[j][k]) { quick++; break; }
      }
      if (a && c) {
        const d = Math.max(Math.abs(a[0] - c[0]), Math.abs(a[1] - c[1]));
        steps.push(d);
        if (d > 12) j++;
      }
    }
    // a label hidden once and never shown again is not a blink
    const last = frames[frames.length - 1][k];
    if (!last && b) b--;
    blinks += b; jumps += j;
    if (b + j) worst.push([k.replace(/#\d+$/, ''), b, j]);
  }
  steps.sort((a, b) => a - b);
  worst.sort((a, b) => b[1] + b[2] - a[1] - a[2]);
  console.log(JSON.stringify({ frames: frames.length, labels: keys.size, medianStep: steps[steps.length >> 1] || 0,
    blinks, quick, jumps, worst: worst.slice(0, 8), log }, null, 1));
})().catch((e) => { console.error(e); process.exit(1); });
