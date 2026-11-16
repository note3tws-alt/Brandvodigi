// Step 2: render bundle-driven routes in Chromium and save the rendered #root HTML.
const http = require('http'), fs = require('fs'), path = require('path');
const { chromium } = require('playwright');
const ROOT = process.argv[2], OUTJSON = process.argv[3];
const types = { '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml', '.xml': 'application/xml' };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  let f = path.join(ROOT, p);
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  if (!fs.existsSync(f)) f = path.join(ROOT, 'index.html');
  res.writeHead(200, { 'content-type': types[path.extname(f)] || 'application/octet-stream' });
  fs.createReadStream(f).pipe(res);
}).listen(8765);
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  const routes = process.argv.slice(4);
  const out = {};
  for (const r of routes) {
    await page.goto('http://localhost:8765' + r, { waitUntil: 'networkidle' });
    await page.waitForTimeout(800);
    // scroll through so reveal-on-scroll sections render, then back to top
    await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 60)); } window.scrollTo(0, 0); });
    await page.waitForTimeout(600);
    out[r] = { root: await page.evaluate(() => document.getElementById('root').innerHTML), title: await page.title() };
    console.log(r, out[r].root.length, out[r].title);
  }
  fs.writeFileSync(OUTJSON, JSON.stringify(out));
  console.log('errors:', errors.slice(0, 8));
  await browser.close(); server.close();
})();
