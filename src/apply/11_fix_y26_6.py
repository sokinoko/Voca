# -*- coding: utf-8 -*-
"""26 6모 첫 묶음의 어긋난 예문 13곳을 바로잡는다. 여러 번 돌려도 같다."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db
_db.data_dir()
from y26_6_fix import FIX, MERGE

def main():
    s, m, DB = _db.load()
    by = {it['w'].lower(): it for it in DB['items']}
    n = 0
    for w, old_src, new_src, ch, u, tr in FIX:
        it = by.get(w.lower())
        assert it, '없는 낱말: %s' % w
        assert ch.count(u) == 1, '밑줄이 예문에 한 번 나와야 한다: %s' % w
        for ex in it['ex']:
            if ex['s'] != old_src: continue
            new = {'ch': ch.replace(u, '<u>%s</u>' % u, 1), 'tr': tr, 's': new_src}
            if ex == new: break
            ex.update(new); n += 1
            if it['s'] == old_src: it['s'] = new_src
            break

    moved = 0
    for src_w, dst_w, new_src, ch, u, tr in MERGE:
        it = by.get(src_w.lower()); dst = by.get(dst_w.lower())
        assert dst, '옮겨 갈 낱말이 없다: %s' % dst_w
        if not it: continue                       # 이미 옮겼다
        if not any(e['s'] == new_src for e in dst['ex']):
            dst['ex'].append({'ch': ch.replace(u, '<u>%s</u>' % u, 1), 'tr': tr, 's': new_src})
        exam = new_src.split()[0] + ' ' + new_src.split()[1]
        if exam not in dst['es']: dst['es'].append(exam)
        for a in it['as']:
            if a not in dst['as']: dst['as'].append(a)
        DB['items'].remove(it); moved += 1

    if moved:
        for i, x in enumerate(DB['items']): x['i'] = i   # 인덱스를 다시 매긴다
    if not n and not moved:
        return print('이미 바로잡혀 있다.')
    _db.save(s, m, DB)
    print('예문 %d곳을 본문대로 고쳤다 · 항목 %d개를 합쳤다 · items %d개'
          % (n, moved, len(DB['items'])))

main()
