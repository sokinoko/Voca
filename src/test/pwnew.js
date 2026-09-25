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

let fails=0; const ok=(n,c,x)=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:'')); if(!c)fails++;};
async function answerOne(p){
  if(await p.locator('[data-cz]').count()){
    return await pickBlanks(p);
  }
  if(await p.locator('[data-aopt]').count()){ await p.locator('[data-aopt]').first().click(); await p.waitForTimeout(55); return true; }
  return false;
}
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({ viewport:{width:390,height:844} });
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(APP); await p.waitForTimeout(700);
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(400);

  // ── 접속사 통합 시험 ──
  ok('부록 탭에 「접속사 통합 시험」 버튼이 있다', (await p.locator('[data-asrc="conn"]').count())>=1);
  await p.locator('[data-asrc="conn"]').first().click(); await p.waitForTimeout(300);
  const menu=(await p.locator('.tmenu').textContent()).replace(/\s+/g,' ');
  console.log('  통합 시험 메뉴:', menu.trim().slice(0,86));
  const nc=+(menu.match(/개념 시험 [^·]*· (\d+)문항/)||[])[1];
  ok('통합 개념 문항이 충분하다', nc>100, nc+'문항');
  await p.locator('[data-apart="concept"]').click(); await p.waitForTimeout(300);
  // 지문 문항이 나올 때까지 넘겨 본다
  let sawPassage=false, sawFive=false;
  for(let k=0;k<30 && !(sawPassage&&sawFive);k++){
    const t=(await p.locator('.czs').textContent()).trim();
    // 지문 문항 = 빈칸 앞에 온전한 문장이 하나 더 있는 것.
    // 보기를 세로로 빼면서 .czs 길이가 짧아졌으므로 글자 수 대신 문장 수로 본다.
    const before=t.split(/[_(]/)[0];
    if(/[.!?]\s/.test(before) && before.length>40) sawPassage=true;
    if(await p.locator('[data-cz^="0."]').count()===5) sawFive=true;
    await answerOne(p); await p.waitForTimeout(60);
    if(await p.locator('[data-anext]').count()) { await p.locator('[data-anext]').click(); await p.waitForTimeout(70); }
  }
  ok('앞 문장이 붙은 지문 문항이 나온다', sawPassage);
  ok('5지선다 문항이 나온다', sawFive);

  // ── 연결사 묶음: 개별 개념 시험이 없고 통합으로 안내 ──
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(350);
  const lbl=await p.locator('.atest').first().textContent();
  ok('연결사 묶음 버튼이 「단어 시험」이다', lbl.trim()==='단어 시험', lbl.trim());
  await p.locator('.atest').first().click(); await p.waitForTimeout(300);
  const m2=(await p.locator('.tmenu').textContent()).replace(/\s+/g,' ');
  ok('개념 시험 대신 통합 시험 안내가 뜬다', m2.includes('접속사 통합 시험으로'));
  await p.locator('.tmenu [data-asrc="conn"]').click(); await p.waitForTimeout(300);
  ok('안내를 누르면 통합 시험으로 간다',
     (await p.locator('.tmenu h2').textContent()).includes('접속사 통합'));

  // ── 동의어 문항: 밑줄 표시 ──
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(350);
  const gi=await p.locator('.grp h3').evaluateAll(e=>e.findIndex(x=>x.textContent.includes('뉘앙스')));
  await p.locator('.atest').nth(gi).click(); await p.waitForTimeout(250);
  await p.locator('[data-apart="concept"]').click(); await p.waitForTimeout(300);
  ok('동의어 문항에 밑줄이 그려진다', (await p.locator('.czs .czu').count())===1,
     await p.locator('.czs .czu').textContent().catch(()=>''));
  ok('밑줄 기호가 글자로 새지 않는다', !(await p.locator('.czs').textContent()).match(/[⟦⟧]/));
  ok('동의어 보기 5개', (await p.locator('[data-cz^="0."]').count())===5);
  await answerOne(p); await p.waitForTimeout(200);
  ok('채점되고 해설이 뜬다', (await p.locator('.czn').count())===1);

  // ── 전치사 지도: 용법 판정 ──
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(350);
  const pi=await p.locator('.atest').evaluateAll(e=>e.findIndex(x=>x.dataset.asrc==='prep'));
  await p.locator('.atest').nth(pi).click(); await p.waitForTimeout(250);
  await p.locator('[data-apart="concept"]').click(); await p.waitForTimeout(300);
  const ps=await p.locator('.czs').textContent();
  ok('전치사는 용법 판정으로 바뀌었다', /여기서/.test(ps), ps.replace(/\s+/g,' ').slice(0,60));

  // ── 전 유닛 워크 ──
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(350);
  const total=await p.locator('.atest').count();
  console.log('\n  개별 시험 버튼', total, '개 + 통합 1개');
  let walked=0;
  for(let i=0;i<total;i++){
    await p.click('button[data-mode="apx"]'); await p.waitForTimeout(180);
    await p.locator('.atest').nth(i).click(); await p.waitForTimeout(180);
    for(const part of ['concept','word']){
      if(!await p.locator(`[data-apart="${part}"]`).count()) continue;
      await p.locator(`[data-apart="${part}"]`).click(); await p.waitForTimeout(180);
      if(await answerOne(p)) walked++;
      await p.click('button[data-mode="apx"]'); await p.waitForTimeout(150);
      await p.locator('.atest').nth(i).click(); await p.waitForTimeout(150);
    }
  }
  ok('모든 버튼에서 시험이 실제로 풀린다', walked>=total, walked+'개 파트');

  console.log('\nJS 에러:', errs.length?errs.slice(0,3):'없음');
  console.log(fails?`실패 ${fails}건`:'전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
