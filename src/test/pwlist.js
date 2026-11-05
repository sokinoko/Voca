const { chromium } = require('playwright');
const { executablePath: CHROME } = require('./chrome');
const path = require('path');
// 서비스 워커·글꼴은 http 가 있어야 본다. 없으면 목록 동작만 본다
const HTTP = process.env.VOCA_HTTP || '';
const APP = HTTP || ('file://' + path.join(__dirname, '..', '..', 'index.html'));
let fail=0; const ok=(n,c,x='')=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:'')); if(!c)fail++;};
(async () => {
  const b = await chromium.launch({ executablePath: CHROME });
  const ctx = await b.newContext({ viewport:{width:390,height:844}, serviceWorkers:'allow' });
  const p = await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(APP, { waitUntil:'load' });
  await p.waitForSelector('tr.row');

  const n0 = await p.locator('tr.row').count();
  ok('처음에는 80줄만 그린다', n0===80, `${n0}줄`);
  ok('「더 보기」가 남은 수를 알려 준다', /\d+개 더 보기/.test(await p.locator('#listMoreBtn').textContent()||''),
     (await p.locator('#listMoreBtn').textContent()||'').trim());
  const total = +(await p.locator('p.count b').textContent());

  await p.click('#listMoreBtn'); await p.waitForTimeout(300);
  ok('누르면 이어 붙는다', (await p.locator('tr.row').count())===160, `${await p.locator('tr.row').count()}줄`);

  // 아래로 내리면 저절로 이어 붙는가
  for (let i=0;i<4;i++){ await p.mouse.wheel(0, 20000); await p.waitForTimeout(500); }
  const n2 = await p.locator('tr.row').count();
  ok('스크롤하면 저절로 더 붙는다', n2 > 160, `${n2}줄`);

  // 번호가 이어지는가
  const nums = await p.$$eval('tr.row .tdnum', ns=>ns.map(x=>+x.textContent));
  ok('번호가 1부터 끊김 없이 이어진다', nums.every((v,i)=>v===i+1), `끝 ${nums[nums.length-1]}`);

  // 회독 점이 제자리에서 바뀌는가 (목록이 다시 그려지지 않아야)
  await p.evaluate(()=>window.scrollTo(0,0)); await p.waitForTimeout(200);
  const before = await p.locator('tr.row').count();
  const y0 = await p.evaluate(()=>window.scrollY);
  await p.locator('tr.row').first().locator('.dot').nth(1).click(); await p.waitForTimeout(250);
  const onCnt = await p.locator('tr.row').first().locator('.dot.on').count();
  ok('회독 점이 켜진다', onCnt===2, `${onCnt}개 켜짐`);
  ok('회독을 눌러도 목록이 처음으로 안 돌아간다', (await p.locator('tr.row').count())===before,
     `${before} → ${await p.locator('tr.row').count()}`);
  ok('보던 자리도 그대로', Math.abs((await p.evaluate(()=>window.scrollY))-y0) < 5);

  // 필터를 바꾸면 처음부터
  await p.click('[data-f="exam"][data-v="26 9모"]'); await p.waitForTimeout(400);
  const n3 = await p.locator('tr.row').count();
  ok('필터를 바꾸면 처음 80줄로 돌아간다', n3===80, `${n3}줄`);
  const t3 = +(await p.locator('p.count b').textContent());
  ok('필터가 제대로 걸린다', t3>0 && t3<total, `${t3}개 / 전체 ${total}개`);

  // 적은 결과에서는 「더 보기」가 없어야
  await p.fill('#q', 'announce'); await p.waitForTimeout(500);
  ok('결과가 적으면 「더 보기」가 없다', (await p.locator('#listMoreBtn').count())===0);

  if (HTTP) {
    const fontOk = await p.evaluate(async ()=>{ await document.fonts.ready;
      return [...document.fonts].some(f=>f.family==='Hahmlet' && f.status==='loaded'); });
    ok('Hahmlet 글꼴이 파일에서 실린다', fontOk);

    await p.waitForTimeout(2500);
    await ctx.setOffline(true);
    const p2 = await ctx.newPage();
    let off='실패';
    try { await p2.goto(APP,{waitUntil:'load',timeout:30000});
          await p2.waitForSelector('tr.row',{timeout:30000});
          const f = await p2.evaluate(async()=>{ await document.fonts.ready;
            return [...document.fonts].some(x=>x.family==='Hahmlet'&&x.status==='loaded'); });
          off = f ? '열림 + 글꼴도 나옴' : '열림 (글꼴 없음)'; } catch(e){ off='실패: '+e.message.slice(0,50); }
    ok('비행기 모드에서도 열린다', off.startsWith('열림'), off);
  } else {
    console.log('  건너뜀  글꼴·오프라인은 http 가 필요하다 (VOCA_HTTP=http://… 로 돌린다)');
  }

  ok('JS 오류 없음', errs.length===0, errs[0]||'');
  console.log(fail?`\n실패 ${fail}건`:'\n전부 통과');
  await b.close(); process.exit(fail?1:0);
})();
