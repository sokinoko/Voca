# -*- coding: utf-8 -*-
"""평가원 PDF에서 뽑은 영어 본문의 글자 간격 잔재를 되돌린다.

평가원 듣기 대본 PDF는 자모다 공백을 넣어 뽑히는 구간이 있고
( "s t o r e .  W e ' r e  e x c i t e d" ), 문제지는 낱말 안이 갈라진다
( "cust omers", "e vent", "fo r" ). 사전을 근거로만 붙인다 — 사전에 없는
조합은 건드리지 않는다. 본문을 고쳐 쓰는 도구가 아니다.

  python3 src/tools/pdftext.py <파일.pdf> [출력.txt]
"""
import io, re, sys
from functools import lru_cache

@lru_cache(maxsize=1)
def lex():
    import cmudict
    from wordfreq import zipf_frequency as z
    d = set(cmudict.dict())
    return d, z

def zf(w):
    _, z = lex()
    return z(w.lower().strip("'’.,;:!?()\""), 'en')

def incmu(w):
    """cmudict에 있는가 — 진짜 낱말인지 가리는 더 깐깐한 기준."""
    d, _ = lex()
    return w.lower().strip("'’.,;:!?()\"") in d

def word(w):
    d, z = lex()
    w = w.lower().strip("'’.,;:!?()\"")
    if len(w) == 1: return w in ('a', 'i')      # 낱말 안이 갈라진 한 글자는 낱말이 아니다
    if len(w) <= 3: return w in d              # ll·fo·goe·sto 같은 조각을 낱말로 보지 않는다
    return bool(w) and (w in d or z(w, 'en') >= 2.0)

def despace(s):
    """자모다 공백이 들어간 구간을 되돌린다.

    그 구간은 글자 사이가 한 칸, 낱말 사이가 두 칸이다. 두 칸을 낱말 경계로
    보고 한 칸만 지운다. 한 글자 토큰이 네 개 이상 이어질 때만 손댄다.
    """
    CH = r"[A-Za-z\u2019',.?!;:]"
    RUN = re.compile(r"(?:(?<=\s)|^)(?:%s[ ]{1,2}){3,}%s(?=\s|$)" % (CH, CH))
    def join(m):
        return re.sub(r'\x00', ' ', re.sub(r'[ ]', '', re.sub(r'[ ]{2,}', '\x00', m.group(0))))
    return RUN.sub(join, s)

CORE = re.compile(r"[A-Za-z\u2019']+")

def core(t):
    m = CORE.search(t)
    return m.group(0) if m else ''

def _runs(toks):
    """한 글자 토큰 두세 개가 이어진 짧은 조각을 붙인다 (「o f」→ of)."""
    out, i = [], 0
    while i < len(toks):
        j = i
        while j < len(toks) and re.fullmatch(r'[A-Za-z]', toks[j]): j += 1
        if j - i >= 2:
            k = j
            while k > i + 1:                       # 긴 쪽부터 낱말인지 본다
                if word(''.join(toks[i:k])):
                    out.append(''.join(toks[i:k])); i = k; break
                k -= 1
            else:
                out.append(toks[i]); i += 1
            continue
        out.append(toks[i]); i += 1
    return out

def _letters(toks):
    """떨어져 나온 한 글자를 원래 붙어 있던 쪽에 되돌린다.

    「fo r」는 왼쪽(for), 「my s ocial」은 오른쪽(social), 「everyon e,」는
    왼쪽(everyone,)이다. 사전에 없는 쪽이 깨진 쪽이라고 보고 그쪽에 붙인다.
    양쪽이 다 낱말이면 손대지 않는다.
    """
    for i, t in enumerate(toks):
        c = core(t)
        if len(c) != 1 or not c.isalpha(): continue
        if not re.fullmatch(r"[A-Za-z][^A-Za-z]*", t): continue   # 뒤 문장부호만 허용
        tail = t[1:]
        L = core(toks[i-1]) if i else ''
        R = core(toks[i+1]) if i+1 < len(toks) else ''
        if len(L) < 2 or toks[i-1] != L: L = ''       # 앞 토큰에 문장부호가 있으면 낱말 끝
        if len(R) < 2 or tail: R = ''                 # 문장부호를 달고 있으면 앞 낱말의 끝이다
        cl = bool(L) and word(L + c)
        cr = bool(R) and word(c + R)
        if cl and cr:
            if word(L) and not word(R): cl = False
            elif word(R) and not word(L): cr = False
            else: continue
        if c in ('a', 'A', 'I'):                      # 진짜 한 글자 낱말을 지키다
            if cl and word(L): cl = False
            if cr and word(R): cr = False
        if cl:   toks[i-1], toks[i] = toks[i-1] + t, ''
        elif cr: toks[i], toks[i+1] = '', c + toks[i+1]
    return [t for t in toks if t]

