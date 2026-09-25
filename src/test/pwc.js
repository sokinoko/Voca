const { chromium } = require('playwright');
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');   // 저장소의 index.html

const fs=require('fs');
let fails=0; const ok=(n,c,x)=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:''));if(!c)fails++;};
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({ viewport:{width:390,height:844} });
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(APP); await p.waitForTimeout(700);
  const openRec = async()=>{ if(!(await p.locator('#fsBtn').isVisible())){ await p.click('#recBtn'); await p.waitForTimeout(200);} };

  // ── C2 글자 크기 ──
  const size = ()=>p.evaluate(()=>parseFloat(getComputedStyle(document.querySelector('.word')).fontSize));
  const base = await size();
  await openRec(); await p.click('#fsBtn'); await p.waitForTimeout(300);
  const big = await size();
  ok('글자 크기를 키울 수 있다', big > base, `${base} → ${big}`);
  await p.click('#fsBtn'); await p.waitForTimeout(300);
  const small = await size();
  ok('한 번 더 누르면 작게', small < base, `${big} → ${small}`);
  await p.click('#fsBtn'); await p.waitForTimeout(300);
  ok('세 번 누르면 원래대로', Math.abs(await size() - base) < 0.5);
  await p.click('#fsBtn'); await p.waitForTimeout(400);
  const saved = await p.evaluate(()=>JSON.parse(localStorage.getItem('suneung-vocab-v2')||'{}').f);
  ok('글자 크기가 저장된다', saved!==undefined, 'f='+saved);
  await p.reload(); await p.waitForTimeout(700);
  ok('새로고침해도 유지된다', Math.abs(await size() - big) < 0.5, String(await size()));
  ok('탭 바 글씨는 커지지 않는다',
     Math.abs(await p.evaluate(()=>parseFloat(getComputedStyle(document.querySelector('.foot .seg button')).fontSize)) - 12) < 0.6);

  // ── C5 부록 시험 타임어택 ──
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(350);
  await p.locator('[data-asrc="conn"]').first().click(); await p.waitForTimeout(250);
  ok('시험 메뉴에 타임어택 칩이 있다', (await p.locator('#atTimer').count())===1);
  ok('기본은 꺼짐', (await p.locator('#atTimer').textContent()).includes('꺼짐'));
  await p.click('#atTimer'); await p.waitForTimeout(250);
  ok('켜진다', (await p.locator('#atTimer').textContent()).includes('켜짐'));
  await p.locator('[data-apart="word"]').click(); await p.waitForTimeout(300);
  ok('시험 화면에 시간 막대가 뜬다', (await p.locator('#atfill').count())===1);
  const t1 = await p.locator('#atnum').textContent();
  await p.waitForTimeout(1600);
  const t2 = await p.locator('#atnum').textContent();
  ok('시간이 줄어든다', +t2 < +t1, `${t1} → ${t2}`);
  const w0 = await p.evaluate(()=>at.wrong.length);
  await p.waitForTimeout(8000);                       // 단어 파트 제한 8초
  const w1 = await p.evaluate(()=>at.wrong.length);
  ok('시간이 다 되면 오답 처리된다', w1 === w0+1, `${w0} → ${w1}`);
  ok('시간 초과 뒤 다음 문제 버튼이 보인다', await p.locator('[data-anext]').isVisible());
  await p.locator('[data-anext]').click(); await p.waitForTimeout(300);
  ok('다음 문제에서 타이머가 다시 돈다', (await p.locator('#atfill').count())===1);
  // 답을 고르면 멈추는지
  await p.locator('[data-aopt]').first().click(); await p.waitForTimeout(300);
  ok('답을 고르면 타이머가 사라진다', (await p.locator('#atfill').count())===0);
  await p.click('button[data-mode="list"]'); await p.waitForTimeout(300);
  ok('시험을 나가면 타이머가 멈춘다', await p.evaluate(()=>atT===null));

  // ── C4 새 버전 알림 (file:// 에선 동작 안 함을 확인) ──
  ok('file:// 에서는 버전 확인이 조용히 넘어간다', (await p.locator('#updBar').count())===0);
  ok('JS 에러 없음', errs.length===0, errs[0]||'');
  console.log(fails?`실패 ${fails}건`:'전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
