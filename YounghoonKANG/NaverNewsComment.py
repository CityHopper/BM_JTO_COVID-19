from selenium import webdriver
import time
url = 'https://news.naver.com/main/read.nhn?mode=LSD&mid=shm&sid1=105&oid=092&aid=0002185333'

#웹 드라이버
driver = webdriver.Chrome('./chromedriver.exe')
driver.implicitly_wait(12)
driver.get(url)
driver.find_element_by_css_selector('span.u_cbox_in_view_comment').click()

#더보기 계속 클릭하기
while True:
    try:
        seemore = driver.find_element_by_css_selector('span.u_cbox_page_more')
        seemore.click()
        time.sleep(1)
    except:
        break

#댓글추출
contents = driver.find_elements_by_css_selector('span.u_cbox_contents')
for content in contents:
    print(content.text)
