import os
from selenium import webdriver

driver = webdriver.Chrome(os.getcwd() + '/chromedriver')
driver.implicitly_wait(50)

driver.get('https://news.naver.com/main/read.nhn?m_view=1&includeAllCount=true&mode=LSD&mid=sec&sid1=102&oid=003&aid=0009172141')

cBox = driver.find_elements_by_css_selector('div[class=u_cbox_comment_box]')
cList = []

for i in range(cBox.__len__()):
    cList.append(cBox[i].find_element_by_css_selector('span[class=u_cbox_contents]').text)

print(cList)