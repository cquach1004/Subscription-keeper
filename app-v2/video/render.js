// Renders video.html frame by frame (deterministic) into frames/, 1080x1920 at 30fps.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const out = process.argv[2] || '/tmp/mosubi-frames'; fs.mkdirSync(out, { recursive: true });
  const only = process.argv[3] ? process.argv[3].split(',').map(Number) : null;
  const b = await chromium.launch();
  const pg = await b.newPage({ viewport: { width: 540, height: 960 }, deviceScaleFactor: 2 });
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto('file://' + path.join(__dirname, 'video.html') + '?still');
  await pg.evaluate(() => document.fonts.ready);
  const FPS = 30, DUR = 14.5;
  if (only) { for (const t of only) { await pg.evaluate(t => window.seek(t), t); await pg.screenshot({ path: `${out}/t${t}.png` }); } }
  else for (let f = 0; f < FPS * DUR; f++) { await pg.evaluate(t => window.seek(t), f / FPS); await pg.screenshot({ path: `${out}/f${String(f).padStart(4, '0')}.jpg`, type: 'jpeg', quality: 95 }); }
  console.log('done', errs); await b.close();
})();
