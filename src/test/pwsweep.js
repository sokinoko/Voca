const { chromium } = require('playwright');
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');   // 저장소의 index.html

const modes = [['list','목록'],['card','카드'],['quiz','시험'],['poly','반복'],['apx','부록'],['sheet','시험지']];
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});
  for (const [file,label] of [['/tmp/claude-0/-home-user/54e5fadb-c51c-5a6f-95be-5e2afe2b608a/scratchpad/base3.html','수정 전'],
                              [require('path').join(__dirname,'..','..','index.html'),'수정 후']]) {
    const p = await b.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:1 });
    const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
    await p.goto('file://'+file); await p.waitForTimeout(700);
    console.log('\n===== ' + label + ' =====');
    console.log('헤더 부제:', JSON.stringify(await p.textContent('h1 em')));
    for (const [m,name] of modes){
      const btn = await p.$(`button[data-mode="${m}"]`);
      if(!btn){ console.log('  ', name, '→ 탭 없음'); continue; }
      await btn.click(); await p.waitForTimeout(350);
      const r = await p.evaluate(()=>({
        가로넘침: document.documentElement.scrollWidth > window.innerWidth,
        scrollW: document.documentElement.scrollWidth,
        넘친요소: [...document.querySelectorAll('body *')]
          .filter(e=>e.getBoundingClientRect().right > window.innerWidth + 1)
          .slice(0,3).map(e=>e.tagName+'.'+(e.className||'').toString().slice(0,20))
      }));
      console.log('  ', name.padEnd(4), '가로넘침:', r.가로넘침, '(폭', r.scrollW+')', r.넘친요소.length?('← '+r.넘친요소.join(', ')):'');
    }
    console.log('  JS 에러:', errs.length?errs:'없음');
    await p.close();
  }
  await b.close();
})();
