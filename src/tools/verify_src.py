# -*- coding: utf-8 -*-
"""단어장에 든 예문이 정말 그 시험 그 문항 본문에 있는지 검사한다.

출처를 지어내지 않는다는 규칙을 기계로 지키기 위한 것이다. 시험 하나를
넣고 나면 돌려서 어긋난 예문이 없는지 본다.

  python3 src/tools/verify_src.py "26 9모" <대본.pdf> <문제지.pdf>
"""
import io, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdftext as P

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRP = {16:[15,16,17], 17:[15,16,17], 41:[40,41,42], 42:[40,41,42],
       43:[42,43,44,45], 44:[42,43,44,45], 45:[42,43,44,45]}
norm = lambda s: re.sub(r'\s+', ' ', s)

def load_exam(scr_pdf, mun_pdf):
    T = {'scr': P.clean('\n'.join(P.pages(scr_pdf))).replace('’', "'"),
         'mun': P.clean('\n'.join(P.pages(mun_pdf))).replace('’', "'")}
    return T, {k: P.question_spans(T[k]) for k in T}

def main(exam, scr_pdf, mun_pdf):
    T, SPAN = load_exam(scr_pdf, mun_pdf)
    def scope(k, no):
        return ' '.join(T[k][a:b] for n in GRP.get(no, [no]) if n in SPAN[k]
                        for a, b in [SPAN[k][n]])
    DB = json.loads(re.search(r'const DB = (\{.*?\});\n',
          io.open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read(), re.S).group(1))
    pat = re.compile(r'^' + re.escape(exam) + r'\s+(?:듣기\s*)?(\d+)번')
    n = 0; bad = []
    for it in DB['items']:
        for ex in it['ex']:
            m = pat.match(ex['s'])
            if not m: continue
            n += 1
            no = int(m.group(1))
            ch = re.sub(r'</?u>', '', ex['ch'])
            # 듣기 문항이라도 선택지는 시험지에 인쇄돼 있다. 양쪽 다 본다.
            if not any(norm(ch) in norm(scope(k, no)) for k in ('scr', 'mun')):
                bad.append((it['w'], ex['s'], ch[:64]))
    print('%s 예문 %d개 검사 — 어긋남 %d건' % (exam, n, len(bad)))
    for b in bad: print('  %-24s %-16s %s' % b)
    return 1 if bad else 0

sys.exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
