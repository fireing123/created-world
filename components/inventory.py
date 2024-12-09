"""아이템, 레시피, 도구 특성같은 정보를 저장함"""
class ItemIndex:
    BOW = 0 # CREATED
    SWORD = 1 # CREATED
    PICKAXE = 2#CREATED
    AXE = 3 #CREATED
    ARROW = 4 # CREATED
    IRON_ORE = 5
    IRON_INGOT = 6#COOKED
    TREE_BRANCH = 7
    FEATHER = 8
    TENDON = 9
    LEATHER = 10
    COAL = 11
    BEEF = 12
    COOKED_BEEF = 13#COOKED
    CHICKEN = 14
    COOKED_CHICKEN = 15#COOKED
    SUPER_ORE = 16
    SUPER_JEWEL = 17#COOKED
    WING = 18# CREATED
    FEATHER_BUNDLE = 19 # CREATED
    STONE = 20
    IRON_PICKAXE = 21 #CREATED
    BOOTS = 22# CREATED
    BREASTPLATE = 23# CREATED
    ZOMBIE_BEEF = 24 # YOU CAN EAT! LOL
    SLIME_OIL = 25 # FIRE!!!
    BONE_TANK = 26 # OIL TANK
    GOD_CALLOR = 27 # LIE
    WORLD_GETTER = 28 # REAL
# 내구도
is_tools = {
    ItemIndex.BOW:100,
    ItemIndex.SWORD:100,
    ItemIndex.PICKAXE:100,
    ItemIndex.IRON_PICKAXE:100,
    ItemIndex.AXE:100,
    ItemIndex.BOOTS:None,
    ItemIndex.BREASTPLATE:None,
    ItemIndex.WING:None,
    ItemIndex.GOD_CALLOR:None,
    ItemIndex.WORLD_GETTER:None
}

is_foods = {
    ItemIndex.COOKED_BEEF:20,
    ItemIndex.COOKED_CHICKEN:15,
    ItemIndex.BEEF:5,
    ItemIndex.CHICKEN:5
}

is_fuel = {
    ItemIndex.COAL:100,
    ItemIndex.TREE_BRANCH:20
}

