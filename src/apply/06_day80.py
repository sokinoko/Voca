# -*- coding: utf-8 -*-
"""Day를 80개씩으로 묶는다.

기존 44일(40개씩)을 둘씩 붙여 22일 × 80개로 만든다.
Day 1+2 → 1, Day 3+4 → 2 … 같이 있던 단어는 계속 같이 있고 번호만 절반이 된다.
단어가 다른 묶음으로 건너가지 않으므로 외우던 덩어리가 흐트러지지 않는다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db

SIZE = 80

def main():
    s, m, DB = _db.load()
    before = DB['days']
    sizes = {}
    for it in DB['items']: sizes[it['d']] = sizes.get(it['d'], 0) + 1
    if max(sizes.values()) > 40:
        return print('이미 묶여 있다 (가장 큰 Day %d개).' % max(sizes.values()))

    moved = {}
    for it in DB['items']:
        old = it['d']
        new = (old + 1) // 2                   # 1,2→1  3,4→2 …
        moved.setdefault(new, set()).add(old)
        it['d'] = new
    DB['days'] = (before + 1) // 2

    _db.save(s, m, DB)
    cnt = {}
    for it in DB['items']: cnt[it['d']] = cnt.get(it['d'], 0) + 1
    print('Day %d일 → %d일' % (before, DB['days']))
    print('묶음 크기:', sorted(set(cnt.values())))
    print('예: 새 Day 1 ← 옛 Day %s / 새 Day 22 ← 옛 Day %s'
          % (sorted(moved[1]), sorted(moved[DB['days']])))

main()
