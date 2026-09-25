const { chromium } = require('playwright');
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');   // 저장소의 index.html

// 인라인이든 아래 세로 배치든 상관없이 빈칸을 앞에서부터 하나씩 고른다
async function pickBlanks(p){
  const idx = await p.locator('[data-cz]').evaluateAll(
    els => [...new Set(els.map(e => e.dataset.cz.split('.')[0]))]);
  for(const bi of idx){
    await p.locator(`[data-cz^="${bi}."]`).first().click();
    await p.waitForTimeout(50);
  }
  return idx.length > 0;
}

let fails=0; const ok=(n,c)=>{if(!c){console.log('  실패  '+n);fails++;}};
async function answerOne(p){                       // 지금 화면 문항 하나 풀기
  if(await p.locator('[data-cz]').count()){
    return await pickBlanks(p);
  }
  if(await p.locator('[data-aopt]').count()){
    await p.locator('[data-aopt]').first().click(); await p.waitForTimeout(60); return true;
  }
  return false;
}
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({ viewport:{width:390,height:844} });
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(APP); await p.waitForTimeout(700);
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(400);

  const total = await p.locator('.atest').count();
  console.log('시험 버튼', total, '개\n');
  ok('19곳 전부에 시험 버튼', total === 19);

  for(let i=0;i<total;i++){
    await p.click('button[data-mode="apx"]'); await p.waitForTimeout(250);
    await p.locator('.atest').nth(i).click(); await p.waitForTimeout(250);
    const title = (await p.locator('.tmenu h2').textContent()).trim().replace(/\s+/g,' ');
    const menu  = (await p.locator('.tmenu').textContent()).replace(/\s+/g,' ');
    const nc = (menu.match(/개념 시험 [^·]*· (\d+)문항/)||[])[1];
    const nw = (menu.match(/단어 시험 [^·]*· (\d+)문항/)||[])[1];
    let line = '  ' + String(i+1).padStart(2) + '. ' + title.slice(0,34).padEnd(36) +
               ' 개념 ' + String(nc||'-').padStart(4) + ' · 단어 ' + String(nw||'-').padStart(4);
    // 연결사 묶음은 개념 시험을 일부러 두지 않는다(통합 시험으로 보낸다)
    const connOnly = menu.includes('접속사 통합 시험으로');
    ok(title+' 개념 문항 있음', !!nc || connOnly); ok(title+' 단어 문항 있음', !!nw);

    // 개념 3문항, 단어 3문항 실제로 풀어 본다
    for(const part of ['concept','word']){
      if(!await p.locator(`[data-apart="${part}"]`).count()){ line += ' · '+(part==='concept'?'개-':'단-'); continue; }
      await p.locator(`[data-apart="${part}"]`).click(); await p.waitForTimeout(220);
      let solved=0;
      for(let k=0;k<3;k++){
        if(await p.locator('.result').count()) break;
        if(!await answerOne(p)) break;
        solved++;
        if(await p.locator('[data-anext]').count() && await p.locator('[data-anext]').isVisible()){
          await p.locator('[data-anext]').click(); await p.waitForTimeout(120); }
      }
      ok(title+' '+part+' 풀림', solved>0);
      line += ' · ' + (part==='concept'?'개':'단') + (solved>0?'✓':'✗');
      await p.click('button[data-mode="apx"]'); await p.waitForTimeout(200);
      await p.locator('.atest').nth(i).click(); await p.waitForTimeout(200);
    }
    console.log(line);
  }
  console.log('\nJS 에러:', errs.length?errs.slice(0,3):'없음');
  console.log(fails?`실패 ${fails}건`:'전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
