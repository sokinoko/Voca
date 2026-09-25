# -*- coding: utf-8 -*-
"""2026학년도 9월 모의평가 영어 — 단어장에 넣을 항목.

뜻(m)은 평가원 해설지의 [Words and Phrases]에서 그대로 가져왔다.
예문(x)은 시험지·듣기 대본의 실제 문장에서 잘라 냈다. 영어는 손대지 않고
PDF가 낱말 안에 넣은 공백과 문항 기호(①②③)만 걷어냈다(src/tools/pdftext.py).
굽은 따옴표(U+2019)만 곧은 따옴표로 바꿨다 — 저장소 규칙이다.
해석(xt)은 그 덩어리를 옮긴 것이다.

문항 번호는 그 낱말의 뜻이 실린 해설지 블록의 번호이고, 예문도 같은 문항의
지문에서만 가져왔다(묶음 문항은 그 묶음 안에서). 출처를 옮겨 붙이지 않는다.

넣지 않은 것:
- flyer · readership · relavance(해설지 오타) — 시험지·대본에 그 낱말이 없어
  예문을 만들 수 없다.
- norms · permanently — 이미 있는 norm · permanent와 같은 낱말이다. 복수형과
  부사형만 다른 것은 새 항목으로 만들지 않는다. 반면 exhausting은 이미 있는
  exhausted와 -ing/-ed가 갈리는 자리라 그대로 둔다.
- 사람 이름과 지명.

(표제어, 뜻, 문항번호, 예문 덩어리, 밑줄 구간, 해석)
"""
R = [
# ── 듣기 (1~17번) ──
("protective film","보호 필름",1,"you'll also get watchbands and protective films at lower prices","protective films","시계 밴드와 보호 필름도 더 싼 값에 받게 된다"),
("tempo","박자",2,"listening to fast tempo music","tempo","빠른 박자의 음악을 듣는 것"),
("heartbeat","심장박동, 심박",2,"Fast tempo music can raise your heartbeat","heartbeat","빠른 박자의 음악은 심장박동을 높일 수 있다"),
("distracted","(주의가) 산만한",2,"make you focus on running and get less distracted","distracted","달리기에 집중하게 하고 덜 산만하게 만들다"),
("smoothly","순조롭게",3,"the conversation should go smoothly","smoothly","대화가 순조롭게 흘러갈 것이다"),
("microwave","전자레인지",4,"there are two microwaves on the table","microwaves","탁자 위에 전자레인지가 두 대 있다"),
("star-patterned","별무늬의",4,"a baby bed with a star-patterned pad next to the wall","star-patterned","벽 옆에 별무늬 패드가 깔린 아기 침대"),
("heart-shaped","하트 모양의",4,"Look at the heart-shaped cushion on the sofa","heart-shaped","소파에 있는 하트 모양 쿠션을 봐"),
("nursing room","수유실",4,"But do they have a nursing room","nursing room","그런데 거기에 수유실이 있을까"),
("heat up","데우다",4,"Let's heat up the baby food there","heat up","거기서 이유식을 데우자"),
("head out to","~로 출발하다, ~로 가다",4,"Now, let's head out to the mall","head out to","이제 쇼핑몰로 출발하자"),
("confirmation","확인서, 확인",5,"I have a confirmation from the hotel","confirmation","호텔에서 받은 확인서가 있다"),
("ferry","페리, (사람·차량 등을 운반하는) 연락선",5,"Did you buy tickets for a ferry to the island","ferry","섬으로 가는 페리 표를 샀니"),
("sort out","~을 정리하다",5,"I'm glad everything is finally sorted out","sorted out","드디어 모든 게 정리되어 기쁘다"),
("biology","생물학",7,"Is it because of your biology report","biology","생물학 보고서 때문이니"),
("gardening","정원 가꾸기, 원예",9,"a market selling gardening tools","gardening","정원 가꾸기 도구를 파는 장터"),
("feel stuck","갇혀 있다는 느낌이 들다",9,"Are you feeling stuck in the city","feeling stuck","도시에 갇혀 있다는 느낌이 드니"),
("pricey","비싼",10,"I think it's too pricey","pricey","너무 비싼 것 같다"),
("water-resistant","방수의",10,"I like the water-resistant one better","water-resistant","방수되는 것이 더 좋다"),
("checkup","건강검진",11,"ask about my regular health checkup tomorrow morning","checkup","내일 아침 정기 건강검진에 대해 문의하다"),
("empty stomach","공복",11,"I need to have an empty stomach for my checkup","empty stomach","검진을 받으려면 공복이어야 한다"),
("subscriber","구독자",13,"checking the number of subscribers to my social media channel","subscribers","내 소셜 미디어 채널 구독자 수를 확인하는 중이다"),
("dormitory","기숙사",14,"Are you in your dormitory room","dormitory","기숙사 방에 있니"),
("fire drill","소방 훈련",14,"a fire drill will be happening in our dormitory soon","fire drill","곧 우리 기숙사에서 소방 훈련이 있을 것이다"),
("get through","~을 통과하다",14,"have a problem getting through the hallways during the drill","getting through","훈련 중에 복도를 통과하는 데 어려움을 겪다"),
("recipe","조리[요리]법",15,"she can't find its recipe","recipe","그녀는 그 조리법을 찾지 못한다"),
("jaw","턱",17,"First of all, human jaws gradually became smaller","jaws","우선 인간의 턱이 점차 작아졌다"),
("gradually","점차, 서서히",17,"human jaws gradually became smaller","gradually","인간의 턱이 점차 작아졌다"),
("chew","(음식을) 씹다",17,"humans didn't need the same powerful chewing ability in their jaws","chewing","인간은 턱에 그만큼 강한 씹는 능력이 필요하지 않았다"),
("heel","발뒤꿈치",17,"Lastly, human heels became thicker","heels","마지막으로 인간의 발뒤꿈치가 더 두꺼워졌다"),
("impact","충격",17,"thicker heels to better absorb the impact from each step","impact","걸음마다 오는 충격을 더 잘 흡수하기 위한 더 두꺼운 발뒤꿈치"),
# ── 독해 (18~45번) ──
("enroll","등록하다",18,"more participants enrolled in our program than we expected","enrolled","예상보다 많은 참가자가 우리 프로그램에 등록했다"),
("enthusiasm","열정, 열의",18,"I am excited about your enthusiasm for expanding your familiarity with AI","enthusiasm","AI에 대한 이해를 넓히려는 네 열정이 반갑다"),
("assignment","과제",19,"she had turned in her art assignment","assignment","그녀는 미술 과제를 제출했다"),
("exclaim","탄성을 지르다, 외치다",19,"Sierra smiled brightly as she exclaimed","exclaimed","Sierra는 탄성을 지르며 환하게 웃었다"),
("abusive language","욕설, 폭언",20,"Showing up late for work and using abusive language","abusive language","지각하는 것과 욕설을 쓰는 것"),
("unaware","모르는",20,"they were unaware their behavior was undesirable","unaware","자기 행동이 바람직하지 않다는 것을 모르고 있었다"),
("uninformed","정보가 부족한, 무지한",20,"distinguish bad apples from merely uninformed apples","uninformed","나쁜 사과와 그저 정보가 부족한 사과를 구분하다"),
("unintentional","의도하지 않은",20,"many problems are unintentional failings","unintentional","많은 문제는 의도하지 않은 잘못이다"),
("circularity","순환성",21,"leads to the notion of circularity in pitch perception","circularity","음 높이 지각에서 순환성이라는 개념으로 이어지다"),
("continuum","연속체",21,"red and violet fall at opposite ends of the continuum","continuum","빨강과 보라는 연속체의 양 끝에 놓인다"),
("electromagnetic","전자기의",21,"visible frequencies of electromagnetic energy","electromagnetic","전자기 에너지의 눈에 보이는 주파수"),
("octave","옥타브",21,"a frequency ratio of 2:1 or 1:2, is called the octave","octave","2 대 1 또는 1 대 2의 주파수 비를 옥타브라고 한다"),
("correspond to","~에 상응하다",21,"a perceptual phenomenon that corresponds to the doubling and halving of frequencies","corresponds to","주파수가 두 배나 절반이 되는 것에 상응하는 지각 현상"),
("mutuality","상호성",22,"built on mutuality and sharing of identity","mutuality","상호성과 정체성의 공유에 기반한"),
("straightforward","직접적인, 확실한",22,"is rather simple and straightforward","straightforward","다소 단순하고 확실하다"),
("social capital","사회적 자본",22,"We increase our social capital when we successfully engage in social media","social capital","소셜 미디어를 잘 활용하면 사회적 자본이 늘어난다"),
("job lead","일자리 정보",22,"We build ties that may pay off with a job lead","job lead","일자리 정보로 돌아올 수 있는 연결을 만든다"),
("a letter of recommendation","추천서",22,"pay off with a job lead or a letter of recommendation","a letter of recommendation","일자리 정보나 추천서로 돌아오다"),
("stress","강조하다",22,"Lin's work stresses that it is who you know as much as what you know","stresses","Lin의 연구는 무엇을 아는지 만큼 누구를 아는지가 중요하다고 강조한다"),
("assertion","단언, 주장",23,"such rhetorical acts as assertion, justification, judgment, conviction","assertion","단언, 정당화, 판단, 확신 같은 수사적 행위"),
("justification","정당화",23,"such rhetorical acts as assertion, justification, judgment","justification","단언, 정당화, 판단 같은 수사적 행위"),
("biographer","전기 작가",23,"the life narrator and the biographer engage different kinds of evidence","biographer","삶을 쓰는 화자와 전기 작가는 서로 다른 종류의 근거를 다룬다"),
("commentary","해설, 논평",23,"or offer commentary on their personalized acts of remembering","commentary","개인화된 기억 행위에 논평을 붙이다"),
("validity","타당성, 유효성",23,"family archives, which they evaluate for validity","validity","그들이 타당성을 따져 보는 집안의 기록"),
("height","정점, 절정",24,"At the height of their activities and influence","height","그들의 활동과 영향력이 정점에 이르렀을 때"),
("civil","시민의, 세속의",24,"intellectual leadership for the institutions of Church and civil governments","civil","교회와 세속 정부의 제도를 이끄는 지적 지도력"),
("provision","공급, 제공",24,"innovation in religious thought and practice, medical provision, education","provision","종교 사상과 실천의 혁신, 의료 제공, 교육"),
("self-imposed","스스로 부과한, 자진한",24,"while apparently observing self-imposed isolation from the wider community","self-imposed","더 넓은 공동체로부터 스스로 부과한 격리를 지키면서"),
("observance","(종교) 의식, (법·규율·의식의) 준수",24,"a permanent rhythm of religious observance, prayer and study","observance","종교 의식과 기도와 공부의 변함없는 리듬"),
("deliverance","구원",24,"as well as for their own deliverance","deliverance","그들 자신의 구원을 위해서도"),
("parallel","나란한, 평행하는",24,"Monks were regarded as leading parallel lives","parallel","수도사들은 나란한 삶을 사는 것으로 여겨졌다"),
("electronics","전자제품",25,"read online reviews the most, by percentage, before buying electronics","electronics","전자제품을 사기 전에 비율상 온라인 후기를 가장 많이 읽었다"),
("by percentage","비율상",25,"people from each age group tended to read online reviews the most, by percentage","by percentage","각 연령대에서 비율상 온라인 후기를 가장 많이 읽는 경향이 있었다"),
("household appliance","(냉장고, 세탁기, 전자레인지 등) 가전제품",25,"For people who read online reviews before purchasing household appliances","household appliances","가전제품을 사기 전에 온라인 후기를 읽는 사람들의 경우"),
("biography","전기",26,"A biography written about his life called him","biography","그의 삶에 대해 쓰인 전기는 그를 ~라고 불렀다"),
("master","석사",26,"he started his master's program in electrical engineering","master's","그는 전기공학 석사 과정을 시작했다"),
("rediscover","다시 발견하다",27,"you can rediscover forgotten rhythms of your life","rediscover","잊고 있던 삶의 리듬을 다시 발견할 수 있다"),
("accessible","이용할 수 있는",27,"but common restrooms easily accessible","accessible","다만 공용 화장실은 쉽게 이용할 수 있다"),
("craft","짓다, 다듬다",27,"Lodging: Beautifully crafted bungalow","crafted","숙소: 아름답게 지은 방갈로"),
("fill out","~을 작성하다",27,"fill out the application form online","fill out","온라인으로 신청서를 작성하다"),
("marine","해양의",28,"Design a unique marine animal mascot","marine","독특한 해양 동물 마스코트를 디자인하시오"),
("additive","첨가물",29,"has had no additives, preservatives or synthetic ingredients added","additives","첨가물이나 방부제, 합성 재료가 들어간 적이 없다"),
("preservative","방부제",29,"no additives, preservatives or synthetic ingredients added","preservatives","첨가물이나 방부제, 합성 재료가 들어가지 않은"),
("synthetic","합성의",29,"no additives, preservatives or synthetic ingredients added","synthetic","첨가물이나 방부제, 합성 재료가 들어가지 않은"),
("processor","가공업자",29,"not by the bees, but by human processors and distributors","processors","벌이 아니라 사람인 가공업자와 유통업자에 의해"),
("distributor","유통업자",29,"by human processors and distributors in stages","distributors","사람인 가공업자와 유통업자에 의해 단계적으로"),
("in stages","단계적으로",29,"by human processors and distributors in stages after the honey has been collected","in stages","꿀을 모은 뒤에 사람인 가공업자와 유통업자에 의해 단계적으로"),
("retailer","소매상",29,"this is an important consideration for producers and retailers","retailers","이것은 생산자와 소매상에게 중요한 고려 사항이다"),
("uniform","균일한",29,"also gives a more uniform flavour","uniform","또한 더 균일한 맛을 낸다"),
("liken","비유하다",30,"One way to visualize its spirit is to liken it to a footpath in the forest","liken","그 정신을 떠올리는 한 가지 방법은 숲의 오솔길에 비유하는 것이다"),
("footpath","오솔길",30,"Suppose a tree falls across a footpath","footpath","나무 한 그루가 오솔길을 가로질러 쓰러졌다고 해 보자"),
("trail","오솔길, 길",30,"A soft-path response would be simply to redirect the trail around the fallen tree","trail","부드러운 방식의 대응은 그저 쓰러진 나무를 돌아 길을 돌리는 것이다"),
("interventionist","개입적인",30,"A still more interventionist response might be to straighten and pave the path","interventionist","더 개입적인 대응은 길을 곧게 펴고 포장하는 것이다"),
("pave","포장하다",30,"might be to straighten and pave the path","pave","길을 곧게 펴고 포장하는 것"),
("superhighway","초고속도로",30,"create a superhighway that removes the landscape","superhighway","풍경을 제거해 버리는 초고속도로를 만들다"),
("obstacle","장애물",30,"bulldozes straight through all obstacles in the topography","obstacles","지형의 모든 장애물을 곧장 밀고 나간다"),
("bulldoze through","~을 밀고 나가다",30,"bulldozes straight through all obstacles in the topography","bulldozes straight through","지형의 모든 장애물을 곧장 밀고 나간다"),
("modesty","겸손",30,"modesty with respect to what we actually know about river movement","modesty","강의 흐름에 대해 우리가 실제로 아는 것에 관한 겸손"),
("variability","변동성",30,"soft-path engineering accepts variability in the river's movement","variability","부드러운 방식의 공학은 강 흐름의 변동성을 받아들인다"),
("insignificant","하찮은",30,"insignificant until proven otherwise","insignificant","달리 증명되기까지는 하찮은"),
("backwater","지류",30,"Backwaters, short-lived wetlands, braids and channels, swamps","Backwaters","지류, 잠시 생기는 습지, 갈래와 수로, 늪지"),
("wetland","습지",30,"Backwaters, short-lived wetlands, braids and channels","wetlands","지류, 잠시 생기는 습지, 갈래와 수로"),
("braid","갈래",30,"short-lived wetlands, braids and channels, swamps","braids","잠시 생기는 습지, 갈래와 수로, 늪지"),
("channel","수로",30,"short-lived wetlands, braids and channels, swamps","channels","잠시 생기는 습지, 갈래와 수로, 늪지"),
("swamp","늪지",30,"wetlands, braids and channels, swamps","swamps","습지, 갈래와 수로, 늪지"),
("undesirable","바람직하지 않은",30,"all undesirable to hard-path engineering","undesirable","단단한 방식의 공학에는 모두 바람직하지 않은"),
("presume","간주하다, 추정하다",30,"are presumed by soft-path engineers to be ecologically important","presumed","부드러운 방식의 공학자들은 생태적으로 중요하다고 간주한다"),
("bower","바우어(수컷 새가 암컷을 유혹하려고 화려하게 꾸민 집)",31,"The larger objects are placed closer to the bower","bower","더 큰 물건이 바우어에 더 가깝게 놓인다"),
("decorate","장식하다",31,"The males decorate the avenue with a variety of objects","decorate","수컷들은 그 길을 온갖 물건으로 장식한다"),
("chaotic","무질서한",31,"But they do not do so in a chaotic manner","chaotic","하지만 그들은 무질서하게 그러지는 않는다"),
("burnout","쇠진, 소모",32,"empathy can be exhausting and lead to burnout","burnout","공감은 소모적일 수 있고 쇠진으로 이어질 수 있다"),
("exhausting","소모적인",32,"empathy can be exhausting and lead to burnout","exhausting","공감은 소모적일 수 있고 쇠진으로 이어질 수 있다"),
("insensitivity","무감각",32,"lead to burnout, insensitivity to suffering, or worse","insensitivity","쇠진이나 고통에 대한 무감각, 더 나쁜 것으로 이어지다"),
("mentality","사고방식",32,"force us into an us vs. them mentality","mentality","우리 대 그들이라는 사고방식으로 우리를 밀어 넣다"),
("prescription","처방, 규정",32,"Thus, the prescription for more empathy","prescription","따라서 공감을 더 하라는 처방"),
("public figure","공인, 유명 인사",32,"empathy is widely praised by scholars and public figures","public figures","공감은 학자와 공인들에게 널리 칭송받는다"),
("meadow","목초지",33,"Wetlands, meadows, and grasslands have a unique biota too","meadows","습지와 목초지와 초원에도 고유한 생물상이 있다"),
("grassland","초원",33,"Wetlands, meadows, and grasslands have a unique biota","grasslands","습지와 목초지와 초원에도 고유한 생물상이 있다"),
("drain","배수하다",33,"the Forestry Commission has drained, fertilized, and fenced extensive areas of wetlands","drained","산림위원회는 넓은 습지를 배수하고 기름지게 하고 울타리를 쳤다"),
("be composed of","~로 구성되다",33,"the forests established are usually composed of exotic trees","composed of","조성된 숲은 대개 외래 나무로 구성된다"),
("anonymity","익명성",34,"Anonymity requires that the collective choice ought to be independent of the agents' identities","Anonymity","익명성은 집단의 선택이 행위자의 신분과 무관해야 한다고 요구한다"),
("neutrality","중립성",34,"whereas neutrality requires impartiality towards the alternatives","neutrality","반면 중립성은 선택지에 대한 공정성을 요구한다"),
("impartiality","공정성",34,"neutrality requires impartiality towards the alternatives","impartiality","중립성은 선택지에 대한 공정성을 요구한다"),
("deterministic","결정적인, 결정론적인",34,"necessitate deterministic systems of selecting voters blindly","deterministic","투표자를 무작위로 고르는 결정론적 방식을 필요로 하다"),
("preference","선호",34,"When gathering the preferences of multiple agents into one collective choice","preferences","여러 행위자의 선호를 하나의 집단적 선택으로 모을 때"),
("psychosocial","심리사회적인",35,"Mentors also provide much needed psychosocial support","psychosocial","멘토는 꼭 필요한 심리사회적 지지도 제공한다"),
("interruption","방해, 중단",36,"have students write about the topic without interruption","interruption","학생들이 방해 없이 그 주제에 대해 쓰게 한다"),
("evaluation","평가",36,"Process writing shifts the emphasis in teaching writing from evaluation to revision","evaluation","과정 중심 글쓰기는 글쓰기 교육의 무게를 평가에서 수정으로 옮긴다"),
("revision","수정, 교정",36,"shifts the emphasis in teaching writing from evaluation to revision","revision","글쓰기 교육의 무게를 평가에서 수정으로 옮긴다"),
("colleague","동료",37,"have to rely on discussions with colleagues to properly understand problems","colleagues","문제를 제대로 이해하려면 동료와의 논의에 의존해야 한다"),
("notation","(특히 수학·과학·음악에서) 기호[표기법]",37,"The complicated notations that might spring to mind","notations","머리에 떠오를 만한 복잡한 기호들"),
("rest assured","안심하다",37,"rest assured, even professional mathematicians sometimes have to rely on discussions","rest assured","안심해도 된다, 전문 수학자조차 때로 논의에 의존해야 한다"),
("mathematician","수학자",37,"even professional mathematicians sometimes have to rely on discussions with colleagues","mathematicians","전문 수학자조차 때로 동료와의 논의에 의존해야 한다"),
("canopy","수관(樹冠)",38,"would struggle to survive through a harsh winter if it retained its canopy of leaves","canopy","잎의 수관을 그대로 두면 혹독한 겨울을 버티기 어려울 것이다"),
("initiate","시작하다, 착수하다",38,"the tree initiates an active process of clever recycling","initiates","나무는 영리한 재활용이라는 적극적인 과정을 시작한다"),
("surgical","외과적인, 매우 정밀한",38,"and then, with surgical precision, block up that pathway into the leaves","surgical","그다음 매우 정밀하게 잎으로 가는 그 통로를 막는다"),
("precision","정밀함, 정확성",38,"with surgical precision, block up that pathway into the leaves","precision","매우 정밀하게 잎으로 가는 그 통로를 막다"),
("snap","끊어지다, 부러지다",38,"in the wind, the leaves snap off and fall to the ground","snap","바람이 불면 잎이 끊어져 땅으로 떨어진다"),
("architectural","건축의",39,"In architectural history this evidence may take the form of the buildings themselves","architectural","건축의 역사에서 이 근거는 건물 자체의 형태를 띨 수 있다"),
("multitude","수많은",39,"is derived from a multitude of sources","multitude","수많은 자료에서 나온다"),
("serialize","연재하다",40,"comics, which are typically serialized in newspaper strips or comic books","serialized","보통 신문 연재만화나 만화책으로 연재되는 만화"),
("ambiguous","모호한",42,"successful managers would choose rich media for confusing or ambiguous messages","ambiguous","성공한 관리자는 혼란스럽거나 모호한 메시지에 풍부한 매체를 고를 것이다"),
("lean","빈약한, 부족한",42,"and lean or less rich media for messages","lean","그리고 메시지에는 빈약하거나 덜 풍부한 매체를"),
("videoconferencing","화상 회의",42,"Videoconferencing would be considered richer than the phone","Videoconferencing","화상 회의는 전화보다 더 풍부하다고 여겨질 것이다"),
("replicate","복제하다",42,"making it closer to replicating a perceived gold standard of face-to-face","replicating","대면이라는 인식된 최고 기준을 복제하는 데 더 가깝게 만들다"),
("social presence","사회적 실재감",42,"How Has Social Presence Evolved with Social Channels","Social Presence","사회적 실재감은 사회적 매체와 함께 어떻게 변해 왔는가"),
("fireworks","불꽃(놀이)",45,"Fireworks filled the sky, and the team song played throughout the stadium","Fireworks","불꽃놀이가 하늘을 메웠고 팀 노래가 경기장에 울려 퍼졌다"),
("cheer for","~를 응원하다",45,"Mike and his dad cheered for their team's players","cheered for","Mike와 아빠는 자기 팀 선수들을 응원했다"),
]

