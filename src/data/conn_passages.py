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

P += [
# ── 역접 · 대조 ──
("Everyone in the office assumed the quiet intern had nothing to contribute. {0}, it was"
 " her memo that reshaped the entire proposal.",
 "사무실 사람들은 조용한 인턴이 기여할 게 없다고 여겼다. 그런데 제안서 전체를 다시 짜게 만든 것은 그녀의 메모였다.",
 [(["In fact","For instance","As a result","Likewise","In short"],0)],
 "앞의 짐작을 사실로 뒤집는다. in fact는 '사실은 그 반대'라는 신호다."),
("Aluminum is light enough to float on mercury. {0}, it is strong enough to carry the"
 " weight of an aircraft.",
 "알루미늄은 수은 위에 뜰 만큼 가볍다. 그런데도 항공기의 무게를 견딜 만큼 튼튼하다.",
 [(["Yet","Thus","Namely","For example","Meanwhile"],0)],
 "가볍다와 튼튼하다를 맞세운다. thus를 넣으면 가벼워서 튼튼하다는 말이 되어 어긋난다."),
("Older maps placed the river two kilometers to the east. {0}, satellite images show it"
 " has barely moved in three centuries.",
 "옛 지도들은 그 강을 동쪽으로 2킬로미터 떨어진 곳에 그렸다. 반면 위성 사진은 3세기 동안 강이 거의 움직이지 않았음을 보여 준다.",
 [(["By contrast","Accordingly","That is","In addition","Eventually"],0)],
 "옛 자료와 새 자료를 맞세우는 자리."),
# ── 인과 ──
("Antibiotics kill the helpful bacteria in the gut along with the harmful ones. {0}, many"
 " patients develop digestive trouble during a long course of treatment.",
 "항생제는 해로운 세균과 함께 장 속 이로운 세균까지 죽인다. 그래서 장기 치료 중에 소화 장애를 겪는 환자가 많다.",
 [(["For this reason","In contrast","For example","Even so","Previously"],0)],
 "앞이 원인, 뒤가 결과. for example을 넣으면 사례가 되어 논리가 어긋난다."),
("The factory sat directly above the aquifer that supplied the town. {0}, a single leak"
 " would have contaminated the drinking water of forty thousand people.",
 "그 공장은 마을에 물을 대는 대수층 바로 위에 있었다. 따라서 누출 한 번이면 4만 명의 식수가 오염될 수 있었다.",
 [(["Therefore","Nevertheless","Similarly","Namely","Afterward"],0)],
 "위치가 원인이고 위험이 결과다."),
# ── 첨가 ──
("Walking to work costs nothing and needs no equipment. {0}, it gives the body the kind of"
 " steady movement that gym sessions rarely provide.",
 "걸어서 출근하면 돈도 장비도 들지 않는다. 더욱이 헬스장에서는 좀처럼 얻기 어려운 꾸준한 움직임을 몸에 준다.",
 [(["What is more","On the contrary","For example","Otherwise","In brief"],0)],
 "장점을 하나 더 얹는다."),
("The library extended its hours through the exam period. {0}, it opened three additional"
 " study rooms on the upper floor.",
 "도서관은 시험 기간 내내 운영 시간을 늘렸다. 또한 위층에 열람실 세 곳을 더 열었다.",
 [(["Furthermore","However","That is","As a result","Formerly"],0)],
 "같은 방향의 조치를 나란히 놓는다."),
# ── 예시 · 환언 ──
("Animals that live in complete darkness often lose the organs they no longer use. {0},"
 " cave fish are born with eye sockets but never develop working eyes.",
 "완전한 어둠 속에 사는 동물은 더 이상 쓰지 않는 기관을 잃는 일이 많다. 예를 들어 동굴 물고기는 눈구멍을 갖고 태어나지만 기능하는 눈은 끝내 생기지 않는다.",
 [(["For instance","Consequently","On the other hand","In conclusion","Until then"],0)],
 "일반 진술 뒤에 구체 사례가 온다."),
("The contract binds the buyer for a full decade with no exit clause. {0}, whoever signs"
 " it is committing the company until 2036.",
 "그 계약은 해지 조항 없이 매수인을 꼬박 10년간 묶는다. 다시 말해 서명하는 사람은 회사를 2036년까지 묶는 셈이다.",
 [(["That is to say","By contrast","For example","Nonetheless","Meanwhile"],0)],
 "앞 내용을 풀어 다시 말한다."),
# ── 양보 ──
("{0} the technology has existed since the 1970s, it became affordable only in the last"
 " five years.",
 "그 기술은 1970년대부터 있었지만 값이 감당할 만해진 것은 최근 5년 사이다.",
 [(["Even though","Because","As long as","Now that","In case"],0)],
 "오래 존재했다는 사실을 인정하고 뒤집는다."),
("{0} its reputation for difficulty, the course attracts more applicants every year.",
 "어렵다는 평판에도 불구하고 그 강의는 해마다 지원자가 는다.",
 [(["Despite","Because of","Thanks to","In terms of","Along with"],0)],
 "어렵다는데도 지원자가 는다. because of를 넣으면 논리가 반대가 된다."),
# ── 조건 ──
("Water the plant only when the top inch of soil is dry. {0}, the roots will sit in"
 " moisture and begin to rot.",
 "흙 위쪽 2~3센티가 말랐을 때만 물을 줘라. 그러지 않으면 뿌리가 젖은 채로 있다가 썩기 시작한다.",
 [(["If not","Even so","That is","In addition","Beforehand"],0)],
 "앞 조건을 지키지 않았을 때를 말한다."),
("{0} the committee had met one week earlier, the decision would have come before the"
 " budget was fixed.",
 "위원회가 일주일만 일찍 모였더라면 예산이 확정되기 전에 결정이 났을 것이다.",
 [(["Had","Because","Unless","Since","While"],0)],
 "가정법 과거완료의 if 생략 도치. 뒤의 would have come이 단서다."),
# ── 시간 ──
("The seeds lay dormant in the soil for nearly forty years. {0}, a single fire cleared the"
 " canopy and the whole slope turned green in one season.",
 "씨앗은 거의 40년을 흙 속에서 잠자고 있었다. 그러다 화재 한 번이 우거진 숲을 걷어내자 비탈 전체가 한 철 만에 초록으로 변했다.",
 [(["Then","Therefore","In other words","Likewise","Regardless"],0)],
 "긴 시간 뒤에 벌어진 일을 잇는다."),
("Check that the power is disconnected. {0} removing the panel, photograph the wiring so"
 " you can put it back exactly as it was.",
 "전원이 차단됐는지 확인하라. 패널을 떼기 전에 배선을 사진으로 찍어 두면 그대로 되돌릴 수 있다.",
 [(["Before","After","Instead of","Despite","Because of"],0)],
 "순서를 정하는 자리. 사진은 떼기 전에 찍어야 한다."),
# ── 비교 · 범위 ──
("The two drugs lower blood pressure by almost the same amount. {0} side effects, however,"
 " the newer one is far easier to tolerate.",
 "두 약은 혈압을 거의 같은 정도로 낮춘다. 다만 부작용에 관해서는 새 약이 훨씬 견디기 쉽다.",
 [(["As for","Because of","Thanks to","In spite of","Instead of"],0)],
 "논의 범위를 부작용으로 좁힌다."),
("She did not merely finish the race; {0}, she set a course record that still stands.",
 "그녀는 완주에 그친 게 아니라 오히려 지금도 깨지지 않은 코스 기록을 세웠다.",
 [(["rather","therefore","for example","similarly","meanwhile"],0)],
 "not merely A 뒤에서 더 강한 쪽으로 밀어 올린다."),
# ── 강조 · 태도 ──
("The committee rejected every proposal that mentioned cost. {0}, the one proposal it"
 " approved never once used the word.",
 "위원회는 비용을 언급한 제안을 모두 물리쳤다. 실제로 승인한 단 하나의 제안은 그 단어를 한 번도 쓰지 않았다.",
 [(["Indeed","Otherwise","In contrast","For example","Beforehand"],0)],
 "앞 진술을 한층 강하게 못 박는다."),
("The bridge was designed to last a century. {0}, it was closed for structural repairs"
 " within eleven years of opening.",
 "그 다리는 100년을 가도록 설계됐다. 역설적이게도 개통 11년 만에 구조 보수를 위해 폐쇄됐다.",
 [(["Ironically","Naturally","Likewise","Accordingly","Subsequently"],0)],
 "설계 의도와 정반대 결과. 필자의 시선이 담긴 말이다."),
# ── 두 칸짜리 ──
("Sleep does more than rest the body. {0}, it is during deep sleep that the brain clears"
 " waste proteins built up while awake. {1}, people who sleep badly for long stretches show"
 " higher levels of those same proteins.",
 "잠은 몸을 쉬게 하는 것 이상이다. 사실 깨어 있는 동안 쌓인 노폐물 단백질을 뇌가 치우는 것은 깊은 잠에 들었을 때다. 따라서 오래 잠을 설친 사람은 바로 그 단백질 수치가 높게 나타난다.",
 [(["In fact","However","Otherwise","By contrast"],0),
  (["Accordingly","Nevertheless","For example","In short"],0)],
 "첫 칸은 앞 문장을 강하게 받고, 둘째 칸은 그로부터 따라 나오는 결과다."),
("Paper maps force you to see where a place sits in relation to everything around it."
 " {0}, a phone screen shows only the next turn. {1}, drivers who rely on turn-by-turn"
 " directions remember routes far less well.",
 "종이 지도는 어떤 장소가 주변과 어떤 관계에 있는지 보게 만든다. 반면 휴대폰 화면은 다음 갈림길만 보여 준다. 그래서 길 안내에만 의존한 운전자는 경로를 훨씬 덜 기억한다.",
 [(["By contrast","Likewise","For instance","That is"],0),
  (["As a result","Even so","On the contrary","Beforehand"],0)],
 "첫 칸은 종이 지도와 화면을 맞세우고, 둘째 칸은 그 차이가 낳은 결과를 잇는다."),
("Museums once competed on the size of their collections. {0}, the measure of success has"
 " shifted to how long visitors stay in a single room. {1}, a gallery with twenty objects"
 " may now be judged better than one with two hundred.",
 "박물관들은 한때 소장품 규모로 겨루었다. 그러나 성공의 잣대는 관람객이 한 전시실에 얼마나 오래 머무는가로 옮겨 갔다. 다시 말해 스무 점짜리 전시실이 이백 점짜리보다 낫다고 평가될 수도 있다.",
 [(["However","Therefore","Similarly","In addition"],0),
  (["In other words","By contrast","Nevertheless","Meanwhile"],0)],
 "첫 칸은 과거와 현재를 꺾고, 둘째 칸은 그 기준을 구체적으로 풀어 말한다."),
("A vaccine does not fight the virus directly. {0}, it teaches the immune system what the"
 " virus looks like. {1}, protection appears only after the body has had time to learn,"
 " usually two weeks or more.",
 "백신은 바이러스와 직접 싸우지 않는다. 그 대신 면역계에 바이러스의 생김새를 가르친다. 그러므로 보호 효과는 몸이 배울 시간을 가진 뒤에야, 보통 2주 넘어서야 나타난다.",
 [(["Instead","Moreover","For example","Likewise"],0),
  (["Consequently","However","That is","Beforehand"],0)],
 "첫 칸은 앞의 부정을 받아 대안을 제시하고, 둘째 칸은 결과를 잇는다."),
("Most people can name the year they graduated but not the year a friend did. {0}, memory"
 " is organized around the self rather than around dates. {1}, asking someone when an event"
 " happened often works better if you first ask where they were living at the time.",
 "대부분은 자기가 졸업한 해는 말해도 친구가 졸업한 해는 못 말한다. 요컨대 기억은 날짜가 아니라 자기 자신을 중심으로 정리된다. 그래서 어떤 일이 언제 있었는지 물을 때는 그때 어디 살았는지를 먼저 묻는 편이 낫다.",
 [(["In short","However","For example","Otherwise"],0),
  (["For this reason","By contrast","Even so","Previously"],0)],
 "첫 칸은 사례를 한 줄로 정리하고, 둘째 칸은 거기서 나오는 실천을 잇는다."),
]
