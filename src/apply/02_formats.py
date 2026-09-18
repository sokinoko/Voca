# -*- coding: utf-8 -*-
"""부록마다 시험 형식(f)과 연결사 방향 라벨(lbl)을 박고,
부정어구의 「긍정이냐 부정이냐」 판정 문항을 넣는다."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db
_db.data_dir()
from formats import FMT
from neg_judge import NEG

def main():
    src, m, DB = _db.load()
    assert len(DB['apx']) == len(FMT), \
        'formats.py의 줄 수(%d)가 부록 수(%d)와 다르다' % (len(FMT), len(DB['apx']))
    for g, (f, lbl) in zip(DB['apx'], FMT):
        g['f'] = f
        if lbl: g['lbl'] = lbl

    neg = next(g for g in DB['apx'] if g['f'] == 'neg')
    heads, judge = [], []
    for s, ans in NEG:
        head, why = ans.split(' — ')
        if head not in heads: heads.append(head)
        judge.append({"s": s + " — 이 문장의 뜻은 {0}", "tr": why, "pick": head,
                      "n": "부정어는 not이 없어도 문장을 뒤집는다. 관사와 어순을 먼저 본다."})
    neg['judge'] = judge
    neg['heads'] = heads

    _db.save(src, m, DB)
    print('형식 지정 %d그룹 / 부정어구 판정 %d문항 (보기: %s)'
          % (len(FMT), len(judge), ', '.join(heads)))

main()
