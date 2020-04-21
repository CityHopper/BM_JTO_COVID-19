from konlpy.tag import Hannanum
from konlpy.tag import Kkma
import re
kkma = Kkma()
hannanum = Hannanum()


news = '''(런던=연합뉴스) 박대한 특파원 = 신종 코로나바이러스 감염증(코로나19)으로 병원에서 집중 치료를 받던 보리스 존슨(55) 영국 총리가 상태가 호전돼 일반 병상으로 옮겼다.
9일(현지시간) BBC 방송에 따르면 영국 총리실 대변인은 "총리가 오늘 저녁 집중 치료 병상에서 일반 병상으로 옮겼다"면서 "그는 회복 초기단계에 긴밀한 관찰을 받을 것"이라고 말했다.
대변인은 "그는 매우 좋은 정신 상태에 있다"고 덧붙였다.
맷 행콕 보건장관은 "존슨 총리가 집중 치료에서 벗어나 회복의 길에 접어들었다는 것을 듣게 돼 매우 좋다"면서 "국민보건서비스(NHS)는 우리 모두를 위해 존재하며, 존슨 총리에게 세계 최고 수준의 치료를 해 줄 것을 알았다"고 칭찬했다.
니컬라 스터전 스코틀랜드 자치정부 수반은 트위터에 "좋은 소식"이라고 적었고, 리즈 트러스 국제통상부 장관은 "멋진 소식"이라고 반응했다.
제1야당인 노동당의 예비내각 법무부 장관인 데이비드 래미 의원은 "나라 전체가 존슨 총리가 가능한 한 빨리 완전히 회복하기를 바란다"고 밝혔다.
도널드 트럼프 미국 대통령은 이날 트위터에 올린 글에서 "아주 좋은 뉴스:보리스 존슨 총리가 방금 집중치료 병동으로부터 밖으로 옮겨졌다"며 "보리스, 쾌유를 빈다!!!"라고 적었다.
앞서 존슨 총리는 지난달 27일 코로나19 확진 사실을 알렸으며, 이후 자가 격리에 들어갔다.
존슨 총리는 열이 계속되면서 열흘가량 증상이 완화되지 않자 결국 지난 5일 저녁 런던 세인트 토머스 병원에 입원했다. 이후 다시 상태가 악화하자 6일 저녁 7시께 집중 치료 병상으로 옮겼다.
집중 치료 병상은 통상 중환자를 위한 곳이다.
코로나19 환자 중에서는 호흡 곤란 문제를 해결하기 위해 산소호흡기 등의 도움이 필요한 이들이 이곳으로 옮겨진다.
존슨 총리는 이곳에서 산소 치료 등을 받으면서 상태가 호전됐고, 결국 이날 일반 병상으로 옮겼다.'''

r = re.compile("(\w+)\((\w+)\)")
print(r.findall(news))
print(dict(r.findall(news)))
print(r.findall(news)[0][0])
print(r.findall(news)[0][1])

# news = kkma.sentences(news)
# for i in range(1, len(news)):
#     print(i, news[i])

# print('search', re.search(r'\((.*?)\)', news))
# print('findall', re.findall('\(([^)]+)', news))

def find_syn(text):
    brck = re.findall('\(([^)]+)', text)
    return brck
print('find_syn', find_syn(news))


# print('한나눔', hannanum.analyze(u'신종코로나바이러스감염증'))

# print('꼬꼬마', kkma.pos(u'')

# sent = kkma.sentences(u'')
# for s in sent:
#     if '코로나' in s:
#         print(s, '\n')

# f = open("./ScrapedData/‘코로나19’ 치료제 실험동물 개발 돌입_19.txt", 'r', encoding='UTF8')
# while True:
#     line = f.readline()
#     if not line: break
#     print(line)
# f.close()
#
# print(type(line))


import nltk
from nltk.corpus import wordnet as wn

# tab = "    "
# for synset in wn.synsets('kindle'):
#     print("{}:".format(synset.name()))
#     print(tab+"definition: {}".format(synset.definition()))
#     print(tab+"pos: {}".format(synset.pos()))
#     for e in synset.examples():
#         print("    "+"example: {}".format(e))
#     print()
#
# for synset in wn.synsets('car'):
#     print("{}: {}".format(synset.name(), synset.definition()))
#     synonyms = ", ".join([lem.name() for lem in synset.lemmas()])
#     print(tab + "synonyms: {}".format(synonyms))
#
#     hypernyms = ", ".join([hypernym.name() for hypernym in synset.hypernyms()])
#     print(tab + "hypernyms: {}".format(hypernyms))
#     print()