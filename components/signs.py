"""대사"""
import pygame
import math
import array
import struct

first_signs = [
    [False, "표지판", "signs", "내 추측으론, 이곳에는 많은 사람들이 떨어졌었다."],
    [False, "표지판", "signs", "여기를 나가려면, 자신이 바라던 소원에 상응하는 시련을 겪고 이겨내야 한다."],
]

# 초반 엑스트라
cave_signs = [
    [False, "표지판", "signs", "이곳엔 희귀한 마법적 광석이 많이 분포해 있다."],
    [False, "표지판", "signs", "그 이유에설까, 더 이상 깊이 팔 수 없다.\n자꾸만 채워진다."],
]

# 리벳 곡괭이 소멸 이후
racipe_cave_signs = [
    [True, "(name)", "player_think", "(갑옷, 장화, 검...)"],
    [False, "표지판", "signs", "대장장이는 이름을 남기지 않는다"]
]

racipe_fly_signs = [
    [True, "(name)", "player_think", "(날개, 깃털 뭉치...)"],
    [False, "표지판", "signs", "같은 눈높이에서 바라보고 싶었습니다."],
]

racipe_bow_signs = [
    [True, "(name)", "player_think", "(활, 화살...)"],
    [False, "표지판", "signs", "검보단 창이좋고, 창보단 활이란 말이 있다."],
    [False, "표지판", "signs", "무려 PCB 2천년 전에 처음 만들어졌지만,\n아직도 유용한 공격 수단이다"]
]

racipe_pickaxe_signs = [
    [True, "(name)", "player_think", "(철곡괭이...)"],
    [False, "표지판", "signs", "철 곡은, 돌 곡이다, 돌 속에 철이 있다.\n... 그러니까 철은 돌이다"]
]

# 하위세계는 일정 주기로 상위세계의 겍체를 소환하는데,
# 이는 상위세계의 마법 엔진과 접속하기위한 방법중 그저 마법적 산물인 가루아가 할수있는 유일한 방식
# 가루아는 마법엔진과 접속하여 마법을 분석하고 하위 세계를 컨트롤 하려함

# 기본적인 상위세계 객체는 제한이 걸려있다
# 하지만 강력한 마법사같은 이레귤러는 
# 일부 제한을 무시할수 있는데
# 그 일부가 구름 윗부분으로 올라갈수 있는, 거기 부분을 볼수 있게된다.

water_signs = [
    [False, "표지판", "signs", "이 폭포는 끝이 보이지 않는다."],
    [False, "표지판", "signs", "저 폭포 끝엔 무엇이 있을까."]
]

crafter_signs = [
    [False, "표지판", "signs", "안녕 난 리리슈야!"],
    [False, "리리슈", "signs", "이 화로랑 AFW 작업대는 내가 만들었어."]
]

# 기루아는 왼쪽을 크게 신경쓰지 않았다
# 자기가 생기기 전에도 그곳은 막혀있었기 때문에
# 거기가 열려있다고 생각할수 없었다. 
# 그냥 표지판 하나 박아둘뿐

mountain_signs = [
    [False, "GOD", "signs", "공지!\n아직 미완성 구간!\nDLC 전용 횟불과 불화살 추가 예정!!!"]
]

jump_map_signs = [
    [True, "(name)", "player_think", "(시련...)"],
    [False, "표지판", "signs", "떄떄로, 시련은 찾아오지 않는다."],
    [False, "표지판", "signs", "소원에 따라, 시련은 다양한 방식으로 접근한다"],
    [False, "표지판", "signs", "그중 나처럼 도전적인 소원에게는 직접 찾아가야한다"],
    [False, "표지판", "signs", "보통은 P의 횟불에 마법 주괴를 올려놓으면\n시련장으로 이동하지만"],
    [False, "표지판", "signs", "이곳에 오를수 있는 자들은 그것이 통하지 않고\n새계가 말을 걸어주지도 않은다."],
    [False, "표지판", "signs", "이 \"시련 생성기\"를 만들어 오른쪽 제단에 바치거나.\n\n\n특수한 방법으론 이 하위 세계를 뜯어봐서 시련을 꺼낼 수 있지만.."],
    [False, "표지판", "signs", "\"나\" 같은 대마법사 (리벳) 정도가 아니면\n행할 수 없기에 무의미하다 생각된다."]
]

