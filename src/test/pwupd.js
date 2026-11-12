const { chromium } = require('playwright');
const { executablePath: CHROME } = require('./chrome');
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');   // 저장소의 index.html

const fs=require('fs');
const URL = process.env.VOCA_HTTP || 'http://127.0.0.1:8778/index.html';
/* 이 검사는 배포된 척하려고 index.html 을 잠깐 고친다. 반드시 되돌린다 —
   예전에는 되돌리지 않아 저장소가 더럽혀진 채로 남았다(<!-- v2 -->가 커밋될 뻔했다). */
const HTML = path.join(__dirname, '..', '..', 'index.html');
const ORIG = fs.readFileSync(HTML, 'utf8');
let restored = false;
const restore = () => { if(!restored){ restored = true; try{ fs.writeFileSync(HTML, ORIG); }catch(e){} } };
process.on('exit', restore);
['SIGINT','SIGTERM','uncaughtException','unhandledRejection'].forEach(e=>
  process.on(e, ()=>{ restore(); process.exit(1); }));

let fails=0; const ok=(n,c,x)=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:''));if(!c)fails++;};
(async () => {
  const b = await chromium.launch({executablePath: CHROME});
  const p = await b.newPage({ viewport:{width:390,height:844} });
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(URL); await p.waitForTimeout(1200);
  ok('처음엔 알림이 없다', (await p.locator('#updBar').count())===0);
  const tag1 = await p.evaluate(()=>verTag);
  ok('ETag를 기준값으로 잡는다', !!tag1, String(tag1).slice(0,24));

  // 파일을 바꿔 배포된 것처럼 만든다 (끝나면 restore 가 되돌린다)
  fs.writeFileSync(HTML, ORIG.replace('</body>', '<!-- v2 --></body>'));
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

  // 진짜로 겪은 일: 앱을 끈 사이에 배포되고, 다시 켜면 워커가 캐시의 옛 파일을 띄운다.
  // 그때도 알림이 떠야 한다 (전에는 켤 때 서버 값을 기준으로 잡아 영영 안 떴다)
  await p.reload(); await p.waitForTimeout(1500);              // 지금 파일(v2)이 캐시에 들어간다
  fs.writeFileSync(HTML, ORIG.replace('</body>', '<!-- v3 --></body>'));
  await p.waitForTimeout(1100);
  await p.reload(); await p.waitForTimeout(1500);              // 캐시가 주는 v2로 다시 켜진다
  const fromCache = await p.evaluate(()=>document.documentElement.outerHTML.includes('<!-- v2 -->'));
  ok('다시 켜면 캐시의 옛 파일이 뜬다 (전제)', fromCache);
  ok('그래도 새 배포 알림이 뜬다', (await p.locator('#updBar').count())===1);
  await p.locator('#updBtn').click(); await p.waitForTimeout(1500);
  ok('새로고침하면 새 파일이 뜬다', await p.evaluate(()=>document.documentElement.outerHTML.includes('<!-- v3 -->')));
  ok('JS 에러 없음', errs.length===0, errs[0]||'');
  console.log(fails?`실패 ${fails}건`:'전부 통과');
  await b.close();
  restore();
  process.exit(fails?1:0);
})();
