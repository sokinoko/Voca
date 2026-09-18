const { chromium } = require('playwright');
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');   // 저장소의 index.html

const fs=require('fs'), path=require('path');
let fails=0; const ok=(n,c)=>{console.log((c?'  통과  ':'  실패  ')+n); if(!c)fails++;};
(async () => {
  const dl = '/tmp/claude-0/-home-user/54e5fadb-c51c-5a6f-95be-5e2afe2b608a/scratchpad/dl';
  fs.rmSync(dl,{recursive:true,force:true}); fs.mkdirSync(dl,{recursive:true});
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  const p = await b.newPage({ viewport:{width:390,height:844}, acceptDownloads:true });
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  // confirm이 뜨면 실패로 본다 (홈 화면 앱에서 막히는 방식)
  let sawDialog=false; p.on('dialog', async d=>{ sawDialog=true; await d.dismiss(); });
  await p.goto(APP); await p.waitForTimeout(700);
  const openRec = async () => {            // 기록 버튼은 평소 접혀 있다
    if(!(await p.locator('#reset').isVisible())){ await p.click('#recBtn'); await p.waitForTimeout(200); }
  };

  // 기록을 좀 만든다 — 3회독 점 찍고 별표
  for(let i=0;i<3;i++){ await p.locator('.dot').nth(i*3+2).click(); await p.waitForTimeout(80); }
  await p.locator('.star').first().click(); await p.waitForTimeout(150);
  const before = await p.evaluate(()=>({p:Object.keys(prog).length, s:Object.keys(star).length}));
  console.log('만든 기록:', JSON.stringify(before));
  ok('회독·별표가 기록됐다', before.p>0 && before.s>0);

  // ── A1 두 번 눌러야 지워진다 ──
  await openRec(); await p.click('#reset'); await p.waitForTimeout(200);
  ok('confirm 창이 뜨지 않는다', !sawDialog);
  ok('한 번 누르면 경고 상태', (await p.locator('#reset').textContent()).includes('한 번 더'));
  const mid = await p.evaluate(()=>Object.keys(prog).length);
  ok('한 번만 눌렀을 때는 안 지워진다', mid === before.p);

  // 5초 지나면 저절로 풀리는지
  await p.waitForTimeout(5300);
  ok('5초 뒤 저절로 풀린다', (await p.locator('#reset').textContent()) === '기록 초기화');
  const still = await p.evaluate(()=>Object.keys(prog).length);
  ok('풀린 뒤에도 기록 그대로', still === before.p);

  // ── A2 내보내기 ──
  await openRec();
  const [dlEv] = await Promise.all([ p.waitForEvent('download'), p.click('#expBtn') ]);
  const file = path.join(dl, dlEv.suggestedFilename());
  await dlEv.saveAs(file);
  const saved = JSON.parse(fs.readFileSync(file,'utf8'));
  console.log('내보낸 파일:', dlEv.suggestedFilename(), '| 키', Object.keys(saved).join(','));
  ok('백업 파일에 회독·별표가 들어 있다',
     Object.keys(saved.p).length===before.p && Object.keys(saved.s).length===before.s);
  ok('파일 이름 확인은 http 테스트에서 따로 한다', true);

  // ── 두 번 눌러 초기화 ──
  await openRec(); await p.click('#reset'); await p.waitForTimeout(150);
  await openRec(); await p.click('#reset'); await p.waitForTimeout(300);
  const after = await p.evaluate(()=>({p:Object.keys(prog).length, s:Object.keys(star).length}));
  ok('두 번 누르면 지워진다', after.p===0 && after.s===0);
  ok('지운 뒤 안내가 뜬다', (await p.locator('#reset').textContent()).includes('지웠'));

  // ── A2 가져오기로 되살리기 ──
  await p.waitForTimeout(2300);
  await openRec(); await p.setInputFiles('#impFile', file); await p.waitForTimeout(500);
  const back = await p.evaluate(()=>({p:Object.keys(prog).length, s:Object.keys(star).length}));
  console.log('되살린 기록:', JSON.stringify(back));
  ok('백업에서 그대로 되살아난다', back.p===before.p && back.s===before.s);
  ok('되살린 뒤 안내가 뜬다', (await p.locator('#impBtn').textContent()).includes('되살림'));

  // ── 이상한 파일은 거절 ──
  const junk = path.join(dl,'junk.json');
  fs.writeFileSync(junk, JSON.stringify({hello:'world'}));
  await p.setInputFiles('#impFile', junk); await p.waitForTimeout(400);
  ok('남의 파일은 거절한다', (await p.locator('#impBtn').textContent()).includes('아닙니다'));
  const keep = await p.evaluate(()=>Object.keys(prog).length);
  ok('거절해도 기존 기록은 그대로', keep===before.p);

  const broken = path.join(dl,'broken.json');
  fs.writeFileSync(broken, '{{{');
  await p.setInputFiles('#impFile', broken); await p.waitForTimeout(400);
  ok('깨진 파일도 앱이 죽지 않는다', errs.length===0);

  console.log('\nJS 에러:', errs.length?errs:'없음');
  console.log(fails?`실패 ${fails}건`:'전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
