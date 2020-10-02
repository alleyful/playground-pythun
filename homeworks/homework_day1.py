import dload

from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Chrome('../chromedriver')
driver.get("https://search.daum.net/search?w=img&nil_search=btn&DA=NTB&enc=utf8&q=%EC%95%84%EA%B9%BD%EC%9D%B4")
time.sleep(5)

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

images = soup.select('#imgList > div > a > img')

i = 1
for image in images:
    src = image['src']
    dload.save(src, f'img_homework/{i}.jpg')
    i += 1

driver.quit()