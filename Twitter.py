import GetOldTweets3 as got
from bs4 import BeautifulSoup

import datetime

###################################
yourquery = '치앙마이' # 검색어
datefirst = "2020-03-03" # 데이터 수집 시작 날짜
datelast = "2020-03-06" # 데이터 수집 끝 날짜, 수집에 포함 안됨
wcnum = 30 # 워드클라우드 단어 개수
###################################

days_range = []
start = datetime.datetime.strptime(datefirst, "%Y-%m-%d")
end = datetime.datetime.strptime(datelast, "%Y-%m-%d")
date_generated = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

for date in date_generated:
    days_range.append(date.strftime("%Y-%m-%d"))

print("=== 설정된 트윗 수집 기간은 {} 에서 {} 까지 입니다 ===".format(days_range[0], days_range[-1]))
print("=== 총 {}일 간의 데이터 수집 ===".format(len(days_range)))


# 특정 검색어가 포함된 트윗 검색하기 (quary search)
# 검색어 : 어벤져스, 스포
import time

# 수집 기간 맞추기
start_date = days_range[0]
end_date = (datetime.datetime.strptime(days_range[-1], "%Y-%m-%d")
            + datetime.timedelta(days=1)).strftime("%Y-%m-%d") # setUntil이 끝을 포함하지 않으므로, day + 1

# 트윗 수집 기준 정의
tweetCriteria = got.manager.TweetCriteria().setQuerySearch(yourquery)\
                                           .setSince(start_date)\
                                           .setUntil(end_date)\
                                           .setMaxTweets(-1)

# 수집 with GetOldTweet3
print("Collecting data started.. from {} to {}".format(days_range[0], days_range[-1]))
start_time = time.time()

tweet = got.manager.TweetManager.getTweets(tweetCriteria)

print("Collecting data ended.. {0:0.2f} Minutes".format((time.time() - start_time)/60))
print("=== Total num of tweets is {} ===".format(len(tweet)))


# 원하는 변수 골라서 저장하기
from random import uniform
from tqdm.notebook import tqdm

# initialize
tweet_list = []

import requests
def get_bs_obj(url):
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj

twitresult = []
for index in tqdm(tweet):
    # 메타데이터 목록
    username = index.username
    link = index.permalink
    content = index.text
    tweet_date = index.date.strftime("%Y-%m-%d")
    tweet_time = index.date.strftime("%H:%M:%S")
    retweets = index.retweets
    favorites = index.favorites

    # # === 유저 정보 수집 시작 === "유저 정보 수집은 시간이 엄청 걸리니까 필요없으면 빼자"
    # personal_link = 'https://twitter.com/' + username
    # try:
    #     bs_obj = get_bs_obj(personal_link)
    #     uls = bs_obj.find("ul", {"class": "ProfileNav-list"}).find_all("li")
    #     div = bs_obj.find("div", {"class": "ProfileHeaderCard-joinDate"}).find_all("span")[1]["title"]
    #
    #     # 가입일, 전체 트윗 수, 팔로잉 수, 팔로워 수
    #     joined_date = div.split('-')[1].strip()
    #     num_tweets = uls[0].find("span", {"class": "ProfileNav-value"}).text.strip()
    #     num_following = uls[1].find("span", {"class": "ProfileNav-value"}).text.strip()
    #     num_follower = uls[2].find("span", {"class": "ProfileNav-value"}).text.strip()
    #
    #
    #
    # except AttributeError:
    #     print("=== Attribute error occurs at {} ===".format(link))
    #     print("link : {}".format(personal_link))
    #     pass

    # 결과 합치기
    info_list = [tweet_date, tweet_time, username, content, link, retweets, favorites]
                 # joined_date, num_tweets, num_following, num_follower]
    tweet_list.append(info_list)
    twitresult.append(content)

    # 휴식
    # time.sleep(uniform(1, 2)) # 자꾸 오류나서 빼버림


# 파일 저장하기
import pandas as pd
pd.set_option('display.width', 400)
pd.set_option('display.max_columns', 10)
twitter_df = pd.DataFrame(tweet_list,
                          columns = ["date", "time", "user_name", "text", "link", "retweet_counts", "favorite_counts"])#,
                                    # "user_created", "user_tweets", "user_followings", "user_followers"])

# csv 파일 만들기
twitter_df.to_csv("scraped_twitter_data_{}_{}_to_{}.csv".format(yourquery, days_range[0], days_range[-1]), index=False, encoding='utf-8-sig')
print("=== {} tweets are successfully saved ===".format(len(tweet_list)))

# 파일 확인하기
df_tweet = pd.read_csv('scraped_twitter_data_{}_{}_to_{}.csv'.format(yourquery, days_range[0], days_range[-1]))
print(df_tweet.head(10)) # 위에서 10개만 출력


# 형태소 분류 및 워드클라우드 만들기
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def make_wordcloud(word_count): # 뉴스 타이틀과 내용만 워드클라우딩
    twitter = Okt()
    sentences_tag = []
    # 형태소 분석하여 리스트에 넣기
    for sentence in twitresult:
        morph = twitter.pos(sentence)
        sentences_tag.append(morph)
        print(morph)
        print('-' * 30)

    print(sentences_tag)
    print('\n' * 3)

    noun_adj_list = []

    # 메모장에 형태소가 분석된 모든 단어들을 저장
    f = open("scraped_twitter_words_{}_{}_to_{}.txt".format(yourquery, days_range[0], days_range[-1]), 'w', encoding='utf-8')
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
    plt.figure(figsize=(10, 8))
    plt.axis('off')
    plt.imshow(cloud)
    plt.show()

make_wordcloud(wcnum)