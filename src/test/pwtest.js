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

let fails=0;
const ok=(n,c)=>{console.log((c?'  통과  ':'  실패  ')+n); if(!c)fails++;};
async function fillBlanks(p){                    // render로 DOM이 갈리니 매번 다시 찾는다
  await pickBlanks(p);
}
async function runToEnd(p, kind){
  for(let k=0;k<200;k++){
    if(await p.locator('.result').count()) return true;
    if(await p.locator('[data-anext]').count() && await p.locator('[data-anext]').isVisible()){
      await p.locator('[data-anext]').click(); await p.waitForTimeout(60); continue; }
    if(kind==='concept'){ if(!await p.locator('[data-cz]').count()) return false; await pickBlanks(p); }
    else { await p.locator('[data-aopt]').first().click(); await p.waitForTimeout(70); }
  }
  return false;
}
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:1 });
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(APP); await p.waitForTimeout(700);

  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(400);
  const heads = await p.locator('.grp h3').count();
  const btns  = await p.locator('.atest').count();
  console.log('아코디언', heads, '개 / 시험 버튼', btns, '개 (전치사 지도·as 제외)');
  ok('부록 16 + 문형표·전치사 지도·as = 19개에 시험 버튼', btns === 19);

  // 부록 19 섹션
  const gi = await p.locator('.grp h3').evaluateAll(e=>e.findIndex(x=>x.textContent.includes('동명사냐')));
  await p.locator('.grp h3').nth(gi).click(); await p.waitForTimeout(350);
  ok('부록 19 섹션 구분선 8개', (await p.locator('.axsec').count()) === 8);

  // ── 부록 19 개념 시험 끝까지 ──
  await p.locator('.atest').nth(gi).click(); await p.waitForTimeout(300);
  ok('시험 메뉴', (await p.locator('.tmenu').count()) === 1);
  await p.locator('[data-apart="concept"]').click(); await p.waitForTimeout(300);
  const total = (await p.locator('.sprog').textContent()).match(/\/\s*(\d+)/)[1];
  console.log('   개념 시험 문항 수:', total);
  ok('개념 시험 문항이 넉넉히 있다', +total >= 53);
  ok('개념 시험 완주 → 결과', await runToEnd(p,'concept'));
  console.log('   결과:', (await p.locator('.result').textContent()).replace(/\s+/g,' ').trim().slice(0,100));
  const wrong = +((await p.locator('.result').textContent()).match(/틀린 문제\s*(\d+)/) || [0,0])[1];
  const wrongN = await p.locator('[data-ares="retry"]').count();
  if(wrongN){
    await p.locator('[data-ares="retry"]').click(); await p.waitForTimeout(300);
    // 무작위로 찍기 때문에 틀린 개수는 그때그때 다르다. 결과창이 말한 수와 견준다
    const again = +(await p.locator('.sprog').textContent()).match(/\/\s*(\d+)/)[1];
    ok('틀린 것만 다시 — 틀린 개수만큼만 나온다',
       again === wrong, `틀린 ${wrong}개 → 다시 ${again}문항 (처음 ${total})`);
  }

  // ── 단어 시험 ──
  // 어디에 있든 부록 목록으로 빠져나왔다가 이 그룹 시험 메뉴로 다시 들어간다
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(350);
  await p.locator('.atest').nth(gi).click(); await p.waitForTimeout(300);
  await p.locator('[data-apart="word"]').click(); await p.waitForTimeout(300);
  ok('단어 시험 보기 4개', (await p.locator('[data-aopt]').count()) === 4);
  await p.locator('[data-aopt="0"]').click(); await p.waitForTimeout(250);
  ok('채점되면 정답이 하나 표시된다', (await p.locator('.opt.right').count()) === 1);
  ok('채점 후 다시 눌러도 중복 채점 안 됨', await (async()=>{
      const before = (await p.locator('.sprog').textContent());
      await p.locator('[data-aopt="1"]').click(); await p.waitForTimeout(150);
      return (await p.locator('.sprog').textContent()) === before; })());

  // ── cz 없는 부록 → 자동 생성 ──
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(350);
  const vi = await p.locator('.grp h3').evaluateAll(e=>e.findIndex(x=>x.textContent.includes('전치사에 유의')));
  await p.locator('.atest').nth(vi).click(); await p.waitForTimeout(250);
  await p.locator('[data-apart="concept"]').click(); await p.waitForTimeout(250);
  ok('직접 쓴 문항이 없는 부록도 개념 시험이 만들어진다', (await p.locator('.czq').count()) === 1);
  console.log('   자동 생성 문장:', (await p.locator('.czs').textContent()).replace(/\s+/g,' ').trim().slice(0,70));
  ok('보기가 둘 이상이다', (await p.locator('[data-cz^="0."]').count()) >= 2);

  // ── 문형표 시험 ──
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(350);
  const gj = await p.locator('.atest').evaluateAll(e=>e.findIndex(x=>x.dataset.asrc==='gram'));
  await p.locator('.atest').nth(gj).click(); await p.waitForTimeout(300);
  console.log('   문형표 메뉴:', (await p.locator('.tmenu').textContent()).replace(/\s+/g,' ').trim().slice(0,80));
  await p.locator('[data-apart="word"]').click(); await p.waitForTimeout(300);
  ok('문형표 단어 시험 진입', (await p.locator('[data-aopt]').count()) >= 2);

  // ── 탭 이동하면 시험이 닫힌다 ──
  await p.click('button[data-mode="list"]'); await p.waitForTimeout(300);
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(300);
  ok('탭 갔다 오면 부록 목록으로 복귀', (await p.locator('.tmenu').count())===0 && (await p.locator('.grp').count())>0);

  // ── 반복 탭 ──
  await p.click('button[data-mode="poly"]'); await p.waitForTimeout(400);
  const accs = await p.locator('.acc').count();
  ok('반복 섹션이 아코디언', accs >= 3);
  ok('기본 접힘', (await p.locator('.acc.open').count()) === 0);
  await p.click('#repAll'); await p.waitForTimeout(400);
  ok('모두 펼치기', (await p.locator('.acc.open').count()) === accs);
  await p.locator('.acc h3').first().click(); await p.waitForTimeout(300);
  ok('개별 접기', (await p.locator('.acc.open').count()) === accs-1);

  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(400);
  ok('부록 「모두 펼치기」 라벨이 반복 탭에 오염되지 않음',
     (await p.locator('#accAll').textContent()).includes('모두 펼치기'));

  console.log('\nJS 에러:', errs.length?errs:'없음');
  console.log(fails?`\n실패 ${fails}건`:'\n전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
