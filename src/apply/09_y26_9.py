# -*- coding: utf-8 -*-
"""2026학년도 9월 모의평가 단어를 단어장에 넣는다.

07_y26_6.py와 같은 방식이다. 뒤쪽 Day부터 채우고 기존 단어의 Day는 건드리지
않는다. 마지막 Day가 80개에 못 미치면 거기부터 채우고, 넘치면 새 Day를 연다.
화면의 시험 라벨 줄에도 「26 9모」를 시험 순서 자리에 끼운다.
"""
import sys, os, io, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db
_db.data_dir()
from y26_9 import R, POS, POLY
from wordfreq import zipf_frequency as z

SIZE, EXAM = 80, '26 9모'
ROW_OLD = "['전체','26 6모','26 수능','27 6모','27 9모','고빈출','문형','부록']"
ROW_NEW = "['전체','26 6모','26 9모','26 수능','27 6모','27 9모','고빈출','문형','부록']"

def tags(e, no):
    w = [t for t in re.findall(r"[A-Za-z']+", e) if len(t) > 2]
    f = min([z(t.lower(), 'en') for t in w] or [9])
    ts = ['핵심' if f < 3.3 else '필수']
    if no <= 17: ts.append('듣기표현')
    if e in POLY: ts.append('다의어')
    return ts

def main():
    s, m, DB = _db.load()
    have = {it['w'].lower() for it in DB['items']}
    rows = [r for r in R if r[0].lower() not in have]
    if rows:
        day = DB['days']
        used = sum(1 for it in DB['items'] if it['d'] == day)
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
            used += 1
        DB['days'] = day
        _db.save(s, m, DB)
        cnt = {}
        for it in DB['items']: cnt[it['d']] = cnt.get(it['d'], 0) + 1
        print('%s 단어 %d개 추가 (건너뜀 %d)' % (EXAM, len(rows), len(R) - len(rows)))
        print('items %d개 · Day %d일' % (len(DB['items']), DB['days']))
        print('마지막 네 Day 인원:', {d: cnt[d] for d in sorted(cnt)[-4:]})
    else:
        print('이미 들어가 있다.')

    src = io.open(_db.HTML, encoding='utf-8').read()
    if ROW_NEW in src:
        print('라벨 줄에 이미 있다.')
    else:
        assert src.count(ROW_OLD) == 1, '시험 라벨 줄을 찾지 못했다'
        io.open(_db.HTML, 'w', encoding='utf-8').write(src.replace(ROW_OLD, ROW_NEW))
        print('시험 라벨 줄에 %s를 끼웠다.' % EXAM)

main()
