# -*- coding: utf-8 -*-
"""26 6모·9모에서 더 뽑은 낱말.

처음에는 어려움 기준(Zipf)만으로 걸렀는데, 그러면 두 가지가 빠진다.
  - 덩어리 표현: 낱말 하나하나는 흔한데 뜻은 합쳐도 안 나오는 것
    (take credit for · on the part of · be supposed to · an off day)
  - 다의어: 흔한 낱말이 뜻밖의 뜻으로 쓰인 것
    (alert 초롱초롱한 · setting 배경 · condition 질병 · engineer ~하게 만들다
     · executive 사무용의 · court 구애하다 · community 학계)
빈도로는 절대 안 걸리는 것들이라 손으로 골랐다.

예문은 그 낱말이 실린 문항의 지문에서 그대로 잘라 냈다. 문항 번호가 0인 것은
시험지에 그 표현이 안 나와서 직접 쓴 예문이고, 출처를 「추가」로 둔다 —
시험에서 따왔다고 적지 않는다.

(표제어, 뜻, 시험, 문항번호, 예문 덩어리, 밑줄 구간, 해석, 품사)
"""
R = [
# ── 26 6모 듣기 ──
("vice principal","교감","26 6모",1,"Owen, your vice principal","vice principal","너희 교감 Owen이다","phr"),
("palm tree","야자수","26 6모",4,"Do you see the palm tree on the beach","palm tree","해변에 있는 야자수 보이니","phr"),
("mess up","(일을) 망치다","26 6모",5,"really don't want to mess up in front of everyone","mess up","모두 앞에서 일을 망치고 싶지 않다","phr"),
("warm-up","준비 운동","26 6모",5,"I helped with the warm-up stretches","warm-up","준비 운동 스트레칭을 도왔다","n"),
("glass cleaner","유리 세정제","26 6모",6,"A bottle of glass cleaner is $5","glass cleaner","유리 세정제 한 병은 5달러다","phr"),
("paper towel","종이 행주","26 6모",6,"What types of paper towels do you have","paper towels","어떤 종류의 종이 행주가 있나요","phr"),
("day off","쉬는 날","26 6모",7,"Actually, I have the day off","day off","사실 나 그날 쉬는 날이야","phr"),
("flyer","(광고 안내용) 전단","26 6모",8,"could you look at this flyer","flyer","이 전단 좀 봐 줄래","n"),
("be really into","~에 푹 빠져 있다","26 6모",8,"I've been really into creating my own stories","really into","나만의 이야기를 만드는 데 푹 빠져 있었다","phr"),
("coffee beans","커피 원두","26 6모",13,"him a bag of coffee beans","coffee beans","그에게 커피 원두 한 봉지를","phr"),
("gift card","상품권","26 6모",13,"we get him a gift card for a cafe","gift card","그에게 카페 상품권을 사 주는 게","phr"),
("be grateful for","~에 감사하다","26 6모",14,"I'm grateful for your help","grateful for","네 도움에 감사한다","phr"),
("in charge of","~을 담당하는","26 6모",15,"teachers in charge of their school library","in charge of","학교 도서관을 담당하는 교사들","phr"),
# ── 26 6모 독해 ──
("carbon pricing","탄소 가격제","26 6모",17,"first country to introduce carbon pricing","carbon pricing","탄소 가격제를 처음 도입한 나라","phr"),
("net zero carbon economy","탄소 중립 경제","26 6모",17,"to achieve a net zero carbon economy by 2050","net zero carbon economy","2050년까지 탄소 중립 경제를 이루려면","phr"),
("reliance","의존","26 6모",17,"its reliance on fossil fuels and investing","reliance","화석 연료에 대한 그 나라의 의존","n"),
("source","에너지원, 공급원","26 6모",17,"its energy from carbon-free sources by 2030","sources","2030년까지 무탄소 공급원에서 얻는 에너지","n"),
("mining industry","광업","26 6모",18,"and worked in the mining industry","mining industry","그리고 광업에 종사했다","phr"),
("fishing pole","낚싯대","26 6모",19,"excitedly held onto the fishing pole","fishing pole","신이 나서 낚싯대를 붙잡았다","phr"),
("fishing line","낚싯줄","26 6모",19,"the fishing line suddenly became tense","fishing line","낚싯줄이 갑자기 팽팽해졌다","phr"),
("widen","(눈이) 커지다, 휘둥그레지다","26 6모",19,"Her eyes widened and her heart began to beat faster","widened","그녀의 눈이 휘둥그레졌고 심장이 더 빨리 뛰기 시작했다","v"),
("an off day","컨디션이 별로 안 좋은 날","26 6모",21,"your partner was having an off day","an off day","네 짝이 컨디션이 안 좋은 날이었다","phr"),
("no better than","~보다 나을 게 없는","26 6모",21,"you were climbing no better than usual","no better than","너는 평소보다 나을 게 없이 오르고 있었다","phr"),
("take credit for","~을 자신의 공으로 돌리다","26 6모",21,"on something you can take credit for","take credit for","네 공으로 돌릴 수 있는 무언가에 대해","phr"),
("constitute","~이 되다","26 6모",22,"three heads in a row constitutes a win","constitutes","앞면이 세 번 연속 나오면 승리가 된다","v"),
("on the part of","~에 의한","26 6모",22,"undetectable cheating on the part of the winning player","on the part of","이긴 선수에 의한 들키지 않는 속임수","phr"),
("alert","정신이 초롱초롱한","26 6모",23,"to keep you active and alert","alert","너를 활동적이고 정신이 초롱초롱하게 유지하려고","a"),
("be supposed to","~하기로 되어 있다","26 6모",23,"through them you are supposed to discover","supposed to","그것을 통해 너는 ~을 발견하기로 되어 있다","phr"),
("master's degree","석사 학위","26 6모",26,"with a master's degree in zoology","master's degree","동물학 석사 학위를 받고","phr"),
("main gate","정문","26 6모",28,"first mission at the main gate","main gate","정문에서 첫 임무를","phr"),
("fictional","허구의","26 6모",29,"making the fictional environment more","fictional","허구의 환경을 더 ~하게 만드는 데","a"),
("setting","배경","26 6모",29,"violence occurs in a contemporary setting","setting","폭력이 현대를 배경으로 일어나면","n"),
("distinctive","구별되는","26 6모",30,"cultivating a distinctive voice","distinctive","구별되는 목소리를 길러 내는 것","a"),
("gap","공백","26 6모",30,"gaps in existing research","gaps","기존 연구의 공백","n"),
("It's about","중요한 것은 ~이다","26 6모",30,"It's about balancing the expression of your ideas","It's about","중요한 것은 네 생각의 표현을 균형 잡는 일이다","phr"),
("novice","초보자","26 6모",31,"to the body of a novice ant","novice","초보 개미의 몸에","n"),
("lay down","(흔적·자취를) 남기다","26 6모",31,"as they lay down chemical trails","lay down","그들이 화학 흔적을 남기면서","phr"),
("social learning","사회적 학습","26 6모",31,"when describing social learning in animals","social learning","동물의 사회적 학습을 설명할 때","phr"),
("community","계, 집단","26 6모",31,"movement within the animal cognition community","community","동물 인지 학계 안의 흐름","n"),
("self-denying","자기 부정적인","26 6모",32,"sounds like a self-denying ordinance","self-denying","자기 부정적인 규정처럼 들린다","a"),
("computing power","연산력","26 6모",33,"redirecting all of our computing power","computing power","우리의 연산력을 전부 ~로 돌리는 것","phr"),
("motivational","동기의","26 6모",33,"we increase motivational intensity","motivational","동기의 강도를 높인다","a"),
("video conference","화상 회의","26 6모",33,"so that our video conference call won't lag","video conference","화상 회의 통화가 끊기지 않도록","phr"),
("take into consideration","~을 고려하다","26 6모",34,"requires taking into consideration population distributions","taking into consideration","인구 분포를 고려해야 한다","phr"),
("political organization","정치 구조","26 6모",34,"consideration of the political organization of territory","political organization","영토의 정치 구조에 대한 고려","phr"),
("accelerate","(속도가) 더 빨라지다","26 6모",35,"it appears that the rate of melting is accelerating","accelerating","녹는 속도가 더 빨라지고 있는 것으로 보인다","v"),
("genuine","진정한, 진짜의","26 6모",35,"A genuine glacier must be permanent","genuine","진짜 빙하는 영구적이어야 한다","a"),
("condition","질병","26 6모",36,"to at least 17 unhealthy conditions","conditions","적어도 열일곱 가지 건강하지 못한 질병으로","n"),
("engineer","~하게 만들다","26 6모",36,"Our modern world has engineered such activity out of our lives","engineered","현대 세계는 그런 활동을 우리 삶에서 밀어내도록 만들어 놓았다","v"),
("executive","사무용의","26 6모",37,"magnetic pendulum sold as an executive toy","executive","사무용 장난감으로 팔리는 자석 진자","a"),
("dear","소중히","26 6모",38,"to hold it dear","dear","그것을 소중히 여기려고","ad"),
("relive","다시 체험하다","26 6모",39,"they are reliving, at least in their imagination, the movement of their feet","reliving","적어도 상상 속에서는 발의 움직임을 다시 체험하고 있다","v"),
("social order","사회 질서","26 6모",40,"technology would upset the social order","social order","기술이 사회 질서를 뒤흔들 것이다","phr"),
("disturbing","불안하게 만드는","26 6모",40,"would be deeply disturbing to the social order","disturbing","사회 질서를 몹시 흔들어 놓을 것이다","a"),
("fulfilment","성취, 실현","26 6모",40,"this sense of fulfilment that some people are fortunate","fulfilment","어떤 사람들이 운 좋게 누리는 이 성취감","n"),
("aim to","~하는 것을 목표로 하다","26 6모",42,"an aspiration towards seamlessness aims to make the technological experience","aims to","이음매 없음을 향한 열망은 기술 경험을 ~하게 만드는 것을 목표로 한다","phr"),
("aspire to","~하기를 열망하다","26 6모",42,"we aspire to seamless aesthetics","aspire to","우리는 이음매 없는 미학을 열망한다","phr"),
("blend into","~에 녹아들다","26 6모",42,"blend seamlessly into our everyday lives","blend seamlessly into","우리 일상에 매끄럽게 녹아들다","phr"),
("seamlessly","매끄럽게","26 6모",42,"technological experience for humans blend seamlessly into our everyday lives","seamlessly","사람을 위한 기술 경험이 우리 일상에 매끄럽게 녹아들다","ad"),
# ── 26 9모 ──
("community center","주민 센터","26 9모",7,"you volunteer at a community center on the weekends","community center","너는 주말에 주민 센터에서 자원봉사를 한다","phr"),
("reading light","독서등","26 9모",8,"tables, chairs, and even reading lights","reading lights","탁자와 의자와 심지어 독서등까지","phr"),
("be on the list","명단에 있다","26 9모",11,"You're on the list","on the list","당신은 명단에 있습니다","phr"),
("shake","(몸을) 떨다","26 9모",19,"shook as she walked back and forth","shook","그녀는 앞뒤로 서성이며 떨었다","v"),
("horrible","형편없는, 끔찍한","26 9모",19,"she thinks my paintings are horrible","horrible","그녀가 내 그림이 형편없다고 생각하면","a"),
("court","구애하다","26 9모",31,"courting in the bower now appears larger","courting","바우어에서 구애하는 것이 이제 더 커 보인다","v"),
("extent","범위","26 9모",33,"Increasing the extent of forests in Britain","extent","영국에서 숲의 범위를 넓히는 것","n"),
# ── 시험지에 그 표현이 없어 직접 쓴 것 (출처 「추가」) ──
("hand out","~을 나눠 주다","26 6모",0,"I will hand out the worksheets before class.","hand out","수업 전에 학습지를 나눠 주겠다","phr"),
("think through","~을 충분히 생각하다","26 6모",0,"Think the plan through before you decide.","through","결정하기 전에 계획을 충분히 생각해 봐라","phr"),
("set apart","~을 차별화하다","26 6모",0,"Its design sets it apart from the rest.","apart","그 디자인이 나머지와 그것을 차별화한다","phr"),
("give a ride","(차를) 태워다 주다","26 9모",0,"Could you give me a ride to the station?","give me a ride","역까지 태워다 줄 수 있니","phr"),
("at the top of one's game","기량이 최고인","26 6모",0,"She was at the top of her game that season.","at the top of her game","그 시즌에 그녀는 기량이 최고였다","phr"),
]