POS = {
 "protective film":"phr","tempo":"n","heartbeat":"n","distracted":"a","smoothly":"ad",
 "microwave":"n","star-patterned":"a","heart-shaped":"a","nursing room":"phr",
 "heat up":"phr","head out to":"phr","confirmation":"n","ferry":"n","sort out":"phr",
 "biology":"n","gardening":"n","feel stuck":"phr","pricey":"a","water-resistant":"a",
 "checkup":"n","empty stomach":"phr","subscriber":"n","dormitory":"n","fire drill":"phr",
 "get through":"phr","recipe":"n","jaw":"n","gradually":"ad","chew":"v","heel":"n",
 "impact":"n","enroll":"v","enthusiasm":"n","assignment":"n","exclaim":"v",
 "abusive language":"phr","unaware":"a","uninformed":"a","unintentional":"a",
 "circularity":"n","continuum":"n","electromagnetic":"a","octave":"n",
 "correspond to":"phr","mutuality":"n","straightforward":"a",
 "social capital":"phr","job lead":"phr","a letter of recommendation":"phr",
 "stress":"v","assertion":"n","justification":"n","biographer":"n","commentary":"n",
 "validity":"n","height":"n","civil":"a","provision":"n","self-imposed":"a",
 "observance":"n","deliverance":"n","parallel":"a","electronics":"n",
 "by percentage":"phr","household appliance":"phr","biography":"n","master":"n",
 "rediscover":"v","accessible":"a","craft":"v","fill out":"phr","marine":"a",
 "additive":"n","preservative":"n","synthetic":"a","processor":"n","distributor":"n",
 "in stages":"phr","retailer":"n","uniform":"a","liken":"v","footpath":"n","trail":"n",
 "interventionist":"a","pave":"v","superhighway":"n","obstacle":"n",
 "bulldoze through":"phr","modesty":"n","variability":"n","insignificant":"a",
 "backwater":"n","wetland":"n","braid":"n","channel":"n","swamp":"n",
 "undesirable":"a","presume":"v","bower":"n","decorate":"v","chaotic":"a",
 "burnout":"n","exhausting":"a","insensitivity":"n","mentality":"n","prescription":"n",
 "public figure":"phr","meadow":"n","grassland":"n","drain":"v","be composed of":"phr",
 "anonymity":"n","neutrality":"n","impartiality":"n","deterministic":"a",
 "preference":"n","psychosocial":"a","interruption":"n","evaluation":"n","revision":"n",
 "colleague":"n","notation":"n","rest assured":"phr","mathematician":"n","canopy":"n",
 "initiate":"v","surgical":"a","precision":"n","snap":"v","architectural":"a",
 "multitude":"n","serialize":"v","ambiguous":"a","lean":"a","videoconferencing":"n",
 "replicate":"v","social presence":"phr","fireworks":"n","cheer for":"phr",
}

# 뜻이 뜻밖인 것 — 「다의어」로 표시한다. 뜻을 외우던 것과 다르게 쓰였다.
POLY = {
 "impact","stress","height","civil","master","craft","uniform","channel","trail",
 "lean","parallel","drain","snap","provision","modesty","liken","presume",
}

# 어려움 기준을 넘지만 넣은 것 — 왜 넣었는지 남긴다.
# 다의어(뜻이 뜻밖인 것): impact 충격 · stress 강조하다 · height 정점 · civil 세속의
#   · master 석사 · craft 짓다 · uniform 균일한 · channel 수로 · trail 길 · lean 빈약한
#   · parallel 나란한 · drain 배수하다 · snap 끊어지다 · provision 공급
# 덩어리 표현(낱말을 합쳐도 뜻이 안 나오는 것): head out to · heat up · sort out
#   · feel stuck · get through · fill out · in stages · by percentage · rest assured
#   · cheer for · be composed of · correspond to · bulldoze through
#   · social capital · social presence · public figure · job lead
#   · a letter of recommendation · empty stomach · nursing room · fire drill
# 합성어(시험에 통째로 나오는 것): protective film · star-patterned · heart-shaped
#   · water-resistant · self-imposed · household appliance · abusive language
