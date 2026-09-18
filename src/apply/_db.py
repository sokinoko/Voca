# -*- coding: utf-8 -*-
"""index.html 안의 const DB = {...} 를 읽고 쓰는 공통 도구.

이 앱은 빌드 파이프라인이 없다. index.html 한 파일이 소스이자 산출물이고,
데이터는 그 안의 DB 리터럴에 들어 있다. 고칠 때는 여기 함수로 읽어
파이썬에서 고친 뒤 다시 써넣는다. html을 손으로 편집하지 않는다.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HTML = os.path.join(ROOT, 'index.html')
PAT  = re.compile(r'const DB = (\{.*?\});\n', re.S)

def data_dir():
    d = os.path.join(ROOT, 'src', 'data')
    if d not in sys.path: sys.path.insert(0, d)
    return d

def load():
    src = io.open(HTML, encoding='utf-8').read()
    m = PAT.search(src)
    if not m: raise SystemExit('index.html에서 DB를 찾지 못했다')
    return src, m, json.loads(m.group(1))

def save(src, m, DB):
    check(DB)
    out = src[:m.start(1)] + json.dumps(DB, ensure_ascii=False) + src[m.end(1):]
    io.open(HTML, 'w', encoding='utf-8').write(out)

def check(DB):
    """어떤 스크립트든 쓰기 전에 통과해야 하는 불변식."""
    items = DB['items']
    assert all(x['i'] == n for n, x in enumerate(items)), 'items의 i가 인덱스와 어긋난다'
    keys = [x['w'].lower() for x in items]
    assert len(keys) == len(set(keys)), '저장 키(w.toLowerCase())가 중복됐다'
    assert all(1 <= x['d'] <= DB['days'] for x in items), 'Day 범위를 벗어난 항목이 있다'
    for g in DB['apx']:
        for r in g['r']:
            assert '<u' in r['xh'], '밑줄 없는 부록 행: %s' % r['e']

def pack_cz(rows):
    """(문장, 해석, [(보기, 정답인덱스)], 해설) → DB에 넣을 모양"""
    return [{"s": s, "tr": tr, "n": n,
             "b": [{"o": list(o), "a": a} for o, a in bl]}
            for s, tr, bl, n in rows]
