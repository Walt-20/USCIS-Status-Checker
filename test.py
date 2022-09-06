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

webdriver_service = Service(<path to chrome driver>) ## path to where you saved chromedriver binary
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)


url = 'https://egov.uscis.gov/casestatus/landing.do'

browser.get(url) 

caseno_input = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='receipt_number']")))
caseno_input.send_keys(<Case Number Here>)
WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[title='CHECK STATUS']"))).click()
time.sleep(3)
splash = browser.find_element(By.CLASS_NAME, "text-center")
header = splash.find_elements(By.TAG_NAME, 'h1')
for h in header:
    hdr = h.text
paragraph = splash.find_elements(By.TAG_NAME, 'p')
for p in paragraph:
    para = p.text

email = ""
pwd = ""

sms_gateway = [<numbers go here>]
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
