# -*- coding: utf-8 -*-
"""26 6모·9모에서 더 뽑은 낱말을 넣는다. 뒤쪽 Day부터 채운다."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db
_db.data_dir()
from y26_more import R
from wordfreq import zipf_frequency as z

SIZE = 80

def tags(e, no, p):
    w = [t for t in re.findall(r"[A-Za-z']+", e) if len(t) > 2]
    f = min([z(t.lower(), 'en') for t in w] or [9])
    ts = ['핵심' if f < 3.3 else '필수']
    if no and no <= 17: ts.append('듣기표현')
    if p == 'phr': ts.append('구동사')
    return ts

def main():
    s, m, DB = _db.load()
    have = {it['w'].lower() for it in DB['items']}
    rows = [r for r in R if r[0].lower() not in have]
    if not rows:
        return print('이미 들어가 있다.')
    day = DB['days']
    used = sum(1 for it in DB['items'] if it['d'] == day)
    for e, mean, exam, no, x, u, tr, p in rows:
        assert x.count(u) == 1, '밑줄 구간이 예문에 한 번 나와야 한다: %s' % e
        # 문항이 0이면 시험지에 없는 표현이라 직접 쓴 예문이다 — 출처를 지어내지 않는다
        ex_src = '추가' if not no else '%s %s' % (exam, ('듣기 %d번' % no) if no <= 17 else ('%d번' % no))
        if used >= SIZE:
            day += 1; used = 0
        DB['items'].append({
            'i': len(DB['items']), 'w': e, 'p': p, 'm': mean,
            's': ex_src if no else exam,
            'ex': [{'ch': x.replace(u, '<u>%s</u>' % u, 1), 'tr': tr, 's': ex_src}],
            't': tags(e, no, p), 'es': [exam],
            'as': ['듣기'] if (no and no <= 17) else ['독해'],
            'd': day,
        })
        used += 1
    DB['days'] = day
    _db.save(s, m, DB)
    cnt = {}
    for it in DB['items']: cnt[it['d']] = cnt.get(it['d'], 0) + 1
    print('낱말 %d개 추가 (건너뜀 %d) · items %d개 · Day %d일'
          % (len(rows), len(R) - len(rows), len(DB['items']), DB['days']))
    print('마지막 네 Day 인원:', {d: cnt[d] for d in sorted(cnt)[-4:]})

main()
