# -*- coding: utf-8 -*-
"""26 6모 첫 묶음에서 예문이 본문과 어긋난 것을 바로잡는다.

src/tools/verify_src.py를 만들고 나서 돌려 보니 13곳이 걸렸다. 예문을 다듬다가
없는 낱말을 끼워 넣었거나(「When designers talk about…」), 문항 번호를 잘못 붙인
것이다. 본문에 있는 그대로로 되돌린다.

(표제어, 지금 출처, 새 출처, 새 예문, 새 밑줄, 새 해석)
새 출처가 지금 것과 같으면 예문만 고친다.
"""
FIX = [
 ("miner","26 6모 18번","26 6모 18번",
  "made the gold miners arriving to Qukkon","miners",
  "Qukkon에 도착하던 금 채굴자들을"),
 ("consistently","26 6모 22번","26 6모 22번",
  "a certain player ends up consistently with the desired outcome","consistently",
  "어떤 선수가 지속적으로 원하는 결과를 내게 되다"),
 ("zoology","26 6모 26번","26 6모 26번",
  "with a master's degree in zoology","zoology",
  "동물학 석사 학위를 받고"),
 ("alien","26 6모 30번","26 6모 30번",
  "alien, they actually engage in similar practices","alien",
  "낯설지만 그들은 실은 비슷한 일을 한다"),
 ("highlight","26 6모 30번","26 6모 30번",
  "the aim is to highlight","highlight",
  "목표는 ~을 부각하는 것이다"),
 ("pinpoint","26 6모 30번","26 6모 30번",
  "pinpointing their target audience, crafting a unique value proposition","pinpointing",
  "목표 독자를 짚어 내고 고유한 가치 제안을 다듬는 것"),
 ("imply","26 6모 31번","26 6모 31번",
  "because teaching implies a level of","implies",
  "가르침은 어느 정도의 ~을 함의하기 때문에"),
 ("inactivity","26 6모 36번","26 6모 36번",
  "inactivity is a waste of human potential","inactivity",
  "움직이지 않는 것은 인간 잠재력의 낭비다"),
 ("back and forth","26 6모 37번","26 6모 37번",
  "a pendulum that swings back and forth between them","back and forth",
  "그 사이를 앞뒤로 흔들리는 진자"),
 ("nurturing motivation","26 6모 38번","26 6모 38번",
  "A cute product or package design elicits a nurturing motivation","nurturing motivation",
  "귀여운 제품이나 포장 디자인은 보살피려는 동기를 불러일으킨다"),
 ("skip","26 6모 39번","26 6모 듣기 12번",
  "you didn't skip breakfast this morning","skip",
  "너 오늘 아침을 거르지 않았구나"),
 ("seamlessness","26 6모 42번","26 6모 42번",
  "an aspiration towards seamlessness aims to make the technological experience","seamlessness",
  "이음매 없음을 향한 열망은 기술 경험을 ~하게 만들려 한다"),
]

# perceived는 항목 자체를 뺀다. 이미 있는 perceive와 같은 낱말인데 밑줄도
# perceive에 그어져 있었고 문항 번호(38번)도 틀렸다(29번). 예문은 perceive
# 밑으로 옮긴다 — 또 나온 낱말은 예문을 하나 더 다는 규칙 그대로다.
MERGE = [("perceived", "perceive", "26 6모 29번",
          "perceive the imaginary story to be a real one", "perceive",
          "상상의 이야기를 진짜로 받아들이다")]
