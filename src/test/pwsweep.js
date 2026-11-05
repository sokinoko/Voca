/* 여섯 탭을 돌며 폰 폭(390px)에서 화면이 가로로 밀리지 않는지 본다.
   필터가 한 칸 늘어 줄이 넘칠 때 이 검사가 잡았다.
   전에는 「수정 전/후」를 나란히 찍어 보는 일회용 스크립트였는데, 비교 대상이
   임시 폴더에 있어 컨테이너가 바뀌면 통째로 못 돌았다. 지금 앱만 보고 단정한다. */
const { chromium } = require('playwright');
const { executablePath: CHROME } = require('./chrome');
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');

const modes = [['list','목록'],['card','카드'],['quiz','시험'],['poly','반복'],['apx','부록'],['sheet','시험지']];
let fails = 0;
const ok = (n, c, x) => { console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:'')); if(!c) fails++; };

(async () => {
  const b = await chromium.launch({ executablePath: CHROME });
  const p = await b.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:1 });
  const errs = []; p.on('pageerror', e => errs.push(String(e)));
  await p.goto(APP); await p.waitForTimeout(700);

  for (const [m, name] of modes) {
    const btn = await p.$(`button[data-mode="${m}"]`);
    if (!btn) { ok(name + ' 탭이 있다', false); continue; }
    await btn.click(); await p.waitForTimeout(400);
    const r = await p.evaluate(() => ({
      넘침: document.documentElement.scrollWidth > window.innerWidth,
      폭: document.documentElement.scrollWidth,
      범인: [...document.querySelectorAll('body *')]
        .filter(e => e.getBoundingClientRect().right > window.innerWidth + 1)
        .slice(0, 3).map(e => e.tagName + '.' + (e.className || '').toString().slice(0, 24)),
    }));
    ok(name.padEnd(4) + ' 가로로 밀리지 않는다', !r.넘침,
       r.넘침 ? `폭 ${r.폭} ← ${r.범인.join(', ')}` : `폭 ${r.폭}`);
  }
  ok('JS 에러 없음', errs.length === 0, errs[0] || '');

  console.log(fails ? `\n실패 ${fails}건` : '\n전부 통과');
  await b.close();
  process.exit(fails ? 1 : 0);
})();
