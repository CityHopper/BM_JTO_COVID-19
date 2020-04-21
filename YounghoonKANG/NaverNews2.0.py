from bs4 import BeautifulSoup
import requests
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from konlpy.tag import Kkma
kkma = Kkma()
okt = Okt()

def get_news(n_url): # HTML parser로 타이틀, 날짜, 내용 저장
    news_detail = []

    breq = requests.get(n_url)
    bsoup = BeautifulSoup(breq.content, 'html.parser')

    title = bsoup.select('h3#articleTitle')[0].text  # 대괄호는  h3#articleTitle 인 것중 첫번째 그룹만 가져옴
    news_detail.append(title)

    pdate = bsoup.select('.t11')[0].get_text()[:11]
    news_detail.append(pdate)

    _text = bsoup.select('#articleBodyContents')[0].get_text().replace('\n', " ")
    btext = _text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")
    btext = re.sub('[▶]', '', btext) # 기사 내용에서 특수문자 제거
    news_detail.append(btext.strip())

    news_detail.append(n_url)

    pcompany = bsoup.select('#footer address')[0].a.get_text()
    news_detail.append(pcompany)

    return news_detail

news_content = [] # 동의어 추출을 위한 리스트
news_result = [] # 워드클라우드 위한 리스트
def scraper(maxpage, query, s_date, e_date): # 뉴스의 보도날짜, 헤드라인, 내용 등을 뽑고 메모장에 저장
    s_from = s_date.replace(".", "")
    e_to = e_date.replace(".", "")
    page = 1
    maxpage_t = (int(maxpage) - 1) * 10 + 1  # 11= 2페이지 21=3페이지 31=4페이지  ...81=9페이지 , 91=10페이지, 101=11페이지
    count = 0
    while page < maxpage_t:
        print(page)
        url = "https://search.naver.com/search.naver?where=news&query=" + query + "&sort=0&ds=" + s_date + "&de=" + e_date + "&nso=so%3Ar%2Cp%3Afrom" + s_from + "to" + e_to + "%2Ca%3A&start=" + str(
            page)

        req = requests.get(url)
        print(url)
        cont = req.content
        soup = BeautifulSoup(cont, 'html.parser')
        # print(soup)

        for urls in soup.select("._sp_each_url"):
            try:
                # print(urls["href"])
                if urls["href"].startswith("https://news.naver.com"):
                    news_detail = get_news(urls["href"])
                    print(news_detail[0], urls["href"])
                    news_result.append(news_detail[0]) # 기사 제목
                    news_result.append(news_detail[2]) # 기사 내용
                    news_content.append(news_detail[2])

                    count += 1
                    f = open("./ScrapedData/{}_{}.txt".format(re.sub('[?"]', '', str(news_detail[0])), count), 'w', encoding='utf-8')  # 기사당 1파일,  특수문자 없앤 기사 제목으로 파일로 저장
                    for sentence in kkma.sentences(news_detail[2]):
                        if '코로나' in sentence:
                            for word in kkma.nouns(sentence):
                                f.write("{}\n".format(word))
                            # f.write("{}\n".format(kkma.nouns(sentence)))  # headline, content

            except Exception as e:
                print(e)
                continue
            finally:
                f.close()
        page += 10


def find_syn():
    r = re.compile("(\w+)\((\w+)\)")
    syns_dict = {}
    syns_list = []
    for news in news_content:
        syns_list.append(r.findall(news))
    for syn in syns_list:
        for s in syn:
            syns_dict[s[0]] = s[1]
    with open('./ScrapedData/test.txt', 'w') as s:
        s.write("{0}\n".format(syns_dict))

def make_wordcloud(word_count): # 뉴스 타이틀과 내용만 워드클라우딩
    twitter = Okt()
    sentences_tag = []
    # 형태소 분석하여 리스트에 넣기
    for sentence in news_result:
        morph = twitter.pos(sentence)
        sentences_tag.append(morph)
        print(morph)
        print('-' * 30)

    print(sentences_tag)
    print('\n' * 3)

    noun_adj_list = []

    # 메모장에 형태소가 분석된 모든 단어들을 저장
    f = open("./news_words.txt", 'w', encoding='utf-8')
    f.write(
        "{}\t".format(sentences_tag))  # new style
    f.close()

    # 명사와 형용사만 구분하여 리스트에 넣기
    for sentence1 in sentences_tag:
        for word, tag in sentence1:
            if tag in ['Noun', 'Adjective']:
                if len(str(word)) >= 2: # 2음절 이상만 포함
                    noun_adj_list.append(word)

    # 형태소별 count
    counts = Counter(noun_adj_list)
    tags = counts.most_common(word_count)
    # print(tags)

    # wordCloud생성, 한글 깨지는 문제 해결하기위해 font_path 지정
    wc = WordCloud(font_path='C:/Windows/Fonts/Fonts/batang.ttc',
                   background_color='white', width=800, height=600)
    print(dict(tags))
    cloud = wc.generate_from_frequencies(dict(tags))
    plt.figure(figsize=(32, 18))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()

def main():
    maxpage = 2
    query = '코로나'
    s_date = '2020.04.06'
    e_date = '2020.04.06'
    # maxpage = input("최대 출력할 페이지수 입력하시오: ")
    # query = input("검색어 입력: ")
    # s_date = input("시작날짜 입력(2019.01.01):")  # 2019.01.01
    # e_date = input("끝날짜 입력(2019.04.28):")  # 2019.04.28
    # get_news(maxpage, query, s_date, e_date)  # 검색된 네이버뉴스의 기사내용을 크롤링
    scraper(maxpage, query, s_date, e_date)
    find_syn()
    # make_wordcloud(100)

main()
