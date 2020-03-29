from selenium import webdriver
import time
url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=100&oid=015&aid=0004302572'

#웹 드라이버
driver = webdriver.Chrome('./chromedriver.exe')
driver.implicitly_wait(30)
driver.get(url)

#더보기 계속 클릭하기
while True:
    try:
        seemore = driver.find_element_by_css_selector('a.u_cbox_btn_more')
        seemore.click()
        time.sleep(1)
    except:
        break

#댓글추출
contents = driver.find_elements_by_css_selector('span.u_cbox_contents')
for content in contents:
    print(content.text)