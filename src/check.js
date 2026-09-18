#!/usr/bin/env node
/* index.html 한 파일을 검사한다. 의존성 없음.
     node src/check.js
   브라우저가 없으므로 최소한의 스텁을 물려 뷰 함수와 시험 문항 생성기를 직접 부른다. */
const fs = require('fs'), path = require('path');
const HTML = path.join(__dirname, '..', 'index.html');
const src = fs.readFileSync(HTML, 'utf8');

let fails = 0;
const ok = (name, cond, note) => {
  console.log((cond ? '  통과  ' : '  실패  ') + name + (note ? '   ' + note : ''));
  if (!cond) fails++;
};

/* ── 1. 데이터 ── */
const DB = JSON.parse(src.match(/const DB = (\{.*?\});\n/s)[1]);
const rows = DB.apx.reduce((a, g) => a + g.r.length, 0);
console.log(`\n데이터 — 단어 ${DB.items.length} · Day ${DB.days} · 부록 ${DB.apx.length}묶음 ${rows}행\n`);

ok('items의 i가 인덱스와 맞는다', DB.items.every((x, n) => x.i === n));
const keys = DB.items.map(x => x.w.toLowerCase());
ok('저장 키가 겹치지 않는다', keys.length === new Set(keys).size);
ok('Day가 1..days 안에 있다', DB.items.every(x => x.d >= 1 && x.d <= DB.days));
ok('부록 행에 밑줄이 있다', DB.apx.every(g => g.r.every(r => /<u/.test(r.xh))));
const noMark = DB.items.filter(x => !x.ex.some(e => e.ch.includes('<u>'))).length;
ok('예문 밑줄 실패가 7건을 넘지 않는다', noMark <= 7, `(${noMark}건)`);
ok('외부 URL 참조가 없다', !/https?:\/\/(?!claude\.ai)/.test(src.replace(/<!--[\s\S]*?-->/g, '')));

/* ── 2. 뷰와 시험 ── */
const stub = { innerHTML:'', textContent:'', style:{}, setAttribute(){}, focus(){},
  setSelectionRange(){}, parentElement:{style:{}},
  classList:{add(){}, remove(){}, toggle(){}} };
global.window = { print(){}, addEventListener(){}, removeEventListener(){} };
global.panel = stub;
['mDone','mAll','mStar','mBar','mLabel'].forEach(k => global[k] = stub);
global.document = { addEventListener(){}, getElementById:()=>stub, querySelector:()=>stub,
  querySelectorAll:()=>[], createElement:()=>stub, body:{ classList:{add(){},remove(){}}, appendChild(){} } };
global.localStorage = { getItem:()=>null, setItem(){} };
global.setInterval = ()=>1; global.clearInterval = ()=>{}; global.setTimeout = ()=>0;
global.navigator = {};

const js = src.split('<script>')[1].split('</' + 'script>')[0];
const tmp = path.join(require('os').tmpdir(), 'voca-check-' + process.pid + '.js');
fs.writeFileSync(tmp, js.replace('load().then(render);', '').split("document.addEventListener('click'")[0]
  + '\nmodule.exports={DB,czOf,wqOf,connGroup,gramGroup,prepGroup,asGroup,filtered,'
  + 'viewList,viewCard,viewQuiz,viewApx,viewPoly,viewSheet};');
const m = require(tmp);
fs.unlinkSync(tmp);

const list = m.filtered();
ok('여섯 화면이 그려진다',
   [m.viewList, m.viewCard, m.viewQuiz, m.viewApx, m.viewPoly, m.viewSheet]
     .every(f => f(list).length > 100));

const units = DB.apx.map(g => [g.t, g])
  .concat([['접속사 통합', m.connGroup()], ['문형표', m.gramGroup()],
           ['전치사 지도', m.prepGroup()], ['as', m.asGroup()]]);
let cz = 0, wq = 0, bad = [];
for (let run = 0; run < 5; run++) units.forEach(([t, g]) => {
  const c = m.czOf(g), w = m.wqOf(g);
  if (!run) { cz += c.length; wq += w.length; }
  // 연결사 묶음은 개념 시험을 일부러 두지 않는다. 한 문장짜리 빈칸은 답이
  // 하나로 정해지지 않아서, 지문이 붙은 문항을 「접속사 통합」에 모아 두었다.
  if (!c.length && g.f !== 'conn') bad.push(t + ' 개념 0문항');
  if (!w.length) bad.push(t + ' 단어 0문항');
  c.forEach(q => q.b.forEach(b => {
    if (b.a < 0) bad.push(t + ' 정답 없음');
    if (b.o.length < 2) bad.push(t + ' 보기 1개');
    if (b.o.some(x => !String(x).trim())) bad.push(t + ' 빈 보기');
    if (new Set(b.o.map(x => String(x).toLowerCase())).size !== b.o.length)
      bad.push(t + ' 보기 중복 ' + JSON.stringify(b.o));
  }));
});
ok(`부록 ${units.length}곳 모두 시험이 만들어진다`, !bad.length,
   bad.length ? bad.slice(0, 3).join(' / ') : `(개념 ${cz} · 단어 ${wq}문항)`);

console.log(fails ? `\n실패 ${fails}건\n` : '\n전부 통과\n');
process.exit(fails ? 1 : 0);
