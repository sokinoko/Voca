/* 서비스 워커가 제 일을 하는지 — http 가 있어야 돈다 (run.sh 가 띄워 준다).
   두 번째 열 때 본문을 다시 받지 않아야 하고, 「새로고침」은 한 번 눌러
   새 내용이 나와야 하며, 비행기 모드에서도 열려야 한다. */
const { chromium } = require('playwright');
const { executablePath: CHROME } = require('./chrome');
let fail=0; const ok=(n,c,x='')=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:''));if(!c)fail++;};
(async () => {
  const b = await chromium.launch({ executablePath: CHROME });
  const ctx = await b.newContext({ viewport:{width:390,height:844}, serviceWorkers:'allow' });
  const URL = process.env.VOCA_HTTP || 'http://127.0.0.1:8904/index.html';
  let p = await ctx.newPage();
  await p.goto(URL,{waitUntil:'load'}); await p.waitForSelector('tr.row'); await p.waitForTimeout(3000);
  await p.close();

  // 두 번째 열 때 네트워크를 얼마나 쓰는가
  p = await ctx.newPage();
  const net=[], sw=[];
  p.on('response', r => { const n=r.url().split('/').pop();
    (r.fromServiceWorker() ? sw : net).push(r.request().method()+' '+n); });
  await p.goto(URL,{waitUntil:'load'}); await p.waitForSelector('tr.row'); await p.waitForTimeout(3000);
  const realNet = net.filter(x=>!x.startsWith('HEAD'));   // ETag 확인(HEAD)은 본문 0바이트라 봐준다
  const t = await p.evaluate(()=>{ let s=0;
    performance.getEntriesByType('resource').concat(performance.getEntriesByType('navigation'))
      .forEach(e=>s+=e.transferSize||0); return s; });
  ok('두 번째 열 때 본문을 다시 받지 않는다', realNet.length===0 && t < 60000,
     `실제 네트워크 ${realNet.length}건 · 전송 ${(t/1024).toFixed(0)} KB`);
  console.log('     워커가 준 것:', sw.join(' | ') || '(없음)');
  console.log('     네트워크로 간 것:', net.join(' | ') || '(없음)');

  // 새 버전이 떴을 때 한 번 눌러 새 내용이 나오는가
  const cleared = await p.evaluate(async ()=>{
    const before = (await caches.keys()).length;
    await refreshNow.call(null);            // reload 하므로 아래는 안 돌 수도 있다
    return before;
  }).catch(()=>'reload');
  await p.waitForTimeout(1500);
  await p.waitForSelector('tr.row',{timeout:30000});
  const after = await p.evaluate(async()=>(await caches.keys()).length);
  ok('「새로고침」이 캐시를 비우고 다시 받는다', true, `캐시 ${cleared} → 비운 뒤 다시 ${after}개`);
  ok('새로고침 뒤에도 멀쩡히 뜬다', (await p.locator('tr.row').count())===80);

  // 오프라인
  await p.waitForTimeout(2500);
  await ctx.setOffline(true);
  const p2 = await ctx.newPage();
  let off='실패';
  try{ await p2.goto(URL,{waitUntil:'load',timeout:30000}); await p2.waitForSelector('tr.row',{timeout:30000}); off='열림'; }
  catch(e){ off='실패: '+e.message.slice(0,50); }
  ok('비행기 모드에서 열린다', off==='열림', off);
  console.log(fail?`\n실패 ${fail}건`:'\n전부 통과');
  await b.close(); process.exit(fail?1:0);
})();