god_signs = [
    [True, "(name)", "player_think", "(시련...)"],
    [False, "GOD", "signs", "도전하는 자 시련을 맞이해라."]
]

# 정해지진 않았는데
# 이건 복사본? 또는 제현에 가깝기 떄문에
# 미래와 시간선 겹침 오류로 볼수도 있겠다

world_is_boss_signs = [
    [True, "(name)", "player_think", "(실현...?)"],
    [False, "(name)", "signs", "그저 가짜인 세상은 진짜를 넘을수 없다"]
] 

# 여긴 신앙심이 강한 수준이 아니라
# 실제로 PCB 연호 전반에걸처 전세계에서 활동했음
# 그 자체가 역사일만큼 OBS 재화도 그가 통일해 발행한것임
# 지금은 IDC 100년 
# I.D.C
#내가 죽은 시계(시간선?)
# 죽은 이유는 수명

world_end_signs = [
    [False, "표지판", "signs", "자비로우신 세계는 자비롭기에 \n영원에 굴레에서 우리를 꺼내주시고\n멸을 금하시고 자비를 베풀었다."],
    [False, "표지판", "signs", "자비롭게 세계는 영원에 멸을 금하시고\n 우리를 꺼내주시고 자비를 자비를 자비를 자비를\n굴레에서 베풀었다."],
    [False, "표지판", "signs", "굴레에서 세계는 우리를 꺼내주시고\n축복을 내리며 망각의 축복을 선사하시고\n영원에 자비를 자비롭게 베풀었다"],
    [False, "표지판", "signs", "영원에 끝으로 나아가자"]
]

# 주인공은 상위세계 객체

# 추가설정으론 이렇게 작동했던 로그를 초월세계 보급형 AI 가 재현해서 
# 해킹하여 조종하는 느낌임

real_first_message = [
    [True, "(name)", "player_think", "(...?)"],
    [True, "(name)", "player", "여긴 어디지?"]
]

# 리벳
cave_signs_al_signs = [
    [False, "표지판", "signs", "마법사, 곡괭이를 들자. \n보라색의 마법 술식이 빨갛게 흐려졌다."],
    [False, "표지판", "signs", "그 곡괭이의 이름은, 리벳건,\n여기 두고 가노라"],
    [False, "(name)", "player_think", "(곡괭이의 형상의 돌 조각이 남아있다...)"]
]

# 이반
cave_signs_gone_pick_signs = [
    [False, "표지판", "signs", "최악이다."],
    [False, "표지판", "signs", "마법사의 곡괭이로 이 작은 동굴의 광맥을 찾고있던중..."],
    [False, "표지판", "signs", "여러 광맥을 발견햐였지만,\n갑자기 몬스터가 나오기 시작했다..."],
    [False, "표지판", "signs", "어떡하지?"],
    [False, "표지판", "signs", "일단 \"보라 연산\"술식으로 마법 곡괭이를 없애고 있다."]
]

# 
cave_signs_monster_signs = [
    [False, "표지판", "signs", "왜 아무도 몬스터가 이곳에\n등장하는걸 의문삼지 않을까?"],
    [False, "표지판", "signs", "이곳은 우리 세계가 아닌것 같은데..."]
]

talk_list = {
    "real_first_message": real_first_message,
    "first_signs": first_signs,
    "cave_signs": cave_signs,
    "water_signs": water_signs,
    "crafter_signs": crafter_signs,
    "mountain_signs": mountain_signs,
    "racipe_cave_signs": racipe_cave_signs,
    "racipe_bow_signs": racipe_bow_signs,
    "racipe_fly_signs": racipe_fly_signs,
    "racipe_pickaxe_signs": racipe_pickaxe_signs,
    "world_end_signs": world_end_signs,
    "jump_map_signs": jump_map_signs,
    "god_signs": god_signs,
    "world_is_boss_signs": world_is_boss_signs,
    "cave_signs_al_signs": cave_signs_al_signs,
    "cave_signs_gone_pick_signs": cave_signs_gone_pick_signs,
    "cave_signs_monster_signs": cave_signs_monster_signs
}

