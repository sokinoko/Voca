# -*- coding: utf-8 -*-
"""수능 표기를 26학년도로 바로잡는다.

05_year.py를 처음 돌릴 때 기존 앱의 「수능」을 27 수능으로 붙였는데 틀렸다.
형석이가 치는 시험이 2027학년도 수능이라 아직 안 쳤고, 단어장에 들어 있는
수능 기출은 직전 시험인 **2026학년도 수능**(2025년 11월)이다.
6월·9월 모의평가는 2027학년도가 맞다.

  27 수능 → 26 수능   (6월·9월 라벨은 그대로)

라벨 순서도 시험 순서대로 바꾼다: 26 6모 · 26 수능 · 27 6모 · 27 9모.
"""
import sys, os, io, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db

OLD, NEW = '27 수능', '26 수능'
ROW_OLD = "['전체','27 6모','27 9모','27 수능','26 6모','고빈출','문형','부록']"
ROW_NEW = "['전체','26 6모','26 수능','27 6모','27 9모','고빈출','문형','부록']"

def walk(v, n):
    if isinstance(v, str):
        if OLD in v: n[0] += 1
        return v.replace(OLD, NEW)
    if isinstance(v, list):
        return [walk(x, n) for x in v]
    if isinstance(v, dict):
        return {k: walk(x, n) for k, x in v.items()}
    return v

def main():
    s, m, DB = _db.load()
    n = [0]
    if OLD not in m.group(1):
        print('DB는 이미 26 수능이다.')
    else:
        DB = walk(DB, n)
        _db.save(s, m, DB)
        print('DB에서 %s → %s 로 바꾼 문자열: %d개' % (OLD, NEW, n[0]))
        print('시험 라벨:', sorted({e for it in DB['items'] for e in it['es']}))

    src = io.open(_db.HTML, encoding='utf-8').read()
    if ROW_NEW in src:
        print('라벨 줄은 이미 바뀌어 있다.')
    else:
        assert src.count(ROW_OLD) == 1, '시험 라벨 줄을 찾지 못했다'
        io.open(_db.HTML, 'w', encoding='utf-8').write(src.replace(ROW_OLD, ROW_NEW))
        print('시험 라벨 줄 순서를 시험 순서대로 바꿨다.')

main()