craft_recipe = {
    (ItemIndex.BOW, 1): list(reversed([
        [[None, 0],                     [ItemIndex.TREE_BRANCH,     1], [ItemIndex.TENDON,        1]],
        [[ItemIndex.TREE_BRANCH,    1], [None, 0],                      [ItemIndex.TENDON,        1]],
        [[None, 0],                     [ItemIndex.TREE_BRANCH,     1], [ItemIndex.TENDON,        1]]
    ])),
    (ItemIndex.SWORD, 1): list(reversed([
        [[None, 0],                     [None, 0],                      [ItemIndex.IRON_INGOT,    1]],
        [[None, 0],                     [ItemIndex.IRON_INGOT,      1], [None, 0]                   ],
        [[ItemIndex.TREE_BRANCH,    1], [None, 0],                      [None, 0]                   ]
    ])),
    (ItemIndex.ARROW, 16): list(reversed([
        [[None, 0],                     [None, 0],                      [ItemIndex.IRON_INGOT,    1]],
        [[None, 0],                     [ItemIndex.TREE_BRANCH,    16], [None, 0],                  ],
        [[ItemIndex.FEATHER,        8], [None, 0],                      [None, 0],                  ]
    ])),
    (ItemIndex.AXE, 1): list(reversed([
        [[ItemIndex.STONE,          1], [ItemIndex.TREE_BRANCH,     1], [ItemIndex.STONE,         1]],
        [[ItemIndex.STONE,          1], [ItemIndex.TREE_BRANCH,     1], [None, 0]                   ],
        [[None, 0],                     [ItemIndex.TREE_BRANCH,     1], [None, 0]                   ]
    ])),
    (ItemIndex.PICKAXE, 1): list(reversed([
        [[ItemIndex.STONE,          1], [ItemIndex.STONE,          1], [ItemIndex.TREE_BRANCH,    1]],
        [[None, 0],                     [ItemIndex.TREE_BRANCH,    1], [ItemIndex.STONE,          1]],
        [[ItemIndex.TREE_BRANCH,    1], [None, 0],                     [ItemIndex.STONE,          1]]
    ])),
    (ItemIndex.IRON_PICKAXE, 1): list(reversed([
        [[ItemIndex.IRON_INGOT,     1], [ItemIndex.IRON_INGOT ,    1], [ItemIndex.TREE_BRANCH,    1]],
        [[None, 0],                     [ItemIndex.TREE_BRANCH,    1], [ItemIndex.IRON_INGOT,     1]],
        [[ItemIndex.TREE_BRANCH,    1], [None, 0],                     [ItemIndex.IRON_INGOT,     1]]
    ])),
    (ItemIndex.FEATHER_BUNDLE, 1): list(reversed([
        [[None, 0],                     [ItemIndex.TENDON,         1], [None, 0]                    ],
        [[ItemIndex.FEATHER,        1], [ItemIndex.FEATHER,        1], [ItemIndex.FEATHER,        1]],
        [[ItemIndex.FEATHER,        1], [None, 0],                     [ItemIndex.FEATHER,        1]]
    ])),
    (ItemIndex.WING, 1): list(reversed([
        [[None, 0],                     [ItemIndex.IRON_INGOT,     1], [None, 0],                   ],
        [[ItemIndex.FEATHER_BUNDLE, 1], [ItemIndex.LEATHER,        1], [ItemIndex.FEATHER_BUNDLE, 1]],
        [[ItemIndex.FEATHER_BUNDLE, 1], [ItemIndex.SUPER_JEWEL,    1], [ItemIndex.FEATHER_BUNDLE, 1]]
    ])),
    (ItemIndex.BREASTPLATE, 1): list(reversed([
        [[ItemIndex.LEATHER,        1], [ItemIndex.TENDON,         1], [ItemIndex.LEATHER,        1]],
        [[ItemIndex.LEATHER,        1], [ItemIndex.LEATHER,        1], [ItemIndex.LEATHER,        1]],
        [[ItemIndex.IRON_INGOT,     1], [ItemIndex.IRON_INGOT,     1], [ItemIndex.IRON_INGOT,     1]]
    ])),
    (ItemIndex.BOOTS, 1): list(reversed([
        [[ItemIndex.FEATHER,        1], [None , 0],                    [ItemIndex.FEATHER,        1]],
        [[ItemIndex.TENDON,         1], [ItemIndex.IRON_INGOT, 1],     [ItemIndex.TENDON,         1]],
        [[ItemIndex.LEATHER,        1], [None, 0],                     [ItemIndex.LEATHER,        1]]
    ])),
    (ItemIndex.GOD_CALLOR, 1): list(reversed([
        [[None, 0],                     [ItemIndex.SUPER_JEWEL,    1], [None, 0]                    ],
        [[None, 0],                     [ItemIndex.IRON_INGOT,     1], [None, 0]                    ],
        [[None, 0],                     [None, 0],                     [None, 0]                    ]
    ])),
    (ItemIndex.WORLD_GETTER, 1): list(reversed([
        [[None, 0],                     [ItemIndex.GOD_CALLOR,     1], [None, 0]                    ],
        [[ItemIndex.BONE_TANK,      1], [ItemIndex.SUPER_JEWEL,    1], [ItemIndex.ZOMBIE_BEEF,    1]],
        [[ItemIndex.SLIME_OIL,      1], [None, 0],                     [None, 0]                    ]
    ]))
}

furnace_recipe = {
    ItemIndex.IRON_ORE: [ItemIndex.IRON_INGOT, 50],
    ItemIndex.SUPER_ORE: [ItemIndex.SUPER_JEWEL, 50],
    ItemIndex.BEEF: [ItemIndex.COOKED_BEEF, 25],
    ItemIndex.CHICKEN: [ItemIndex.COOKED_CHICKEN, 25]
}

