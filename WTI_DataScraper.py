import requests
from bs4 import BeautifulSoup as bs 
import time
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import csv
from urllib.parse import urlparse, parse_qs    
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

start_time = time.time() 

wti_link = "https://finance.yahoo.com/quote/CL=F/history/"

chrome_options = Options()
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(options=chrome_options)
browser.get(wti_link)
dropdown  = browser.find_element(By.XPATH, "//*[@id=\"Col1-1-HistoricalDataTable-Proxy\"]/section/div[1]/div[1]/div[1]/div/div/div/span")
dropdown.click()
date_range = browser.find_element(By.XPATH, "//*[@id=\"dropdown-menu\"]/div/ul[2]/li[4]/button/span")
date_range.click()
apply = browser.find_element(By.XPATH, "//*[@id=\"Col1-1-HistoricalDataTable-Proxy\"]/section/div[1]/div[1]/button/span")
apply.click()

parsed_url = urlparse(wti_link)
path_components = parsed_url.path.split("/")
stock_ticker = path_components[2] 

browser.implicitly_wait(10)

time.sleep(5)  

def scroll_to_bottom():
    
    actions = webdriver.ActionChains(browser)
    actions.send_keys(Keys.END)
    actions.perform()


for _ in range(100):  
    scroll_to_bottom()
    time.sleep(.5)  

table = browser.find_element(By.XPATH, "//*[@id=\"Col1-1-HistoricalDataTable-Proxy\"]/section/div[2]/table")

table_html = table.get_attribute("outerHTML")

soup = bs(table_html, 'html.parser')

rows = soup.find_all('tr')

header_row = rows[0]
headers = [header.text.strip() for header in header_row.find_all(['th'])]

csv_filename = os.path.join("data", 'WTI.TO_historical_data.csv')
with open(csv_filename, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(headers)

    for row in rows[1:]:
        columns = row.find_all(['td'])
        row_data = [column.text.strip() for column in columns]
        csv_writer.writerow(row_data)


browser.quit()

print('--- %s seconds ---' % (time.time() - start_time))