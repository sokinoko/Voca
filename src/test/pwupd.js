const { chromium } = require('playwright');
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');   // 저장소의 index.html

const fs=require('fs');
let fails=0; const ok=(n,c,x)=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:''));if(!c)fails++;};
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({ viewport:{width:390,height:844} });
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto('http://127.0.0.1:8778/index.html'); await p.waitForTimeout(1200);
  ok('처음엔 알림이 없다', (await p.locator('#updBar').count())===0);
  const tag1 = await p.evaluate(()=>verTag);
  ok('ETag를 기준값으로 잡는다', !!tag1, String(tag1).slice(0,24));

  // 파일을 바꿔 배포된 것처럼 만든다
  const s = fs.readFileSync(require('path').join(__dirname,'..','..','index.html'),'utf8');
  fs.writeFileSync(require('path').join(__dirname,'..','..','index.html'), s.replace('</body>','<!-- v2 --></body>'));
  await p.waitForTimeout(1100);
  // 앱을 다시 앞으로 가져온 것처럼
  await p.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
  await p.waitForTimeout(900);
  ok('파일이 바뀌면 알림이 뜬다', (await p.locator('#updBar').count())===1);
  console.log('   알림 문구:', (await p.locator('#updBar').textContent().catch(()=>'')).trim());
  ok('새로고침 버튼이 있다', (await p.locator('#updBtn').count())===1);
  const box = await p.locator('#updBar').boundingBox();
  const foot = await p.locator('.foot').boundingBox();
  ok('알림이 탭 바를 가리지 않는다', box.y + box.height <= foot.y + 2,
     `알림끝 ${Math.round(box.y+box.height)} / 탭 시작 ${Math.round(foot.y)}`);
  await p.locator('#updBtn').click(); await p.waitForTimeout(1200);
  ok('새로고침하면 알림이 사라진다', (await p.locator('#updBar').count())===0);
  ok('JS 에러 없음', errs.length===0, errs[0]||'');
  console.log(fails?`실패 ${fails}건`:'전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