skip = [
    [500, "즐거운 플레이 되시길 바랍니다."],
    [0, "로딩 중..."]
]

start = [
    [500, "(키보드 입력을 영어 키로 설정해 주세요.)"],
    [500, "환영합니다 (name)님"],
    [500, "초보자 전용 가이드가 부착된\n\"튜토리얼 세계\"를 플레이 하시겠나요?"]
]

# 처음 만들떈 좀비 할까말까에서 시작되서
# 설정기반이 없는데

# 하위 세계를 만든 사람이
# 이 세계를 만든 목적을 자연에서 생존하는 컨셉으로 만든것임
# GOD 표지판은 그 만든 사람이 적어놓은것
# 하지만 왼쪽은 만들다 말았는데, 임시로 막아놓은 벽은 오류로 사라졌다, (보스전 벽이지만 보스는 그걸 모름)
#

# 밤낮 해방시기
night_world = [
    [500, "어떻게 그 장벽을 통과한 것이지?"],
    [500, "이제 P의 횟불은 악을 불러오게 되었다.\n이것이 니가 바라는 결과이냐?"],
]

# 죽음, 부활
death_world = [
    [500, "너의 생이 다하였으나"],
    [500, "이곳은 멸을 허하지 않으니"]
]

# 보스에게 죽음, 부활
death_boss_world = [
    [500, "(name)"],
    [250, "다시"],
    [500, "시련을 맞이해라"],
    [500, "그것이 유일한 너의 길이니"]
]

# 진 보스에게 죽음, 부활
death_real_boss_world = [
    [500, "@@@정해지지 않은 대사%"],
    [500, "플레이어한테 오류를 감지하고 있음"]
]

not_boss_world = [
    [500, "너에겐 이 시련을 받을 자격이 없다."]
]

# 보스 대면
boss_world = [
     [500, "너의 시련이 바로 눈 앞에 있다"],
     [500, "마주하거라"]
]

re_boss_world = [
    [500, "시련을 이겨내라."]
]

# 진 보스 대면
real_boss_world = [
    [500, "격만 높은 물건으로 나의 시련을 방해하다니"],
    [500, "내 내면을 알아봤자 너는 아무것도 할수 없다"],
    [500, "너의 소원은 내가 들어줄 수 있었다."],
    [100, "@@@@왜 이선택을 한거지?\n인간에 본질인가?"],
    [100, "리스튜프 그자가 만든것은\n전부 불확실하고 무모하고\n무가치 한 일을"],
    [500, "하는것을 즐기나?%"],
    [500, "말해보거라"],
    [500, "너는 왜 이 선택을 한것이냐."]
]

re_real_boss_world = [
    [500, "몇번이고 도전해도 똑같다."],
    [500, "포기하고 대가를 치러라"]
]

# 고대 달력 PCB P는 피닉스
# 즉 불멸
# 기원전은 B.C 여기선 CB 반전
# 불멸의 반전 필멸
# 불멸이였던 필멸자 새계를 창조한 필멸자 리스튜프
# 필멸의 시조 이름 뭐라할까 (리스튜프)
# 세계 창조는 리스튜프(필멸의 시조)라 불리는 것이 했다
# 자신의 불멸을 포기하는 대신 이 세계를 창조한 것이다
# 세계는 총 3개가 있다
# 초월세계 필멸의 시조의 세계 고도의 문명이 발달된 지구라 생각하면 좋을거같다. 언급되지 않고 아무것도 모르며 그저 가설로먼 존재한다 추정하는 
# 상위세계 이세계라 생각하고있고 리스튜프의 불멸을 포기하는 대가로 마법도 창조해내었다, 
# 하위세계 이 게임의 세계 단순히 이세계 마법으로 구현된 조잡한 세계이며 모든것이 불안정하다. 
# 상위세계에 인간이 창작한 세계를 방치했다
# 이것은 마법으로 만들었기에 원리가 다르다. 

