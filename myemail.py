import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

load_dotenv()
EMAIL_ME = os.getenv('EMAIL_ME')
EMAIL_ME_PASSWORD = os.getenv('EMAIL_ME_PASSWORD')
EMAIL_YOU = os.getenv('EMAIL_YOU')

# 보내는 사람 정보
me = EMAIL_ME
my_password = EMAIL_ME_PASSWORD

# 로그인하기
s = smtplib.SMTP_SSL('smtp.gmail.com')
s.login(me, my_password)

# 받는 사람 정보
emails = [EMAIL_YOU]

for you in emails:
    # 메일 기본 정보 설정
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "추석기사 테스트"
    msg['From'] = me
    msg['To'] = you

    # 메일 내용 쓰기
    content = "추석에 뭐해?"
    part2 = MIMEText(content, 'plain')
    msg.attach(part2)

    part = MIMEBase('application', "octet-stream")
    with open("results/articles.xlsx", 'rb') as file:
        part.set_payload(file.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment", filename="추석기사.xlsx")
    msg.attach(part)

    # 메일 보내고 서버 끄기
    s.sendmail(me, you, msg.as_string())
s.quit()