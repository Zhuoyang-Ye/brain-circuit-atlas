#!/usr/bin/env node
/* For every species, region and 3D circuit: the labels drawn, the number of pathway objects, whether the trace
 * button shows, and any errbar/console error. Diff two dumps to catch regressions after a 3D change.
 *
 *   node handoff/tools/circuits_dump.js out.json [region ...]
 */
'use strict';
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const ROOT = path.resolve(__dirname, '..', '..');
const [out, ...only] = process.argv.slice(2);
if (!out) { console.error('usage: circuits_dump.js out.json [region ...]'); process.exit(2); }

(async () => {
  const browser = await chromium.launch({ args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const res = {};
  for (const sp of ['human', 'macaque', 'mouse']) {
    const page = await browser.newPage({ viewport: { width: 1400, height: 900 } });
    let log = [];
    page.on('console', (m) => { if (m.type() === 'error' || m.type() === 'warning') log.push(m.text()); });
    page.on('pageerror', (e) => log.push('pageerror: ' + e.message));
    await page.addInitScript((sp) => {
      if (sessionStorage.getItem('seeded')) return;
      localStorage.clear();
      localStorage.setItem('ca.atlas.species', JSON.stringify(sp));
      localStorage.setItem('ca.intro.dismissed', 'true');
      sessionStorage.setItem('seeded', '1');
    }, sp);
    await page.goto('file://' + path.join(ROOT, 'index.html') + '#/atlas');
    await page.waitForTimeout(4000);
    const regions = await page.evaluate(() => CA.D.regions.map((r) => r.id));
    for (const reg of regions) {
      if (only.length && !only.includes(reg)) continue;
      await page.evaluate((reg) => CA.setRegion(reg), reg);
      await page.waitForTimeout(800);
      const circs = await page.evaluate(() => [...document.querySelectorAll('.circ')].map((b) => b.dataset.c));
      for (const c of circs) {
        log = [];
        await page.evaluate((c) => document.querySelector(`.circ[data-c="${c}"]`).click(), c);
        await page.waitForTimeout(500);
        const r = await page.evaluate(() => ({
          labels: [...document.querySelectorAll('.alabel:not(.tx)')].map((e) => e.textContent).sort(),
          trace: document.querySelector('.trace').style.display !== 'none',
          errbar: (() => { const b = document.getElementById('errbar'); return b && getComputedStyle(b).display !== 'none' ? b.textContent.trim() : ''; })(),
        }));
        r.log = log;
        res[`${sp} ${reg} ${c}`] = r;
      }
    }
    await page.close();
  }
  fs.writeFileSync(out, JSON.stringify(res, null, 1));
  console.log(`${Object.keys(res).length} circuits → ${out}`);
  await browser.close();
})().catch((e) => { console.error(e); process.exit(1); });
