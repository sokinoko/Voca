const { chromium } = require('playwright');
// 스크린샷은 저장소에 남기지 않는다
const SHOT = n => require('path').join(require('os').tmpdir(), 'voca-' + n);
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');   // 저장소의 index.html

let fails=0; const ok=(n,c,x)=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:''));if(!c)fails++;};
const lum = c => { const [r,g,b]=c.match(/\d+/g).map(Number).slice(0,3).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4);}); return .2126*r+.7152*g+.0722*b; };
const ratio = (a,b) => { const [x,y]=[lum(a),lum(b)].sort((p,q)=>q-p); return (x+.05)/(y+.05); };
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  for (const scheme of ['light','dark']){
    const p = await b.newPage({ viewport:{width:390,height:844}, colorScheme:scheme, deviceScaleFactor:2 });
    const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
    await p.goto(APP); await p.waitForTimeout(700);
    const c = await p.evaluate(()=>{
      const g=e=>getComputedStyle(e);
      return { bg:g(document.body).backgroundColor, fg:g(document.body).color,
               word:g(document.querySelector('.word')).color,
               mask:g(document.querySelector('.mask')).backgroundColor,
               src:g(document.querySelector('.src')).color };
    });
    console.log(`\n【${scheme}】 배경 ${c.bg} / 글자 ${c.fg}`);
    ok(`${scheme}: 본문 대비비 4.5 이상`, ratio(c.fg,c.bg)>=4.5, ratio(c.fg,c.bg).toFixed(2));
    ok(`${scheme}: 표제어 대비비 4.5 이상`, ratio(c.word,c.bg)>=4.5, ratio(c.word,c.bg).toFixed(2));
    ok(`${scheme}: 출처 글씨 대비비 3 이상`, ratio(c.src,c.bg)>=3, ratio(c.src,c.bg).toFixed(2));
    ok(`${scheme}: 가림판이 배경과 구분된다`, ratio(c.mask,c.bg)>=1.1, ratio(c.mask,c.bg).toFixed(2));
    await p.screenshot({path: SHOT(`theme-${scheme}.png`)});
    // 인쇄는 언제나 밝게
    await p.emulateMedia({media:'print'});
    const pr = await p.evaluate(()=>getComputedStyle(document.body).backgroundColor);
    ok(`${scheme}: 인쇄는 흰 배경`, /255,\s*255,\s*255/.test(pr), pr);
    await p.emulateMedia({media:'screen'});
    // 시험 화면 정오답 색도 보이는지
    await p.click('button[data-mode="apx"]'); await p.waitForTimeout(350);
    await p.locator('[data-asrc="conn"]').first().click(); await p.waitForTimeout(250);
    await p.locator('[data-apart="concept"]').click(); await p.waitForTimeout(250);
    await p.locator('[data-cz]').first().click(); await p.waitForTimeout(250);
    const mark = await p.evaluate(()=>{
      const r=document.querySelector('.czo.right'), w=document.querySelector('.czo.wrong');
      const g=e=>e?getComputedStyle(e):null;
      return { right:r?g(r).color:null, rbg:r?g(r).backgroundColor:null,
               wrong:w?g(w).color:null };
    });
    if(mark.right) ok(`${scheme}: 정답 표시 대비비 3 이상`, ratio(mark.right,mark.rbg)>=3, ratio(mark.right,mark.rbg).toFixed(2));
    ok(`${scheme}: JS 에러 없음`, errs.length===0, errs[0]||'');
    await p.close();
  }
  console.log(fails?`\n실패 ${fails}건`:'\n전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
