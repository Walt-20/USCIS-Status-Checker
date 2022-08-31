import time
import requests
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



chrome_options = Options()
chrome_options.add_argument('headless')

webdriver_service = Service("<path to chrome driver>") ## path to where you saved chromedriver binary
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)


url = 'https://egov.uscis.gov/casestatus/landing.do'

browser.get(url) 

caseno_input = WebDriverWait(browser,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[id='receipt_number']")))
caseno_input.send_keys('<your case number ID>')
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
slack_url = "<your slack app>"
message = (hdr + "\n" + para)
title = (f"New Incoming Message :zap:")
slack_data = {
    "username": "NotificationBot",
    "icon_emoji": ":satellite:",
    #"channel" : "#somerandomcahnnel",
    "attachments": [
        {
            "color": "#9733EE",
            "fields": [
                {
                    "title": title,
                    "value": message,
                    "short": "false",
                }
            ]
        }
    ]
}
byte_length = str(sys.getsizeof(slack_data))
headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
response = requests.post(slack_url, data=json.dumps(slack_data), headers=headers)
if response.status_code != 200:
    raise Exception(response.status_code, response.text)