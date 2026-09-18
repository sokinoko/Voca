# -*- coding: utf-8 -*-
"""접속사 통합 시험 — 문맥이 있는 지문 문항.

연결사는 앞뒤 관계가 있어야 답이 하나로 정해진다. 한 문장만 주고 빈칸을 뚫으면
However든 In addition이든 다 들어가서 문제가 성립하지 않는다.
그래서 앞 문장을 반드시 붙이고, 보기는 서로 다른 방향에서 고른다.

(지문, 해석, [(보기, 정답인덱스)], 해설)   ·  {0} {1} 이 빈칸
"""
P = [
# ── 역접 ──
("Most people assume that talking faster makes a speaker sound confident. {0}, listeners"
 " in the study rated slower speakers as more trustworthy.",
 "대부분은 빠르게 말하면 자신 있어 보인다고 여긴다. 그러나 연구에서 청자들은 느리게 말하는 사람을 더 믿을 만하다고 평가했다.",
 [(["However","Therefore","For example","In addition","Likewise"],0)],
 "앞의 통념을 연구 결과가 뒤집는다. 방향이 꺾이므로 역접."),
("The new policy was expected to cut waiting times in half. {0}, the average wait grew"
 " longer in the first three months.",
 "새 정책은 대기 시간을 절반으로 줄일 것으로 기대됐다. 그런데 첫 석 달간 평균 대기 시간은 오히려 길어졌다.",
 [(["On the contrary","As a result","That is","Moreover","Accordingly"],0)],
 "기대와 정반대 결과다. As a result를 쓰면 기대대로 됐다는 뜻이 되어 틀린다."),
("Solar panels have become far cheaper over the past decade. {0}, installation costs in"
 " many regions have barely moved.",
 "태양광 패널은 지난 10년간 훨씬 저렴해졌다. 그럼에도 여러 지역의 설치 비용은 거의 그대로다.",
 [(["Nonetheless","Consequently","For instance","Similarly","In short"],0)],
 "싸졌는데도 비용이 안 내렸다. 앞을 인정하면서 뒤집는 자리."),
# ── 인과 ──
("The bridge had gone thirty years without inspection. {0}, engineers closed it the moment"
 " the cracks were reported.",
 "그 다리는 30년간 점검을 받지 않았다. 그래서 기술자들은 균열이 보고되자마자 다리를 폐쇄했다.",
 [(["Consequently","Nevertheless","By contrast","Meanwhile","Admittedly"],0)],
 "앞이 원인, 뒤가 결과다."),
("Coastal water temperatures rose nearly two degrees last summer. {0}, several fish species"
 " moved north for the first time on record.",
 "지난여름 연안 수온이 2도 가까이 올랐다. 그 결과 여러 어종이 기록상 처음으로 북쪽으로 이동했다.",
 [(["As a result","On the other hand","In other words","Even so","Beforehand"],0)],
 "온도 상승이 원인, 이동이 결과."),
("The museum removed its entrance fee last year. {0}, attendance among local students"
 " tripled within six months.",
 "그 박물관은 작년에 입장료를 없앴다. 그리하여 여섯 달 만에 지역 학생 관람객이 세 배가 되었다.",
 [(["Thus","Yet","Namely","Conversely","Previously"],0)],
 "정책이 원인이고 관람객 증가가 결과다."),
# ── 첨가 ──
("The training program shortened the average recovery time by two weeks. {0}, it lowered"
 " the rate of repeat injury among the same athletes.",
 "그 훈련 프로그램은 평균 회복 기간을 2주 줄였다. 게다가 같은 선수들의 재부상률도 낮췄다.",
 [(["Moreover","However","For example","Otherwise","In contrast"],0)],
 "같은 방향의 좋은 점을 하나 더 얹는다."),
("Bamboo grows back within a few years of cutting. {0}, it needs neither fertilizer nor"
 " irrigation on most soils.",
 "대나무는 베어도 몇 년 안에 다시 자란다. 또한 대부분의 토양에서 비료도 관개도 필요하지 않다.",
 [(["In addition","Nevertheless","As a result","Instead","Regardless"],0)],
 "장점을 나열하는 자리라 첨가."),
# ── 예시 ──
("Some birds change their songs to cut through city noise. {0}, great tits in downtown"
 " Leiden sing at a higher pitch than those in the woods.",
 "어떤 새들은 도시 소음을 뚫으려고 노랫소리를 바꾼다. 예를 들어 레이던 도심의 박새는 숲의 박새보다 높은 음으로 운다.",
 [(["For example","Therefore","On the other hand","In conclusion","Meanwhile"],0)],
 "앞의 일반적 진술을 구체 사례로 받는다."),
("Small design choices can change how much people eat. {0}, diners served on ten-inch"
 " plates took about a fifth less food than those given twelve-inch plates.",
 "작은 디자인 선택이 먹는 양을 바꿀 수 있다. 가령 10인치 접시를 받은 사람은 12인치를 받은 사람보다 약 5분의 1 적게 담았다.",
 [(["For instance","Even so","Accordingly","Likewise","In brief"],0)],
 "추상 진술 다음에 구체 수치가 온다."),
# ── 환언 ──
("The committee decided to postpone the vote until every member had read the full report."
 " {0}, nothing will be settled before the end of the month.",
 "위원회는 모든 위원이 보고서를 다 읽을 때까지 표결을 미루기로 했다. 다시 말해 이달 말 전에는 아무것도 정해지지 않는다.",
 [(["In other words","For example","Nevertheless","Similarly","Afterward"],0)],
 "앞 내용을 쉬운 말로 바꿔 말한다."),
# ── 양보 ──
("{0} the sample was small, the pattern held in every one of the twelve trials.",
 "표본이 작기는 했지만, 그 양상은 열두 번의 실험 모두에서 유지됐다.",
 [(["Although","Because","Provided that","So that","As soon as"],0)],
 "앞을 인정하고 뒤에서 뒤집는 양보 자리. Because를 넣으면 논리가 반대가 된다."),
("{0} critics dismissed the film on release, it is now taught in half the country's"
 " film schools.",
 "비평가들이 개봉 당시엔 그 영화를 깎아내렸지만, 지금은 전국 영화학교 절반에서 가르친다.",
 [(["While","Since","Unless","In case","Now that"],0)],
 "과거의 혹평과 현재의 평가가 대조된다. 양보의 while."),
# ── 조건 ──
("Keep the seedlings above ten degrees at night. {0}, the roots will stop taking up water"
 " and the leaves will yellow within days.",
 "모종을 밤에 10도 이상으로 유지하라. 그러지 않으면 뿌리가 물을 빨아들이지 못해 며칠 안에 잎이 누레진다.",
 [(["Otherwise","Therefore","Likewise","In addition","Meanwhile"],0)],
 "앞의 지시를 안 지켰을 때를 말한다. 조건의 부정."),
("{0} her teacher's encouragement, Sally would never have picked up the violin at all.",
 "선생님의 격려가 없었다면 Sally는 바이올린을 아예 잡지도 않았을 것이다.",
 [(["But for","Thanks to","Owing to","As for","Along with"],0)],
 "가정법 과거완료와 짝을 이루는 but for. Thanks to를 넣으면 가정이 사라진다."),
# ── 시간 ──
("The article was written in 1948 but found no publisher at the time. {0}, it appeared in"
 " a small journal nine years later.",
 "그 글은 1948년에 쓰였지만 당시엔 낼 곳을 찾지 못했다. 결국 9년 뒤 작은 학술지에 실렸다.",
 [(["Eventually","Immediately","In contrast","For example","Namely"],0)],
 "시간이 흐른 뒤의 결말을 말한다."),
("First the wind separates from the face of the building. {0}, a low-pressure pocket forms"
 " on the far side and pulls the structure toward it.",
 "먼저 바람이 건물 표면에서 떨어져 나간다. 그다음 반대편에 저기압 주머니가 생겨 구조물을 그쪽으로 당긴다.",
 [(["Then","Nevertheless","By comparison","That is","Regardless"],0)],
 "순서를 매기는 자리."),
# ── 비교·범위 ──
("He could not stand without help after the accident. He could not walk, {0} run.",
 "그는 사고 후 부축 없이는 서지도 못했다. 걷지도 못했는데 뛰는 것은 말할 것도 없었다.",
 [(["let alone","in addition to","rather than","as well as","along with"],0)],
 "부정문 뒤에서 '~은 말할 것도 없이'. as well as를 넣으면 뛴다는 뜻이 되어 앞뒤가 어긋난다."),
("{0} price, the two models are nearly identical; the difference lies entirely in the"
 " warranty.",
 "가격에 관한 한 두 모델은 거의 같다. 차이는 전적으로 보증에 있다.",
 [(["When it comes to","Because of","In spite of","Thanks to","Instead of"],0)],
 "논의 범위를 한정한다."),
# ── 두 칸짜리 ──
("Optimistic patients report less distress during treatment. {0}, they also recover"
 " physical strength faster than pessimistic patients. {1}, patients who expect the worst"
 " tend to report more pain than their charts would predict.",
 "낙관적인 환자는 치료 중 고통을 덜 호소한다. 게다가 체력도 더 빨리 회복한다. 반면 최악을 예상하는 환자는 차트가 예측하는 것보다 더 큰 통증을 호소하는 경향이 있다.",
 [(["In addition","However","For example","Otherwise"],0),
  (["On the other hand","Therefore","Likewise","In short"],0)],
 "첫 칸은 같은 방향으로 한 걸음 더, 둘째 칸은 낙관과 비관을 맞세우는 자리다."),
("Handwriting notes is slower than typing them. {0}, students who wrote by hand recalled"
 " more of the lecture a week later. {1}, the slowness may be what forces them to"
 " summarize instead of transcribing.",
 "손으로 필기하는 것은 타자보다 느리다. 그런데도 손으로 쓴 학생들이 일주일 뒤 강의 내용을 더 많이 기억했다. 다시 말해 그 느림이야말로 받아적는 대신 요약하게 만드는 것일 수 있다.",
 [(["Nevertheless","Therefore","Similarly","Meanwhile"],0),
  (["In other words","By contrast","For instance","Nonetheless"],0)],
 "첫 칸은 불리한 조건에도 결과가 좋았다는 역접, 둘째 칸은 그 이유를 풀어 말하는 환언이다."),
("The city widened the main road to ease congestion. {0}, traffic volume rose to fill the"
 " new lanes within a year. {1}, adding capacity can end up producing the very jams it was"
 " meant to remove.",
 "그 도시는 정체를 풀려고 간선도로를 넓혔다. 그러나 1년 만에 교통량이 늘어 새 차선을 채웠다. 요컨대 용량을 늘리는 것이 없애려던 정체를 오히려 만들어 낼 수 있다.",
 [(["However","Accordingly","For example","Besides"],0),
  (["In short","On the contrary","Beforehand","Even so"],0)],
 "둘째 칸은 앞의 사례를 한 줄로 정리하는 자리다."),
]
