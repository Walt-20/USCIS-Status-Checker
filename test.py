import time
import requests
import json
import sys
from http import server
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



chrome_options = Options()
chrome_options.add_argument('headless')

webdriver_service = Service("/usr/bin/chromedriver") ## path to where you saved chromedriver binary
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)


url = 'https://egov.uscis.gov/casestatus/landing.do'

browser.get(url) 

caseno_input = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='receipt_number']")))
caseno_input.send_keys('IOE0914378133')
WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[title='CHECK STATUS']"))).click()
time.sleep(3)
splash = browser.find_element(By.CLASS_NAME, "text-center")
header = splash.find_elements(By.TAG_NAME, 'h1')
for h in header:
    hdr = h.text
paragraph = splash.find_elements(By.TAG_NAME, 'p')
for p in paragraph:
    para = p.text
# with open('file.txt', 'a') as f:
#     f.write('\nExecuted: {}'.format(ct))
#     f.write('{} \n {} \n'.format(h1, p))
# slack_url = "https://hooks.slack.com/services/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"
# message = (hdr + "\n" + para)
# title = (f"New Incoming Message :zap:")
# slack_data = {
#     "username": "NotificationBot",
#     "icon_emoji": ":satellite:",
#     #"channel" : "#somerandomcahnnel",
#     "attachments": [
#         {
#             "color": "#9733EE",
#             "fields": [
#                 {
#                     "title": title,
#                     "value": message,
#                     "short": "false",
#                 }
#             ]
#         }
#     ]
# }
# byte_length = str(sys.getsizeof(slack_data))
# headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
# response = requests.post(slack_url, data=json.dumps(slack_data), headers=headers)
# if response.status_code != 200:
#     raise Exception(response.status_code, response.text)

email = "ahwl77@gmail.com"
pwd = "gzlkzokwojlbvpwb"

sms_gateway = ['2697204070@msg.fi.google.com', '9159101469@msg.fi.google.com']
smtp = "smtp.gmail.com"
port = 587
server = smtplib.SMTP(smtp, port)
server.starttls()
server.login(email,pwd)
try:
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = ", ".join(sms_gateway)
    msg['Subject'] = "USCIS Notification"
    body = hdr + "\n" + para
    msg.attach(MIMEText(body, 'plain'))
    sms = msg.as_string()

    server.sendmail(email, sms_gateway, sms)

    server.quit()
except BaseException:
    print("Error: unable to send")