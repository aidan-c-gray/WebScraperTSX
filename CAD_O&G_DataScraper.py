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

pages = [] 
for page_number in range(1,3):
        url_start = 'https://disfold.com/'
        url_end = 'canada/industry/oil-gas-e-p/companies/?page='
        url = url_start + url_end + str(page_number)
        pages.append(url)

values_list = []
ticker_list = [] 
for page in pages:
    webpage = requests.get(page)
    soup = bs(webpage.text, 'html.parser')
    stock_table = soup.find('table', class_ = 'striped')
    tr_tag_list = stock_table.find_all('tr')

    for each_tr_tag in tr_tag_list[1:]:
        td_tag_list = each_tr_tag.find_all('td')

        row_values = []
        for each_td_tag in td_tag_list[1:4]:
            new_value = each_td_tag.text.strip()
            row_values.append(new_value)
        if(len(row_values) == 3 ):
            trim_mc = row_values[1]
            unit_mc = trim_mc[-1]
            value_mc = float(trim_mc.split(' ', 1)[0][1:])
            a_tag_list = each_td_tag.find_all('a')
            ticker_col = []
            if((value_mc > 100 and unit_mc == 'M') or (unit_mc == 'B')):
                for each_a_tag in a_tag_list:
                    new_ticker = each_a_tag.text.strip()
                    ticker_col.append(new_ticker)
                if(ticker_col[0] != 'CGXEF' and ticker_col[0] != '0XD' and ticker_col[0] != 'PIPE' and ticker_col[0] != 'AFE' and ticker_col[0] != 'SNM'):
                    ticker_list.append(ticker_col[0])
        values_list.append(row_values)

data_folder = "data"

with open(os.path.join("Ticker", 'ticker_list'), 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(ticker_list)

historical_link = []
for ticket_index in range(0, len(ticker_list)):
    url_start = 'https://finance.yahoo.com/quote/'
    url_ticker = ticker_list[ticket_index] + ".TO"
    url_mid = '/history?p='
    url = url_start + url_ticker + url_mid + url_ticker
    historical_link.append(url)

for company in historical_link: 

    chrome_options = Options()
    chrome_options.add_argument('--headless')

    browser = webdriver.Chrome(options=chrome_options)
    browser.get(company)
    dropdown  = browser.find_element(By.XPATH, "//*[@id=\"Col1-1-HistoricalDataTable-Proxy\"]/section/div[1]/div[1]/div[1]/div/div/div/span")
    dropdown.click()
    date_range = browser.find_element(By.XPATH, "//*[@id=\"dropdown-menu\"]/div/ul[2]/li[4]/button/span")
    date_range.click()
    apply = browser.find_element(By.XPATH, "//*[@id=\"Col1-1-HistoricalDataTable-Proxy\"]/section/div[1]/div[1]/button/span")
    apply.click()

    parsed_url = urlparse(company)
    path_components = parsed_url.path.split("/")
    stock_ticker = path_components[2] 

    browser.implicitly_wait(10)

    time.sleep(3)  

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

    csv_filename = os.path.join(data_folder, f'{stock_ticker}_historical_data.csv')
    with open(csv_filename, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)

        for row in rows[1:]:
            columns = row.find_all(['td'])
            row_data = [column.text.strip() for column in columns]
            csv_writer.writerow(row_data)


    browser.quit()

print('--- %s seconds ---' % (time.time() - start_time))
