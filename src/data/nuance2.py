# -*- coding: utf-8 -*-
"""부록 17(뉘앙스) 2차분 — 강사가 짚어 준 낱말.

사전 1번 뜻으로 읽으면 문장이 뒤집히는 낱말들이다. 1차분(23행)과 같은 성격이라
새 묶음을 만들지 않고 같은 그룹에 보탠다.

예문은 강사 노트에서 왔고 평가원 본문을 그대로 옮긴 것이 아니다. 그래서 출처는
전부 '추가'다(화면에는 「본시험 대비」로 나온다). 기출에 실제로 나온 낱말은
문항 번호를 n(독해포인트)에 적어 둔다 — 출처 라벨을 지어내지 않기 위한 것이다.

ROWS: (표제어, 뜻, 독해포인트, 예문, 해석, 밑줄 넣은 예문)
MORE: 이미 있는 행에 보탤 독해포인트. 같은 낱말을 두 행으로 쪼개지 않는다.
MERGE: 부록 행 → 단어장에서 예문을 보탤 기존 표제어. 없으면 새 항목을 만든다.
"""

ROWS = [
 ("challenge",
  "이의를 제기하다, 반박하다 / 난제(n)",
  "'도전하다'로만 읽으면 반박 신호를 놓친다. challenge the assumption = 그 가정이 틀렸다고 반박하다. 이 말이 나오면 뒤에 필자의 반론이 온다. 26 수능 37번에 challenging established assumptions로 나왔다",
  "The author is challenging established assumptions about the brain.",
  "필자는 뇌에 관한 기존의 가정에 이의를 제기하고 있다.",
  "The author is <u>challenging</u> established assumptions about the brain."),

 ("orientation / -oriented",
  "(평소 향하는) 방향, 지향, 성향",
  "동서남북 같은 물리적 방향뿐 아니라 '사람이나 대륙이 평소 향하는 쪽'. 수능에서는 접미사 -oriented로 자주 나온다. self-oriented = 자기 지향적인. 27 9모 33번에는 sense of orientation(방향 감각)으로 나왔다",
  "The very orientation of the continent decided which crops could spread.",
  "그 대륙이 놓여 있는 방향 자체가 어떤 작물이 퍼질 수 있는지를 정했다.",
  "The very <u>orientation</u> of the continent decided which crops could spread."),

 ("yield / yield to",
  "산출하다, 낳다 / (yield to) 굴복하다, 밀리다",
  "전치사 하나로 뜻이 갈린다. yield A = A를 산출하다 / yield to A = A에 굴복하다(= submit to). 27 6모 31번과 26 수능 36번은 둘 다 '산출하다' 쪽이다",
  "Feelings and thoughts are yielding to science.",
  "감정과 생각은 과학에 밀려 굴복하고 있다.",
  "Feelings and thoughts are <u>yielding to</u> science."),

 ("even / evenly / uneven",
  "고른, 균일한, 공평한 / 고르게 / 고르지 않은, 불공평한",
  "'심지어 · 짝수'가 아니라 고르고 균형 잡힌 이미지. do not learn evenly = 균일한 속도로 배우지 않는다. 그래서 uneven은 속도나 대우가 '균일하지 않은 → 불공평한'이 된다. 27 6모 41-42번에 uneven으로 나왔다",
  "People's experience of that access is uneven.",
  "그 접근에 대한 사람들의 경험은 고르지 않다.",
  "People's experience of that access is <u>uneven</u>."),

 ("pay / pay off",
  "대가를 치르다 / 보상을 주다, 결실을 맺다",
  "주어가 사람이면 '대가를 치르다'로 부정적이다 — You are going to pay for this. 주어가 노력이나 범죄처럼 무생물이면 '보상을 주다'가 된다 — Crime does not pay(범죄는 남는 게 없다). pay off는 '노력이 결실을 맺다'로 외워 둘 것",
  "Hard work pays off in the long run.",
  "노력은 길게 보면 결실을 맺는다.",
  "Hard work <u>pays off</u> in the long run."),

 ("general / generalization",
  "종합의, 전체를 다 다루는 / 일반화",
  "'그냥 대충의'가 아니라 '전체를 하나로 묶는'이다. General Hospital = 종합병원, Secretary General = 사무총장, General = 장군. generalization은 개별 차이를 뭉갰다는 비판 맥락에서 자주 나온다",
  "Almost all generalizations about human nature turn out to be wrong.",
  "인간 본성에 대한 거의 모든 일반화는 결국 틀린 것으로 드러난다.",
  "Almost all <u>generalizations</u> about human nature turn out to be wrong."),

 ("condition / be conditioned to",
  "조건 / 조건화하다, ~하도록 길들이다",
  "파블로프의 개처럼 '어떤 조건에 반응하도록 학습되다'. be conditioned to V = ~하도록 길들여지다 → A가 B를 좌우한다는 구조가 된다. unconditional love = 무조건적인 사랑. 26 6모 36번에서는 명사 '질병'으로 쓰였다",
  "Emotions must be conditioned to operate by the rules of reason.",
  "감정은 이성의 법칙에 따라 작동하도록 조건화되어야 한다.",
  "Emotions must be <u>conditioned to</u> operate by the rules of reason."),
]

# 이미 있는 행에 강사가 짚어 준 각도만 덧붙인다 (표제어 → 덧붙일 문장)
MORE = {
 "pitch": "야구의 '던지기'와 음악의 '음높이'로 갈린다. 음 이름(도 · 레)이 같아도 pitch는 다를 수 있다",
 "at the expense of": "돈 얘기가 아니라 '얻기 위해 치르는 희생'이다. = at the price/cost of",
 "end": "빈칸 추론에서 '최종 목적'으로 자주 나온다. The end does not always justify the means",
}

# 부록 행 → 단어장에서 예문을 보탤 기존 표제어 (규칙 8: 같은 낱말을 두 항목으로 쪼개지 않는다)
MERGE = {
 "challenge": "challenge",
 "orientation / -oriented": "orientation",
 "yield / yield to": "yield",
 "even / evenly / uneven": "uneven",
 "pay / pay off": "pay",
 "condition / be conditioned to": "condition",
}

# 기존 항목의 뜻을 넓혀야 하는 것만 (표제어 → 새 뜻)
WIDEN = {
 "orientation": "방향 감각, 지향, 성향",
 "uneven": "고르지 않은, 불공평한 (↔ even 고른 / evenly 고르게)",
 "pay": "지불하다 (→ pay B to A) / 대가를 치르다 · (pay off) 결실을 맺다",
 "condition": "1.n.질병 2.n.조건 3.v.조건화하다, ~하도록 길들이다",
}

# 새로 만들 항목 (부록 표제어 → 품사)
FRESH = {"general / generalization": "n"}
