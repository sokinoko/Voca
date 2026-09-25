# -*- coding: utf-8 -*-
"""또 나온 낱말에 예문을 하나 더 단다.

새 항목을 만들지 않는다. 이미 있는 낱말 밑에 그 시험의 예문을 붙이고,
시험 라벨(es)과 영역(as)을 보탠다. 이미 외운 뜻과 다른 뜻으로 나왔으면
뜻(m)에도 그 뜻을 덧붙인다 — 같은 뜻을 두 번 적지는 않는다.

저장 키는 낱말 문자열이라 예문을 보태도 학습 기록은 그대로다.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db
_db.data_dir()
from y26_6_again import R as R6
from y26_9_again import R as R9

SETS = [('26 6모', R6), ('26 9모', R9)]

def main():
    s, m, DB = _db.load()
    by = {it['w'].lower(): it for it in DB['items']}
    n_ex = n_m = n_skip = 0
    for exam, rows in SETS:
        for e, no, x, u, tr, add in rows:
            it = by.get(e.lower())
            assert it, '단어장에 없는 낱말: %s' % e
            assert x.count(u) == 1, '밑줄 구간이 예문에 한 번 나와야 한다: %s' % e
            src = '%s %s' % (exam, ('듣기 %d번' % no) if no <= 17 else ('%d번' % no))
            if any(ex['s'] == src and ex['ch'].replace('<u>', '').replace('</u>', '') == x
                   for ex in it['ex']):
                n_skip += 1; continue
            it['ex'].append({'ch': x.replace(u, '<u>%s</u>' % u, 1), 'tr': tr, 's': src})
            n_ex += 1
            if exam not in it['es']: it['es'].append(exam)
            area = '듣기' if no <= 17 else '독해'
            if area not in it['as']: it['as'].append(area)
            if add and add not in it['m']:
                it['m'] = it['m'] + ' / ' + add; n_m += 1
    if not n_ex:
        return print('이미 다 붙어 있다.')
    _db.save(s, m, DB)
    print('예문 %d개를 기존 낱말 밑에 붙였다 (건너뜀 %d) · 뜻을 보탠 낱말 %d개' % (n_ex, n_skip, n_m))
    cnt = {}
    for it in DB['items']: cnt[len(it['ex'])] = cnt.get(len(it['ex']), 0) + 1
    print('예문 개수 분포:', sorted(cnt.items()))

main()
