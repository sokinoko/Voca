# -*- coding: utf-8 -*-
"""직접 쓴 문법 예문 뱅크를 개념 시험에 넣는다.
A 준동사 → 부록 19 / B 전치사 동사 → 부록 12 / C 문형 → 문형표(DB.gramcz)"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db
_db.data_dir()
from bank_a import A
from bank_b import B
from bank_c import C

def main():
    src, m, DB = _db.load()
    g19 = next(g for g in DB['apx'] if g['t'].startswith('19.'))
    g12 = next(g for g in DB['apx'] if g.get('f') == 'vprep')

    packA, packB, packC = _db.pack_cz(A), _db.pack_cz(B), _db.pack_cz(C)
    have = {q['s'] for q in g19.get('cz', [])}
    g19['cz'] = g19.get('cz', []) + [q for q in packA if q['s'] not in have]
    g12['cz'] = packB
    DB['gramcz'] = packC

    _db.save(src, m, DB)
    print('부록 19 개념 %d문항 / 부록 12 개념 %d문항 / 문형표 개념 %d문항'
          % (len(g19['cz']), len(g12['cz']), len(DB['gramcz'])))

main()
