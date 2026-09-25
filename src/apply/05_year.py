# -*- coding: utf-8 -*-
"""시험 표기에 학년도를 붙인다.

기존 앱의 6월·9월은 2027학년도(형석이 고3 때 친 것)이고, 수능 기출은 직전
시험인 2026학년도 수능이다. 작년 모의평가를 새로 넣게 되면서 구분이 필요해졌다.
  6월 → 27 6모   /   9월 → 27 9모   /   수능 → 26 수능

「수능 빈출」처럼 특정 시험을 가리키지 않는 말은 건드리지 않는다.
"""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _db

MAP = [('6월', '27 6모'), ('9월', '27 9모'), ('수능', '26 수능')]

def src(v):                       # 출처만 들어 있는 필드 — 그대로 바꾼다
    for a, b in MAP:
        v = re.sub(r'(?<![0-9년])' + a, b, v)
    return v

def main():
    s, m, DB = _db.load()
    if '27 6모' in s[m.start(1):m.end(1)][:4000] or any(
            e.startswith('27 ') for it in DB['items'] for e in it['es']):
        return print('이미 학년도가 붙어 있다.')

    n = {'es':0, 'items.s':0, 'ex.s':0, 'apx':0, 'rep':0}
    for it in DB['items']:
        it['es'] = [dict(MAP).get(e, e) for e in it['es']]
        n['es'] += 1
        if re.search(r'6월|9월|수능', it['s']): it['s'] = src(it['s']); n['items.s'] += 1
        for e in it['ex']:
            if re.search(r'6월|9월|수능', e['s']): e['s'] = src(e['s']); n['ex.s'] += 1

    for g in DB['apx']:            # 그룹 제목(「수능 빈출」)은 건드리지 않는다
        for r in g['r']:
            if re.search(r'6월|9월|수능', r['s']): r['s'] = src(r['s']); n['apx'] += 1
            # 설명 안의 (수능 33번) 같은 출처 표기만
            r['n'] = re.sub(r'(6월|9월|수능)(?=\s*\d)', lambda mm: dict(MAP)[mm.group(1)], r['n'])

    for secn in DB['rep']:
        secn['t'] = src(secn['t'])
        secn['g'] = src(secn['g'])
        for r in secn.get('r', []):
            if r.get('src'): r['src'] = [src(v) for v in r['src']]; n['rep'] += 1
            for e in r.get('ex', []) or []: e['s'] = src(e['s'])

    _db.save(s, m, DB)
    print('바꾼 곳:', n)
    print('시험 라벨:', sorted({e for it in DB['items'] for e in it['es']}))

main()
