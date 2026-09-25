const fs = require('fs');
const s = fs.readFileSync(require('path').join(__dirname,'..','..','index.html'), 'utf8');

// ── DOM 스텁: 클릭 리스너를 붙잡아 직접 호출한다 ──
let clickFn = null;
const bodyCls = new Set();
let printed = 0;
const winListeners = {};

const stub = {innerHTML:'', textContent:'', style:{},
  classList:{add(){},remove(){},toggle(){}},
  setAttribute(){}, focus(){}, setSelectionRange(){}, parentElement:{style:{}}};

global.window = {
  print(){ printed++; },
  addEventListener(k,f){ (winListeners[k] = winListeners[k]||[]).push(f); },
  removeEventListener(k,f){ if(winListeners[k]) winListeners[k] = winListeners[k].filter(x=>x!==f); },
};
global.panel = stub;
['mDone','mAll','mStar','mBar','mLabel'].forEach(k => global[k] = stub);
global.document = {
  addEventListener(type, fn){ if(type==='click') clickFn = fn; },
  getElementById(){ return stub }, querySelector(){ return stub },
  querySelectorAll(){ return [] },
  body:{ classList:{ add(c){bodyCls.add(c)}, remove(...c){c.forEach(x=>bodyCls.delete(x))} } },
};
global.localStorage = { getItem(){return null}, setItem(){} };
global.setInterval = () => 1; global.clearInterval = () => {};
const timers = [];
global.setTimeout = (f) => { timers.push(f); return 0; };
global.navigator = {};

const js = s.split('<script>')[1].split('</' + 'script>')[0];
fs.writeFileSync('/tmp/t2.js', js.replace('load().then(render);','')
  + "\nmodule.exports={render,viewSheet,filtered,state,get sheetNo(){return sheetNo},get sheet(){return sheet}};");
const m = require('/tmp/t2.js');

// 버튼 클릭을 흉내낸다
function click(action){
  const el = { dataset:{ sheet: action }, hasAttribute:()=>false,
               classList:{toggle(){},add(){},remove(){}}, setAttribute(){} };
  clickFn({ target: { closest: () => el } });
}

let fail = 0;
const ok = (name, cond) => { console.log((cond?'  통과  ':'  실패  ') + name); if(!cond) fail++; };

ok('클릭 리스너 등록됨', typeof clickFn === 'function');

m.state.mode = 'sheet';
m.render();
const total = Math.ceil(m.sheet.w.length/40);
console.log(`\n세트 총 ${total}개 (단어 ${m.sheet.w.length}개)\n`);

// 1) 다음 / 이전
ok('시작 세트 0', m.sheetNo === 0);
click('next');  ok('다음 → 1', m.sheetNo === 1);
click('next');  ok('다음 → 2', m.sheetNo === 2);
click('prev');  ok('이전 → 1', m.sheetNo === 1);
click('prev');  click('prev');
ok('첫 세트에서 이전 → 마지막으로 순환 (' + m.sheetNo + ')', m.sheetNo === total - 1);
click('next');  ok('마지막에서 다음 → 0으로 순환', m.sheetNo === 0);

// 2) 다시 섞기
const before = m.sheet.w.slice(0, 40).join(',');
click('next');
click('shuffle');
ok('다시 섞기 → 세트 0으로', m.sheetNo === 0);
ok('다시 섞기 → 문항 순서 바뀜', m.sheet.w.slice(0,40).join(',') !== before);

// 3) 인쇄 3종
printed = 0; bodyCls.clear();
click('printq');
ok('시험지만 → window.print() 호출', printed === 1);
ok('시험지만 → body.pq 부착', bodyCls.has('pq') && !bodyCls.has('pa'));
timers.forEach(f=>f()); timers.length = 0;
ok('인쇄 후 body 클래스 정리', bodyCls.size === 0);

printed = 0; bodyCls.clear();
click('printa');
ok('정답지만 → window.print() 호출', printed === 1);
ok('정답지만 → body.pa 부착', bodyCls.has('pa') && !bodyCls.has('pq'));
(winListeners.afterprint||[]).slice().forEach(f=>f());
ok('afterprint → body 클래스 정리', bodyCls.size === 0);
ok('afterprint 리스너는 하나뿐', (winListeners.afterprint||[]).length === 1);

printed = 0; bodyCls.clear();
click('printall');
ok('둘 다 → window.print() 호출', printed === 1);
ok('둘 다 → body 클래스 없음(전체 인쇄)', bodyCls.size === 0);
timers.forEach(f=>f()); timers.length = 0;

// 4) 인쇄가 막힌 환경(홈 화면 앱)에서도 죽지 않아야 한다
delete global.window.print;
let threw = false;
try { click('printq'); } catch(e) { threw = true; }
ok('window.print 없어도 예외 없음', !threw);

console.log(fail ? `\n실패 ${fail}건` : '\n전부 통과');
process.exit(fail ? 1 : 0);