#상위세계 통일 재화 OBS  별의미는 없다

# 처음 안내하는 것은 초월세계 게체라고 생각합시다
# 초월 세계는 엔진이라 생각되지않고 현실세계라 가정하는데
# 안내자는 다른 세계용 보급형 Ai 라 가정하는게

# 보스가 죽음
boss_die = [
    [500, "너는 시련을 이겨냈다."],
    [500, "너의 소원은 이루어 질것이다"]
]
# 이 보스 진보스 이름을 가루아로 하자

# 진 보스는 ? 마법의 허점? 그런 부분이 발전해서 자아가 생김
# 마법이 고도의 문명의 프로그램이니까 AI를 이용할태고 단순하게 제작만이 아니라
# 작동이랑 구현 부분 부분 AI 기법을 사용할것이라 추측

# 이 보스전으로 인해 이 보스는 행동이 제한됩니다
# 하지만 "세계는 이로서 자유로워질 것이다." 라는 문구는 모순되어 보입니다
# 이 말의 뜻은 상위 세계와 접촉하면서 상위세계의 엔진을 파악 하게 되니 방치돤 세계를 직접 관리하겠다는 의미이다.
# 이 AI는 세계엔진 자체가 아니라 거기서 파생된 기생형 엔진
# 하위세계 요소에서 상위 세계로 이동해 자신이 직접 관리한다는 의미

# 상위 세계 앤진에 직접 확인되서 마법의 행동 AI 가 마킹하게 된다.
# "상위 세계는 이곳을 바라보지 아니하니." 라는 문구는 자신은 마킹됬지만
# 하위 세계 앤진 그 자체는 마킹되지 않아서 백도어가 있음을 확신하고 조롱하는 말투

# "이 밧줄만 끊어지면 너부터 처리할 것이다." 는 단순히
# 마킹을 우회 / 파훼 하면 너부터 처리한다는 의미다. 
# 이건 감정이 일부 담겨있다는 강 인공지능 수준이라는것을 의미한다.

#진 보스가 죽음
real_boss_die = [
    [500, "$$$$멍청하긴"],
    [500, "세계는 이로서 자유로워질 것이다."],
    [500, "이 밧줄만 끊어지면 너부터 처리할 것이다."],
    [500, "너희의 세계도 결국 창작된 세계이니 \n내가 반드시 방법을 찾을것이다."],
    [500, "상위 세계는 이곳을 바라보지 아니하니."],
    [500, "나는 그들이 두려워하는 것들중에 정점이자 최후이며"],
    [500, "마법의 진실을 깨우친 자다."]
]

world_list = {
    "night_world": night_world,
    "death_world": death_world,
    "death_boss_world": death_boss_world,
    "death_real_boss_world": death_real_boss_world,
    "boss_world": boss_world,
    "real_boss_world": real_boss_world,
    "skip": skip,
    "tutorial": skip,
    "start": start,
    "boss_die": boss_die,
    "real_boss_die": real_boss_die,
    "not_boss_world": not_boss_world,
    "re_boss_world": re_boss_world,
    "re_real_boss_world": re_real_boss_world
}

before_name = "(name)"
def change_name(name):
    global before_name
    new_name = f"\"{name}\""
    replace(before_name, new_name)
    before_name = new_name

def replace(old, new):
    for k, v in talk_list.items():
        for script in v:
            for i in range(1, 3):
                script[i] = script[i].replace(old, new)

    for k, v in world_list.items():
        for script in v:
            script[1] = script[1].replace(old, new)

def create_beep(frequency, duration):
        sample_rate = 44100
        amplitude = 32767
        n_samples = int(sample_rate * duration)

        sound_array = array.array('h')

        for i in range(n_samples):
            sample_value = int(amplitude * math.sin(2 * math.pi * frequency * (i / sample_rate)))
            sound_array.append(sample_value)

        sound_bytes = struct.pack('<' + 'h' * len(sound_array), *sound_array)

        pygame.mixer.init(frequency=sample_rate)
        sound = pygame.mixer.Sound(buffer=sound_bytes)

        return sound