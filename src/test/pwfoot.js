const { chromium } = require('playwright');
// 스크린샷은 저장소에 남기지 않는다
const SHOT = n => require('path').join(require('os').tmpdir(), 'voca-' + n);
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');   // 저장소의 index.html

let fails=0; const ok=(n,c,x)=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:''));if(!c)fails++;};
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:2 });
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(APP); await p.waitForTimeout(700);
  ok('평소엔 기록 버튼이 접혀 있다', !(await p.locator('#expBtn').isVisible()));
  const navBox = await p.locator('.foot .seg').boundingBox();
  const recBox = await p.locator('#recBtn').boundingBox();
  ok('탭 바와 기록 버튼이 한 줄에 겹치지 않는다',
     recBox.x >= navBox.x + navBox.width - 1, `nav끝 ${Math.round(navBox.x+navBox.width)} / 기록 ${Math.round(recBox.x)}`);
  ok('탭 6개가 모두 보인다', (await p.locator('.foot .seg button').count())===6
     && (await p.locator('.foot .seg button').last().isVisible()));
  await p.screenshot({path: SHOT('foot-closed.png')});
  await p.click('#recBtn'); await p.waitForTimeout(250);
  ok('누르면 펼쳐진다', await p.locator('#expBtn').isVisible());
  await p.screenshot({path: SHOT('foot-open.png')});
  await p.click('#recBtn'); await p.waitForTimeout(250);
  ok('다시 누르면 접힌다', !(await p.locator('#expBtn').isVisible()));
  // 가로 넘침 없는지
  ok('가로 넘침 없음', !(await p.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth)));
  console.log('JS 에러:', errs.length?errs:'없음');
  console.log(fails?`실패 ${fails}건`:'전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
