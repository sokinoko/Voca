/* 크로미움 경로. 컨테이너가 새로 뜰 때마다 버전 폴더 이름이 바뀌어서
   (chromium-1194 → chromium-1243) 테스트가 통째로 안 돌던 일이 두 번 있었다.
   박아 두지 말고 찾아서 쓴다. */
const fs = require('fs'), path = require('path');

function find(){
  if (process.env.CHROME_PATH && fs.existsSync(process.env.CHROME_PATH)) return process.env.CHROME_PATH;
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH || '/opt/pw-browsers';
  let best = null;
  for (const d of (fs.existsSync(root) ? fs.readdirSync(root) : [])) {
    if (!d.startsWith('chromium-')) continue;
    for (const sub of ['chrome-linux64/chrome', 'chrome-linux/chrome']) {
      const p = path.join(root, d, sub);
      if (fs.existsSync(p)) { const n = +d.split('-')[1] || 0; if (!best || n > best.n) best = { p, n }; }
    }
  }
  if (best) return best.p;
  try { return require('playwright').chromium.executablePath(); } catch (e) { return undefined; }
}

module.exports = { executablePath: find() };
