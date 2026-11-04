#!/usr/bin/env node
/* Cloud substitute for the skill's ui_check.py: drive the site in headless Chromium (SwiftShader WebGL).
 *
 *   node handoff/tools/ui_check.js [--route '#/atlas'] [--store key=JSON ...] [--before JS] [--wait ms]
 *                                  [--screenshot out.png] [--eval JS] [--smoke] [--size 1400x900]
 *
 * --store sets localStorage 'ca.<key>' before the page loads (region, theme, atlas.species, atlas.circuit.<region>, ...).
 * --smoke visits every view in the nav and prints {view: {errbar, log}}; each must be empty.
 * Otherwise it loads --route, runs --before, waits, prints errbar/log (and --eval's result), and takes the screenshot.
 * Run from anywhere; the site is loaded from file:// (the repo root is two levels up from this file).
 */
'use strict';
const path = require('path');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..', '..');
const args = process.argv.slice(2);
const opt = { route: '#/atlas', store: {}, before: [], wait: 1500, screenshot: null, evals: [], smoke: false, size: [1400, 900] };
for (let i = 0; i < args.length; i++) {
  const a = args[i], v = () => args[++i];
  if (a === '--route') opt.route = v();
  else if (a === '--store') { const s = v(), k = s.indexOf('='); opt.store[s.slice(0, k)] = s.slice(k + 1); }
  else if (a === '--before') opt.before.push(v());
  else if (a === '--wait') opt.wait = +v();
  else if (a === '--screenshot') opt.screenshot = v();
  else if (a === '--eval') opt.evals.push(v());
  else if (a === '--smoke') opt.smoke = true;
  else if (a === '--size') opt.size = v().split('x').map(Number);
  else { console.error('unknown argument ' + a); process.exit(2); }
}
for (const [k, s] of Object.entries(opt.store)) { try { JSON.parse(s); } catch (e) { console.error(`--store ${k}: not JSON: ${s}`); process.exit(2); } }

(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: opt.size[0], height: opt.size[1] }, deviceScaleFactor: 1 });
  let log = [];
  page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') log.push(`${m.type()}: ${m.text()}`); });
  page.on('pageerror', (e) => log.push('pageerror: ' + e.message));
  await page.addInitScript((store) => {
    if (sessionStorage.getItem('ui_check.seeded')) return;   // seed once, so later choices in the page stick
    for (const [k, v] of Object.entries(store)) localStorage.setItem('ca.' + k, v);
    sessionStorage.setItem('ui_check.seeded', '1');
  }, opt.store);
  const url = 'file://' + path.join(ROOT, 'index.html');
  const errbar = () => page.evaluate(() => { const b = document.getElementById('errbar'); return b && getComputedStyle(b).display !== 'none' ? b.textContent.trim() : ''; });

  if (opt.smoke) {
    await page.goto(url + '#/atlas');
    await page.waitForTimeout(opt.wait);
    const views = await page.evaluate(() => [...document.querySelectorAll('#nav a')].map((a) => a.dataset.view));
    const out = {};
    for (const v of views) {
      log = [];
      await page.evaluate((v) => { location.hash = '#/' + v; }, v);
      await page.waitForTimeout(opt.wait);
      for (const js of opt.before) await page.evaluate(js);
      out[v] = { errbar: await errbar(), log };
    }
    const region = await page.evaluate(() => window.CA && CA.region && CA.region.id);
    const theme = await page.evaluate(() => document.documentElement.getAttribute('data-theme'));
    console.log(JSON.stringify({ region, theme, views: out }, null, 1));
    const bad = Object.values(out).some((r) => r.errbar || r.log.length);
    await browser.close();
    process.exit(bad ? 1 : 0);
  }

  await page.goto(url + opt.route);
  await page.waitForTimeout(opt.wait);
  for (const js of opt.before) { await page.evaluate(js); await page.waitForTimeout(opt.wait); }
  const res = { errbar: await errbar(), log };
  if (opt.evals.length) res.eval = [];
  for (const js of opt.evals) res.eval.push(await page.evaluate(js));
  if (opt.screenshot) await page.screenshot({ path: opt.screenshot });
  console.log(JSON.stringify(res, null, 1));
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
