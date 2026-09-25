# -*- coding: utf-8 -*-
"""평가원 영어 해설지에서 [Words and Phrases]를 문항별로 뽑는다.

PDF가 넣은 줄바꿈·쪽번호를 걷어내고 (표제어, 뜻, 문항번호)로 돌려준다.
뽑기만 한다 — 어떤 것을 단어장에 넣을지는 사람이 고른다.

  python3 src/tools/wp_extract.py <해설지.pdf> [출력.json]
"""
import io, json, re, sys

HEAD = r"[A-Za-z][A-Za-z\-'’.]*(?:[ ](?:[A-Za-z][A-Za-z\-'’.]*|~[A-Za-z]*))*"
PAT  = re.compile(r'(?<![A-Za-z])(' + HEAD + r')[ ]+(?=[가-힣~(\[])')
HAN  = '가-힣'

def clean(raw):
    s = re.sub(r'(?m)^\s*-?\s*\d{1,3}\s*-?\s*$', ' ', raw)          # 쪽번호 줄
    s = re.sub(r'\s*\n\s*', '\n', s)
    s = re.sub(r'\n\s*\d{1,3}\s*\n', '\n', s)                      # 줄 사이 쪽번호
    s = re.sub(r'(?<=[%s])\n(?=[%s])' % (HAN, HAN), '', s)          # 줄바꿈으로 갈린 한글 낱말
    s = re.sub(r'(?<=[%s])(\d{1,3})\n(?=[%s])' % (HAN, HAN), '', s)  # 그 사이 쪽번호
    s = re.sub(r'\n', ' ', s)
    return re.sub(r'[ ]{2,}', '  ', s).strip()

def blocks(text):
    qs = [(int(m.group(1)), m.start())
          for m in re.finditer(r'(?m)^\s*(\d{1,2})\.\s*\[출제 의도\]', text)]
    for i, (no, s) in enumerate(qs):
        yield no, text[s: qs[i+1][1] if i+1 < len(qs) else len(text)]

def entries(raw):
    s = clean(raw)
    ms = list(PAT.finditer(s))
    for i, m in enumerate(ms):
        end = ms[i+1].start() if i+1 < len(ms) else len(s)
        g = s[m.end():end].strip().rstrip(',')
        # 해석 문단을 삼킨 것은 버린다 — 뜻은 짧다
        if len(g) > 40 or not re.search(r'[%s]' % HAN, g): continue
        yield m.group(1).strip(), g

def extract(pdf):
    from pypdf import PdfReader
    text = '\n'.join(p.extract_text() or '' for p in PdfReader(pdf).pages)
    out = {}
    for no, b in blocks(text):
        m = re.search(r'\[Words and Phrases\](.*?)(?=\[출제 의도\]|\Z)', b, re.S)
        if not m: continue
        for e, g in entries(m.group(1)):
            out.setdefault(e.lower(), (e, g, no))
    return [list(v) for v in sorted(out.values(), key=lambda x: (x[2], x[0].lower()))]

if __name__ == '__main__':
    rows = extract(sys.argv[1])
    print('항목 %d개' % len(rows))
    if len(sys.argv) > 2:
        io.open(sys.argv[2], 'w', encoding='utf-8').write(
            json.dumps(rows, ensure_ascii=False, indent=0))
    else:
        for e, g, no in rows: print('%2d  %-26s %s' % (no, e, g))
