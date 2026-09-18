# -*- coding: utf-8 -*-
"""부록 19(동명사·to부정사)를 DB에 넣는다. 이미 적용돼 있으면 아무것도 하지 않는다.

- apx 마지막에 그룹을 붙인다. 행에 sec(섹션), 그룹에 cz(개념 문항).
- 각 행을 단어장에도 편입한다. 표제어가 이미 있으면 예문만 보태고,
  없으면 맨 뒤 Day부터 40개씩 새로 붙인다.
- 기존 항목의 d(Day)는 절대 건드리지 않는다. 건드리면 외우던 묶음이 전부 뒤섞인다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db
_db.data_dir()
from apx19_rows import RAW
from apx19_cz import CZ

TITLE = "19. 동명사냐 to부정사냐 — 뒤에 오는 형태로 갈리는 자리"
SRC   = "부록 · 19. 동명사·to부정사"
TAG   = "준동사"
INTRO = ("동사 뒤에 ~ing를 쓸지 to V를 쓸지는 외워야 갈립니다. 크게 두 갈래예요. "
         "동명사는 이미 하고 있거나 끝난 일, to부정사는 아직 안 한 일을 가리킵니다. "
         "여기에 목적어가 끼면 형식까지 함께 봐야 하고, to가 전치사인 표현은 뒤에 반드시 ~ing가 옵니다. "
         "뜻이 갈리는 <b>④번 묶음과 전치사 to인 ⑦번 묶음</b>이 가장 많이 나옵니다.")

def main():
    src, m, DB = _db.load()
    if any(g['t'].startswith('19.') for g in DB['apx']):
        return print('이미 적용돼 있다. 아무것도 하지 않는다.')

    rows = []
    for sec, e, mm, n, x, xt, u in RAW:
        assert x.count(u) == 1, '밑줄 구간이 예문에 정확히 한 번 나와야 한다: %s' % e
        rows.append({"e": e, "m": mm, "n": n, "s": "추가", "x": x, "xt": xt,
                     "xh": x.replace(u, "<u>%s</u>" % u, 1), "sec": sec})
    DB['apx'].append({"t": TITLE, "g": INTRO, "r": rows,
                      "f": "form", "cz": _db.pack_cz(CZ)})

    by_w = {it['w'].lower(): it for it in DB['items']}
    merged, added = [], []
    for r in rows:
        ex = {"ch": r['xh'], "tr": r['xt'], "s": SRC}
        hit = by_w.get(r['e'].lower())
        if hit:
            if not any(e['ch'] == ex['ch'] for e in hit['ex']): hit['ex'].append(ex)
            for k, v in (('t', TAG), ('t', '부록'), ('es', '부록'), ('as', '부록')):
                if v not in hit[k]: hit[k].append(v)
            merged.append(r['e'])
        else:
            added.append({"w": r['e'], "p": "phr", "m": r['m'], "ex": [ex], "s": SRC,
                          "t": ["부록", TAG], "es": ["부록"], "as": ["부록"]})

    day = DB['days']
    used = sum(1 for it in DB['items'] if it['d'] == day)
    for it in added:
        if used >= 40: day += 1; used = 0
        it['d'] = day; used += 1
        it['i'] = len(DB['items'])
        DB['items'].append(it)
    DB['days'] = day

    _db.save(src, m, DB)
    print('부록 19: %d행 / 단어장 예문 병합 %d건, 신규 %d건 / Day -> %d'
          % (len(rows), len(merged), len(added), DB['days']))

main()
