const { chromium } = require('playwright');
const path = require('path');
const APP = 'file://' + path.join(__dirname, '..', '..', 'index.html');
let fails=0; const ok=(n,c,x)=>{console.log((c?'  통과  ':'  실패  ')+n+(x?'   '+x:''));if(!c)fails++;};
// 음성 목록을 심어 기기 상황을 흉내낸다
const fake = list => `
  Object.defineProperty(window.speechSynthesis,'getVoices',{configurable:true,
    value:()=>(${JSON.stringify(list)})});
`;
(async () => {
  const b = await chromium.launch({executablePath:'/opt/pw-browsers/chromium-1194/chrome-linux/chrome'});

  // ① 영어 음성이 전혀 없는 기기 (예전 사고가 나던 상황)
  let p = await b.newPage({viewport:{width:390,height:844}});
  const errs=[]; p.on('pageerror',e=>errs.push(String(e)));
  await p.addInitScript(fake([{name:'Yuna',lang:'ko-KR',default:true}]));
  await p.goto(APP); await p.waitForTimeout(800);
  ok('한국어 음성만 있으면 발음 버튼이 아예 없다', (await p.locator('.say').count())===0);
  ok('그래도 앱은 멀쩡히 뜬다', (await p.locator('tr.row').count())>10);
  const spoke = await p.evaluate(()=>{ let said=[];
    speechSynthesis.speak = u=>said.push(u.text); speak('announce'); return said; });
  ok('speak()를 불러도 한국어 음성으로 읽지 않는다', spoke.length===0, JSON.stringify(spoke));
  await p.close();

  // ② 영어 음성이 있는 기기
  p = await b.newPage({viewport:{width:390,height:844}});
  p.on('pageerror',e=>errs.push(String(e)));
  await p.addInitScript(fake([
    {name:'Yuna',lang:'ko-KR',default:true},
    {name:'Daniel',lang:'en-GB'},
    {name:'Samantha',lang:'en-US'},
  ]));
  await p.goto(APP); await p.waitForTimeout(800);
  ok('영어 음성이 있으면 발음 버튼이 생긴다', (await p.locator('.say').count())>10);
  const v = await p.evaluate(()=>({name:enVoice.name, lang:enVoice.lang}));
  ok('미국 영어를 고른다', v.lang==='en-US', JSON.stringify(v));
  // 실제로 읽히는 문자열
  const said = await p.evaluate(()=>{ const out=[];
    speechSynthesis.speak = u=>out.push({text:u.text, voice:u.lang, rate:u.rate});
    ['announce','enjoy ~ing','little (셀 수 없는 명사)','prevent / stop / keep A from -ing']
      .forEach(w=>speak(w)); return out; });
  console.log('   읽히는 문자열:'); said.forEach(x=>console.log('     ', JSON.stringify(x.text), x.voice, 'rate '+x.rate));
  ok('한글·기호를 걷어내고 읽는다', said.every(x=>/^[A-Za-z][A-Za-z '.,!?]*$/.test(x.text)));
  ok('영어 음성으로만 읽는다', said.every(x=>/^en/.test(x.voice)));
  // 버튼 클릭으로도 되는지
  const clicked = await p.evaluate(()=>{ const out=[];
    speechSynthesis.speak = u=>out.push(u.text);
    document.querySelector('.say').click(); return out; });
  ok('버튼을 누르면 읽는다', clicked.length===1, JSON.stringify(clicked));
  ok('JS 에러 없음', errs.length===0, errs[0]||'');
  await p.close();

  // ③ 음성이 늦게 올라오는 기기 (아이폰이 그렇다)
  p = await b.newPage({viewport:{width:390,height:844}});
  await p.addInitScript(`
    window.__late = [];   // init script는 함수로 감싸이므로 전역에 둔다
    Object.defineProperty(window.speechSynthesis,'getVoices',{configurable:true,
      value:()=>window.__late});
    window.__voicesUp = () => {                 // 타이머 대신 테스트가 직접 올린다
      window.__late = [{name:'Samantha',lang:'en-US',default:true}];
      if(speechSynthesis.onvoiceschanged) speechSynthesis.onvoiceschanged();
    };
  `);
  await p.goto(APP); await p.waitForTimeout(300);
  const before = await p.locator('.say').count();
  await p.evaluate(() => window.__voicesUp());
  await p.waitForTimeout(400);
  ok('음성이 늦게 올라와도 버튼이 나타난다', before===0 && (await p.locator('.say').count())>10,
     `처음 ${before} → 나중 ${await p.locator('.say').count()}`);
  await p.close();

  console.log(fails?`실패 ${fails}건`:'전부 통과');
  await b.close(); process.exit(fails?1:0);
})();