def _fragments(toks):
    """낱말 안이 두 조각으로 갈라진 것을 붙인다 (「cust omers」)."""
    out, i = [], 0
    while i < len(toks):
        a = toks[i]
        b = toks[i+1] if i+1 < len(toks) else ''
        ca, cb = core(a), core(b)
        # 뒤 조각은 cmudict에 있어야 낱말로 인정한다. lls·fulness 같은 꼬리를 걸러낸다.
        # 뒤 조각이 사전에 있어도(safe ty · import ant) 붙인 쪽이 훨씬 흔하면 붙인다.
        joinable = (a == ca and len(ca) >= 2 and len(cb) >= 2 and word(ca + cb)
                    and (not (word(ca) and incmu(cb))
                         or (zf(ca + cb) >= 3.0 and zf(ca + cb) > zf(cb) + 1.0)))
        if joinable:
            out.append(a + b); i += 2; continue
        out.append(a); i += 1
    return out

def _contract(toks):
    """축약형이 따옴표에서 끊긴 것을 되돌린다 (「there’ sa」→ there’s a)."""
    SUF = ('ll', 're', 've', 's', 't', 'd', 'm')
    for i in range(len(toks) - 1):
        a, b = toks[i], toks[i+1]
        if not a.endswith('\u2019') or not re.match(r'[A-Za-z]', b): continue
        for suf in SUF:
            if not b.lower().startswith(suf): continue
            rest = b[len(suf):]
            if rest and not word(core(rest)): break
            toks[i], toks[i+1] = a + b[:len(suf)], rest
            break
    return [t for t in toks if t]

def _shift(toks):
    """낱말 경계가 한 글자 밀린 것을 되돌린다 (「Ib elieve」→ I believe)."""
    for i in range(len(toks) - 1):
        a, b = toks[i], toks[i+1]
        if not re.fullmatch(r"[A-Za-z]{2,}", a): continue     # 축약형(there's)은 아래에서 다룬다
        if not re.fullmatch(r"[A-Za-z\u2019']{2,}[^A-Za-z]*", b): continue
        if word(a) and word(core(b)): continue
        if len(a[-1] + core(b)) >= 3 and word(a[:-1]) and word(a[-1] + core(b)):
            toks[i], toks[i+1] = a[:-1], a[-1] + b
    return toks

def rejoin(s):
    """낱말 안이 갈라진 것을 사전을 보고 붙인다. 사전에 없는 조합은 두다."""
    toks = _runs(re.split(r'\s+', s))
    for _ in range(3):                    # 세 조각으로 갈린 것(fo rt h · impo rt ant)은
        joined = _fragments(_letters(toks))   # 한 번에 안 붙는다. 더 안 붙을 때까지 돌린다
        if joined == toks: break
        toks = joined
    return ' '.join(_shift(_contract(toks)))

LIG = {'ﬀ':'ff','ﬁ':'fi','ﬂ':'fl','ﬃ':'ffi','ﬄ':'ffl','ﬅ':'st','ﬆ':'st'}

def clean(s):
    s = s.replace('﻿', '')
    for a, b in LIG.items(): s = s.replace(a, b)   # 합자(ﬃ)를 풀어 놓는다
    s = despace(s)
    s = re.sub(r'\s*\n\s*', ' ', s)
    s = rejoin(s)
    s = re.sub(r'\s+([.,;:!?])', r'\1', s)          # 낱말과 떨어진 마침표
    return re.sub(r'[ \t]{2,}', ' ', s).strip()

def pages(pdf):
    from pypdf import PdfReader
    return [p.extract_text() or '' for p in PdfReader(pdf).pages]

if __name__ == '__main__':
    t = clean('\n'.join(pages(sys.argv[1])))
    if len(sys.argv) > 2: io.open(sys.argv[2], 'w', encoding='utf-8').write(t)
    else: print(t[:3000])

def sentences(text):
    """한글·문항 기호를 걷어내고 영어 문장만 끊어 낸다."""
    t = re.sub(r'[가-힣ㄱ-㆏①-⑳ⅰ-ⅹ]+', '\n', text)
    t = re.sub(r'[\[\]*※◦]|\d+\s*번|\(\s*[A-E]\s*\)|-\s*\d+\s*-', '\n', t)
    out = []
    for part in t.split('\n'):
        part = re.sub(r'\s+', ' ', part).strip(' .,;:')
        if len(part) < 12: continue
        for s in re.split(r'(?<=[.?!])\s+(?=[A-Z“"(])', part):
            s = s.strip()
            if len(s.split()) >= 4: out.append(s)
    return out

def question_spans(text, last=45):
    """문제지 본문을 문항별로 가른다. {문항번호: 그 문항이 차지하는 구간}

    「31. We know that…」처럼 번호 뒤에 영어가 오기도 하고 「26. Claude Shannon에
    관한…」처럼 한글이 오기도 한다. 번호만 보고 1부터 차례로 올라가는 것만 잡는다.
    """
    want, marks = 1, []
    for m in re.finditer(r'(?<![\d.,])(\d{1,2})\.(?=\s)', text):
        if int(m.group(1)) == want:
            marks.append((want, m.start())); want += 1
            if want > last: break
    out = {}
    for i, (no, s) in enumerate(marks):
        out[no] = (s, marks[i+1][1] if i+1 < len(marks) else len(text))
    return out
