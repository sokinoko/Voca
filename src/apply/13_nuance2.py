# -*- coding: utf-8 -*-
"""부록 17(뉘앙스) 2차분을 DB에 넣는다.

 - 새 행 7개를 부록 17에 보탠다 (새 묶음을 만들지 않는다 — 성격이 같다)
 - 이미 있는 행 3개(pitch, at the expense of, end)는 독해포인트만 보강한다
 - 단어장에는 기존 표제어에 예문을 보태고, 없는 것만 맨 뒤 Day에 새로 만든다

몇 번을 돌려도 결과가 같다. 이미 들어가 있으면 건너뛴다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db
_db.data_dir()
from nuance2 import ROWS, MORE, MERGE, WIDEN, FRESH

NUM = '17'
SRC = '추가'                      # 예문이 평가원 본문 그대로가 아니다 → 지어내지 않는다


def group(DB):
    for g in DB['apx']:
        if g['t'].split('.')[0] == NUM:
            return g
    raise SystemExit('부록 %s 묶음을 찾지 못했다' % NUM)


def main():
    src, m, DB = _db.load()
    g = group(DB)
    label = '부록 · ' + g['t']
    have = {r['e'] for r in g['r']}

    added = 0
    for e, mean, note, x, xt, xh in ROWS:
        assert xh.replace('<u>', '').replace('</u>', '') == x, '밑줄과 예문이 어긋난다: %s' % e
        row = {'e': e, 'm': mean, 'n': note, 's': SRC, 'x': x, 'xt': xt, 'xh': xh}
        if e in have:
            for i, r in enumerate(g['r']):
                if r['e'] == e:
                    g['r'][i] = row
        else:
            g['r'].append(row)
            added += 1

    bumped = 0
    for e, extra in MORE.items():
        hit = [r for r in g['r'] if r['e'] == e]
        if not hit:
            raise SystemExit('보강할 행이 없다: %s' % e)
        r = hit[0]
        if extra not in r['n']:
            r['n'] = r['n'] + ' · ' + extra
            bumped += 1

    idx = {it['w'].lower(): it for it in DB['items']}
    merged = fresh = 0

    for e, mean, note, x, xt, xh in ROWS:
        ex = {'ch': xh, 'tr': xt, 's': label}
        w = MERGE.get(e)
        if w:
            it = idx[w.lower()]
            if not any(q['ch'] == xh for q in it['ex']):
                it['ex'].append(ex)
                merged += 1
            for tag in ('부록', '뉘앙스'):
                if tag not in it['t']:
                    it['t'].append(tag)
            if label not in it['s']:
                it['s'] = it['s'] + ' · ' + label
            for key in ('es', 'as'):
                if '부록' not in it[key]:
                    it[key].append('부록')
            if w in WIDEN:
                it['m'] = WIDEN[w]
        elif e in FRESH:
            if e.lower() in idx:
                continue
            it = {'i': len(DB['items']), 'w': e, 'p': FRESH[e], 'm': mean, 's': label,
                  't': ['부록', '뉘앙스', '다의어'], 'ex': [ex],
                  'es': ['부록'], 'as': ['부록'], 'd': DB['days']}
            DB['items'].append(it)
            idx[e.lower()] = it
            fresh += 1
        else:
            raise SystemExit('MERGE에도 FRESH에도 없는 행: %s' % e)

    _db.save(src, m, DB)
    print('부록 %s — 행 %d개 (새로 %d개, 보강 %d개)' % (NUM, len(g['r']), added, bumped))
    print('단어장 — 예문 보탠 항목 %d개, 새 항목 %d개 (Day %d), 전체 %d개'
          % (merged, fresh, DB['days'], len(DB['items'])))


main()
