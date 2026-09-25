const { chromium } = require('playwright');
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');   // 저장소의 index.html

let fails=0; const ok=(n,c,x)=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:''));if(!c)fails++;};
async function swipe(p, dx, dy=0){          // 터치 손짓 흉내
  const box = await p.locator('#panel .card').boundingBox();
  const x = box.x + box.width/2, y = box.y + box.height/2;
  await p.evaluate(({x,y,dx,dy})=>{
    const mk=(t,cx,cy)=>{ const tch=new Touch({identifier:1,target:document.querySelector('#panel .card'),clientX:cx,clientY:cy});
      return new TouchEvent(t,{touches:t==='touchend'?[]:[tch],changedTouches:[tch],bubbles:true,cancelable:true}); };
    const el=document.querySelector('#panel .card');
    el.dispatchEvent(mk('touchstart',x,y));
    el.dispatchEvent(mk('touchmove',x+dx/2,y+dy/2));
    el.dispatchEvent(mk('touchmove',x+dx,y+dy));
    el.dispatchEvent(mk('touchend',x+dx,y+dy));
  },{x,y,dx,dy});
  await p.waitForTimeout(250);
}
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({ viewport:{width:390,height:844}, hasTouch:true });
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.goto(APP); await p.waitForTimeout(700);
  await p.click('button[data-mode="card"]'); await p.waitForTimeout(400);
  ok('카드 화면에 안내가 있다', (await p.locator('.swhint').count())===1);

  // 뜻을 안 본 상태에서 밀면 먼저 뒤집힌다
  ok('처음엔 뜻이 가려져 있다', await p.evaluate(()=>!shown));
  await swipe(p, 120);
  ok('밀면 먼저 뜻이 열린다', await p.evaluate(()=>shown));
  const i0 = await p.evaluate(()=>ses.i);
  ok('뒤집기만 하고 넘어가지는 않는다', (await p.evaluate(()=>ses.i))===i0);

  // 오른쪽 = 외웠어요
  const w0 = await p.evaluate(()=>[ses.right, ses.wrong.length, ses.i]);
  await swipe(p, 130);
  const w1 = await p.evaluate(()=>[ses.right, ses.wrong.length, ses.i]);
  ok('오른쪽으로 밀면 외운 것으로 센다', w1[0]===w0[0]+1 && w1[2]===w0[2]+1, JSON.stringify(w1));

  // 왼쪽 = 모르겠어요 (오답 누적도)
  await swipe(p, 120);                        // 먼저 뒤집기
  const m0 = await p.evaluate(()=>Object.keys(miss).length);
  const l0 = await p.evaluate(()=>[ses.wrong.length, ses.i]);
  await swipe(p, -130);
  const l1 = await p.evaluate(()=>[ses.wrong.length, ses.i]);
  ok('왼쪽으로 밀면 틀린 것으로 센다', l1[0]===l0[0]+1 && l1[1]===l0[1]+1, JSON.stringify(l1));
  ok('스와이프 오답도 누적에 쌓인다', (await p.evaluate(()=>Object.keys(miss).length))===m0+1);

  // 살짝 스친 것은 무시
  await swipe(p, 120);
  const s0 = await p.evaluate(()=>ses.i);
  await swipe(p, 30);
  ok('살짝 스친 것은 무시한다', (await p.evaluate(()=>ses.i))===s0);

  // 세로로 긁으면 스와이프로 보지 않는다
  const v0 = await p.evaluate(()=>ses.i);
  await swipe(p, 100, 160);
  ok('세로로 긁으면 넘어가지 않는다', (await p.evaluate(()=>ses.i))===v0);
  ok('카드가 제자리로 돌아온다',
     !(await p.evaluate(()=>document.querySelector('#panel .card').style.transform)));

  // 다른 화면에서는 작동하지 않는다
  await p.click('button[data-mode="apx"]'); await p.waitForTimeout(350);
  ok('부록 화면에선 스와이프가 없다', (await p.locator('#panel .card').count())===0);
  ok('JS 에러 없음', errs.length===0, errs[0]||'');
  console.log(fails?`실패 ${fails}건`:'전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
