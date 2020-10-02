import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from openpyxl import Workbook
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

load_dotenv()
EMAIL_ME = os.getenv('EMAIL_ME')
EMAIL_ME_PASSWORD = os.getenv('EMAIL_ME_PASSWORD')
EMAIL_YOU = os.getenv('EMAIL_YOU')

driver = webdriver.Chrome('../chromedriver')

wb = Workbook()
ws1 = wb.active
ws1.title = "articles"
ws1.append(["제목", "링크", "신문사", "썸네일"])
ws1.column_dimensions['A'].width = 50
ws1.column_dimensions['B'].width = 30
ws1.column_dimensions['C'].width = 10
ws1.column_dimensions['D'].width = 30

url = f"https://search.naver.com/search.naver?&where=news&query=추석"

driver.get(url)
req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

articles = soup.select('#main_pack > div.news.mynews.section._prs_nws > ul > li')

for article in articles:
    title = article.select_one('dl > dt > a').text
    href = article.select_one('dl > dt > a')['href']
    comp = article.select_one('span._sp_each_source').text.split(' ')[0].replace('언론사', '')
    thumbnail = article.select_one('div > a > img')['src']
    ws1.append([title, href, comp, thumbnail])

wb.save(filename='../results/articles.xlsx')
driver.quit()

# 보내는 사람 정보
me = EMAIL_ME
my_password = EMAIL_ME_PASSWORD

# 로그인하기
s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(me, my_password)

# 받는 사람 정보
you = EMAIL_YOU

# 메일 기본 정보 설정
msg = MIMEMultipart('alternative')
msg['Subject'] = "추석 기사 크롤링 과제"
msg['From'] = me
msg['To'] = you

# 메일 내용 쓰기
content = "스파르타 2일차 과제"
part2 = MIMEText(content, 'plain')
msg.attach(part2)

# 파일 첨부하기
part = MIMEBase('application', "octet-stream")
with open("../results/articles.xlsx", 'rb') as file:
    part.set_payload(file.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment", filename="추석기사모음.xlsx")
msg.attach(part)

# 메일 보내고 서버 끄기
s.sendmail(me, you, msg.as_string())
s.quit()