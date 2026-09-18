# -*- coding: utf-8 -*-
"""시험 문항을 다시 손본다.

문맥 없이는 답이 하나로 정해지지 않는 문항 유형을 걷어내고, 부록 성격에 맞는
유형으로 갈아 끼운다.
 - 연결사 10묶음의 한 문장짜리 빈칸은 성립하지 않는다(앞뒤 관계가 있어야 한다).
   지문이 붙은 문항을 따로 써서 「접속사 통합 시험」 하나로 모은다.
 - 어휘성 부록은 빈칸 대신 「밑줄 친 말의 뜻 고르기」로 바꾼다.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db
_db.data_dir()
from conn_passages import P
from syn_items import ALL as SYN

# 부록 번호 → 시험 형식
NEWF = {'8':'syn', '10':'syn', '11':'syn', '17':'syn'}

def main():
    src, m, DB = _db.load()

    DB['connpass'] = _db.pack_cz(P)          # 접속사 통합 시험용 지문 문항

    n = 0
    for g in DB['apx']:
        num = g['t'].split('.')[0]
        if num in SYN:
            g['syn'] = [{"s": s, "tr": tr, "n": note, "o": list(o), "a": a}
                        for s, tr, o, a, note in SYN[num]]
            n += len(g['syn'])
        if num in NEWF:
            g['f'] = NEWF[num]

    _db.save(src, m, DB)
    got = {g['t'].split('.')[0]: len(g.get('syn', [])) for g in DB['apx'] if g.get('syn')}
    print('접속사 지문 문항 %d개' % len(DB['connpass']))
    print('동의어 문항 %d개 — 부록별 %s' % (n, got))
    print('형식 바뀐 부록:', ', '.join('%s→%s' % (k, v) for k, v in NEWF.items()))

main()