itemDescriptions = {
    ItemIndex.BOW: [
        "목궁",
        "목궁(木弓)은 보통 호궁(弧弓)이라고도\n하는데, 활고자(활 양쪽 끝의 꺾인 부분)는 \n뽕나무로, 활채는 광대싸리로 만든 이 \n호궁이 가장 많이 쓰였기 때문이다. \n제작법이 단순하고 제조비용이 싸기는 \n하지만 각궁에 비해 성능이 떨어져 \n일반 병사용 또는 보조 활로 사용되었다."
    ],
    ItemIndex.SWORD: [
        "롱소드",
        "IDC 70년산 최고급 관상용 전시상품으로\n등록된 레시피로 제작됬다."
    ],
    ItemIndex.PICKAXE: [
        "곡괭이",
        "내구성을 포기하는데신,\n강력한 힘을 부여한다는 속박을 걸었다."
    ],
    ItemIndex.AXE: [
        "도끼",
        "Here is Johnny!"
    ],
    ItemIndex.ARROW: [
        "화살",
        "화살은 활로 쏘는 뾰족한 비행 구조체이다. \n화살은 오랜 옛날의 유물과 기록을 보면 \n다양한 문화에 걸쳐 발견되는데 지금도 \n활과 함께 스포츠나 사냥에 사용되고 있다. \n줄여서 살이나 시(矢)라고도 한다."
    ],
    ItemIndex.IRON_ORE: [
        "철 원석",
        "산화철(II)(FeO)는 검은색, \n산화철(III)(Fe2O3)은 붉은색을 띤다. \n자연 상태에서는 철광석의 \n형태로 존재하며, \n모래 형태로 된 사철도 있다."
    ],
    ItemIndex.IRON_INGOT: [
        "철 주괴",
        "4주기 8족에 위치하는 금속 원소. \n융점(녹는점)은 상압에서 1538℃, \n결정구조는 체심입방결정이며 \n공간군은 Im3m 산화수는 \n2+, 3+로 알려져 있는데, \n각각 판이한 특성을 지닌다."
    ],
    ItemIndex.TREE_BRANCH: [
        "나뭇가지",
        "짱돌과 더불어 인류가 최초로 사용한 무기. \n원시인 시절에는 전쟁이 났다 하면 \n서로에게 돌을 던지며 나뭇가지를 \n들고 휘둘렀을 것이다."
    ],
    ItemIndex.FEATHER: [
        "깃털",
        "표피가 변형되어 생긴 것으로, \n중심의 깃줄기에서 많은 깃가지가 \n나온 것이 특징이다. \n포유류의 털, 파충류의 비늘과 \n그 기원을 같이 하나, \n훨씬 복잡한 구조를 갖고 있다."
    ],
    ItemIndex.TENDON: [
        "소 힘줄",
        "아마 줄이니 활시위로 만들수 있을거같다.?"
    ],
    ItemIndex.LEATHER: [
        "가죽",
        "벗겨낸 동물의 피부를 일컫는 말로, \n'가죽'은 한자어 같지만 순우리말이다. \n한자어는 피혁(皮革)이다. \n사람한테는 잘 쓰이지 않으며, \n사람한테 쓰이는 경우 살 또는 피부를 \n낮잡아 이르는 말이기도 하다."
    ],
    ItemIndex.COAL: [
        "석탄",
        "석탄(石炭, coal)은 셀룰로스와 리그닌을 \n주성분으로 한 수목이 두껍게 쌓여서 \n만들어진 층이 그 위의 압력으로 탄화되어 \n생성된 퇴적암이다."
    ],
    ItemIndex.BEEF: [
        "소고기",
        "돼지고기, 닭고기와 더불어 대표적인 고기 \n중 하나로, 보통 이 중에선 가장 비싸고 \n고급스럽다는 인식이 강하다. 오죽했으면 \n쇠고기를 正肉[3]이라 불렀겠는가? 돼지나 \n닭과는달리 농사나 건축의 동력원으로도 사\n용되는 가축이었기 때문에, 과거 소고기를 \n먹는다는 것은 사치스러운 일로 통했고,대\n중화된 지금도 비싼 고기로 통한다.이는 \n소의 사육 비용이 돼지나 닭보다 많이들기\n 때문이다. 닭은 아예 비교하기도 어렵고\n돼지랑비교해도 단백질 전환율이 상당히 \n나쁜 편이다. 즉, 효율이 낮다."
    ],
    ItemIndex.COOKED_BEEF: [
        "익힌 소고기",
        "최적의 온도로 구워진 소고기!"
    ],
    ItemIndex.CHICKEN: [
        "닭고기",
        "닭을 도축하여 얻는 고기로, 계육(鷄肉)이\n라고도 한다. 전세계적으로 많이 애용되는 \n고기 중 하나이며 마리로 따졌을 때 가장 \n많이 도축되는 고기이다. 백색육(white\n meat)의 대명사이기도 하다.[1] 단\n, 과거 세계에서 가장 많이 소비되는 육류\n는 아니었었는데, 소비량(무게)으로 따졌을\n때 1위인 돼지고기와 체급에서 상대가 안 \n되었었기 때문. 다만 2020년대 들어서는\n닭고기가 소비 총량으로도 1위로 올라섰다.\n[2] 또한 새는 수각류 공룡의 한 종류이\n기에 닭고기는 가장 흔하게 구할 수 있는 \n공룡 고기이기도 하다. 다만 현생 조류 중\n에서 중생대의 비조류 공룡들과 가까운 새는\n타조 등의 고악류이다. 하지만 닭도 오리나\n기러기와 함께 고악류 바로 다음으로 분화된\n원시적인 분류군에 속하기 때문에 비조류 공\n룡들과 멀리 떨어진 정도는 아니다.[3]"
    ],
    ItemIndex.COOKED_CHICKEN: [
        "익힌 닭고기",
        "삼계탕보다 맛있다."
    ],
    ItemIndex.SUPER_ORE: [
        "마법 광석",
        "자연상태로는 주변물질을 \n점정 불안정하게 만든다"
    ],
    ItemIndex.SUPER_JEWEL: [
        "마법 주괴",
        "오랫동안 방치하면 주변에있는 물질과 \n동화된다."
    ],
    ItemIndex.WING: [
        "날개",
        "\"2단점프!\n특가 할인 단돈 199,999OBS!\"\n라는 광고를 저번주에 봤었다...\n공중에서 한번더 점프할수있다."
    ],
    ItemIndex.FEATHER_BUNDLE: [
        "깃털뭉치",
        "힘줄을 묶은줄알겠지만,\n사실 소 힘줄을 아교로 만들어 칠한거다."
    ],
    ItemIndex.STONE: [
        "돌",
        "강가에있는 돌처럼 둥글둥글하다."
    ],
    ItemIndex.IRON_PICKAXE: [
        "철 곡괭이",
        "굳었거나 단단한 땅을 파는 데 쓰이는 \n농기구로, 괭이의 변형. 농사 \n외 토목 등에도 쓰인다. \n드릴 같은 동력공구가 \n없던 과거엔 바위를 제거할 \n유일한 수단이었기에 \n광부의 상징이기도 하다. 원래 괭이라는 \n농기구는 주로 밭농사의 골을 파기 \n위해 쓰는 기구이다. 이 지면을 \n수평으로 파는 괭이를 지면에 수직으로 파기 \n좋게 뾰족한 형태로 바꾼 기구가 곡괭이."
    ],
    ItemIndex.BOOTS: [
        "가죽 부츠",
        "이제 뛰어도 발이 안아플것같다.\n왼쪽 shift키로 달릴수있다."
    ],
    ItemIndex.BREASTPLATE: [
        "갑옷",
        "갑옷(甲-)은 무기에 의한 공격을 피하거나 \n흡수하기 위해 설계된 보호의를 일컫는다. \n기능, 문화, 지역에 따라 공격을 막기위해 \n역사적으로 다양하게 발전되어 왔다. \n보호의 측면 이외에도 그 쓰임과 \n역사에 따라 많은 형태로 연구될 \n가치가 있어 사료의 측면에서도 \n중요성을 가진다."
    ],
    ItemIndex.ZOMBIE_BEEF: [
        "좀비 정수",
        "이것의 동력원이자 상위 세계를 창조한 힘"
    ],
    ItemIndex.SLIME_OIL: [
        "슬라임",
        "발화점 380-425oC 인 인화성 물질입니다."
    ],
    ItemIndex.BONE_TANK: [
        "뼈",
        "팔 부분이다. #$#@!적으로 그릇에 해당된다."
    ],
    ItemIndex.GOD_CALLOR: [
        "시련",
        "맞이하라"
    ],
    ItemIndex.WORLD_GETTER: [
        "실현",
        "상위세계 마법 핸들러 주소"
    ]
}