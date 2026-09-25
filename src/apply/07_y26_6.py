# -*- coding: utf-8 -*-
"""2026학년도 6월 모의평가 단어를 단어장에 넣는다.

뒤쪽 Day부터 채운다. 기존 단어의 Day는 건드리지 않는다.
마지막 Day가 80개에 못 미치면 거기부터 채우고, 넘치면 새 Day를 연다.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db
_db.data_dir()
from y26_6 import R, POS
from wordfreq import zipf_frequency as z

SIZE, EXAM = 80, '26 6모'

def tags(e, no):
    ts = []
    w = [t for t in re.findall(r"[A-Za-z']+", e) if len(t) > 2]
    f = min([z(t.lower(), 'en') for t in w] or [9])
    ts.append('핵심' if f < 3.3 else '필수')
    if no <= 17: ts.append('듣기표현')
    return ts

def main():
    s, m, DB = _db.load()
    have = {it['w'].lower() for it in DB['items']}
    rows = [r for r in R if r[0].lower() not in have]
    if not rows:
        return print('이미 들어가 있다.')

    day = DB['days']
    used = sum(1 for it in DB['items'] if it['d'] == day)
    added = 0
    for e, mean, no, x, u, tr in rows:
        assert x.count(u) == 1, '밑줄 구간이 예문에 한 번 나와야 한다: %s' % e
        src = '%s %s' % (EXAM, ('듣기 %d번' % no) if no <= 17 else ('%d번' % no))
        if used >= SIZE:
            day += 1; used = 0
        DB['items'].append({
            'i': len(DB['items']), 'w': e, 'p': POS.get(e, 'n'),
            'm': mean, 's': src,
            'ex': [{'ch': x.replace(u, '<u>%s</u>' % u, 1), 'tr': tr, 's': src}],
            't': tags(e, no), 'es': [EXAM],
            'as': ['듣기'] if no <= 17 else ['독해'],
            'd': day,
        })
        used += 1; added += 1
    DB['days'] = day
    _db.save(s, m, DB)
    cnt = {}
    for it in DB['items']: cnt[it['d']] = cnt.get(it['d'], 0) + 1
    print('%s 단어 %d개 추가 (건너뜀 %d)' % (EXAM, added, len(R) - len(rows)))
    print('items %d개 · Day %d일' % (len(DB['items']), DB['days']))
    print('마지막 세 Day 인원:', {d: cnt[d] for d in sorted(cnt)[-3:]})

main()
