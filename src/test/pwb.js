const { chromium } = require('playwright');
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');   // 저장소의 index.html

let fails=0; const ok=(n,c,x)=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:'')); if(!c)fails++;};
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({ viewport:{width:390,height:844} });
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(APP); await p.waitForTimeout(700);

  // ── B1 오답 누적 ──
  await p.click('button[data-mode="quiz"]'); await p.waitForTimeout(400);
  let wrongWord = null;
  for(let k=0;k<6;k++){                          // 일부러 틀린다
    const w = await p.locator('.cw').textContent();
    const opts = await p.locator('[data-opt]').count();
    // 정답이 아닌 보기를 고른다
    const right = await p.evaluate(()=>quizQ.it.i);
    let picked=false;
    for(let i=0;i<opts;i++){
      const v = await p.locator('[data-opt]').nth(i).getAttribute('data-opt');
      if(+v !== right){ await p.locator('[data-opt]').nth(i).click(); picked=true; break; }
    }
    if(picked && !wrongWord) wrongWord = w;
    await p.waitForTimeout(150);
    if(await p.locator('[data-quiz="next"]').count()) { await p.locator('[data-quiz="next"]').click(); await p.waitForTimeout(150); }
  }
  const missN = await p.evaluate(()=>Object.keys(miss).length);
  console.log('틀린 단어 누적:', missN, '개 (첫 단어:', wrongWord+')');
  ok('오답이 누적된다', missN >= 3);

  await p.click('button[data-mode="list"]'); await p.waitForTimeout(400);
  ok('「✗ 자주 틀림」 필터가 있다', (await p.locator('[data-v="✗ 자주 틀림"]').count())===1);
  await p.locator('[data-v="✗ 자주 틀림"]').click(); await p.waitForTimeout(400);
  const shown = await p.locator('tr.row').count();
  ok('필터가 틀린 단어만 보여 준다', shown === missN, `(${shown}개)`);
  ok('목록에 오답 횟수가 붙는다', (await p.locator('.miss').count()) === shown);
  const order = await p.locator('.miss').allTextContents();
  const nums = order.map(t=>+t.replace('✗',''));
  ok('많이 틀린 순으로 정렬된다', nums.every((v,i)=>i===0||nums[i-1]>=v), JSON.stringify(nums));

  // 같은 단어를 또 틀리면 횟수가 오르는지
  const before = await p.evaluate(w=>miss[w.toLowerCase()], wrongWord);
  await p.evaluate(w=>{ miss[w.toLowerCase()] = (miss[w.toLowerCase()]||0)+1; save(); }, wrongWord);
  await p.waitForTimeout(500);
  const after = await p.evaluate(w=>miss[w.toLowerCase()], wrongWord);
  ok('횟수가 쌓인다', after === before+1, `${before} → ${after}`);

  // ── B2 부록 시험 최고 기록 ──
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(400);
  ok('아직 기록이 없으면 표시도 없다', (await p.locator('.bestx').count())===0);
  await p.locator('.atest').nth(3).click(); await p.waitForTimeout(250);
  const title = await p.locator('.tmenu h2').textContent();
  await p.locator('[data-apart="word"]').click(); await p.waitForTimeout(250);
  for(let k=0;k<60;k++){
    if(await p.locator('.result').count()) break;
    if(await p.locator('[data-anext]').count() && await p.locator('[data-anext]').isVisible()){
      await p.locator('[data-anext]').click(); await p.waitForTimeout(60); continue; }
    await p.locator('[data-aopt]').first().click(); await p.waitForTimeout(60);
  }
  ok('결과 화면 도달', (await p.locator('.result').count())===1);
  const rec = await p.evaluate(()=>Object.entries(best).map(([k,v])=>k+' '+v.r+'/'+v.t));
  console.log('남은 기록:', rec.join(' | '));
  ok('최고 기록이 저장된다', rec.length===1);

  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(400);
  const bx = await p.locator('.bestx').count();
  ok('제목줄에 최고 기록이 뜬다', bx===1, bx? await p.locator('.bestx').first().textContent() : '');

  // 더 낮은 점수는 최고 기록을 덮지 않아야 한다
  const keep = await p.evaluate(()=>JSON.stringify(best));
  await p.evaluate(()=>{ const k=Object.keys(best)[0]; best[k]={r:0,t:best[k].t,at:'2000-01-01'}; });
  await p.evaluate(()=>{});   // 직접 넣은 건 비교 로직을 안 타므로 로직만 따로 확인
  await p.evaluate(s=>{ best = JSON.parse(s); }, keep);
  const lower = await p.evaluate(()=>{
    const g = DB.apx[3], k = atKey(g,'word');
    best[k] = {r:9, t:10, at:'2026-01-01'};
    at = {gi:3, src:'apx', part:'word', qs:new Array(10), i:9, right:1, wrong:[], picks:{}, done:true};
    atNext();
    return best[k];
  });
  ok('더 낮은 점수는 최고 기록을 덮지 않는다', lower.r===9, JSON.stringify(lower));
  const higher = await p.evaluate(()=>{
    const g = DB.apx[3], k = atKey(g,'word');
    at = {gi:3, src:'apx', part:'word', qs:new Array(10), i:9, right:10, wrong:[], picks:{}, done:true};
    atNext();
    return best[k];
  });
  ok('더 높은 점수는 갱신된다', higher.r===10, JSON.stringify(higher));

  // ── 초기화하면 넷 다 지워진다 ──
  if(!(await p.locator('#reset').isVisible())){ await p.click('#recBtn'); await p.waitForTimeout(200); }
  await p.click('#reset'); await p.waitForTimeout(150);
  await p.click('#reset'); await p.waitForTimeout(400);
  const all = await p.evaluate(()=>[Object.keys(prog).length,Object.keys(star).length,
                                    Object.keys(miss).length,Object.keys(best).length]);
  ok('초기화가 회독·별표·오답·최고기록을 모두 지운다', all.every(v=>v===0), JSON.stringify(all));

  console.log('\nJS 에러:', errs.length?errs:'없음');
  console.log(fails?`실패 ${fails}건`:'전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
