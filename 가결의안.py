from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import time
import pandas as pd
from bs4 import BeautifulSoup
import re

#가결된 의안 함수 짜기

#몇 대
#21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, CC(국가보위입법회의), 10, 09, BB(비상국무회의), 08, 07, 06, AA(국가재건최고회의), 05, 04, 03, 02, 01

#무슨 안
#전체, 헌법개정, 예산안, 결산, 법률안, 동의안, 승인안, 결의안, 건의안, 규칙안, 선출안, 중요동의, 의원징계, 윤리심사

#무슨 위원회
#소관위원회전체, 9700005 ~


def final_bill(year, kind, comm):
    driver = webdriver.Chrome()
    url = "https://likms.assembly.go.kr/bill/FinishBill.do"
    driver.get(url)
    time.sleep(3)

    #가결 탭
    driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div[2]/a[2]').click()

    #인수받은 걸로 결정하기
    #몇대?
    dropdown_year = Select(driver.find_element(By.XPATH, "/html/body/div/div[2]/div[2]/div/div[1]/div/div[1]/select[1]"))
    dropdown_year.select_by_value(str(year))
    
    #무슨종류?
    dropdown_kind = Select(driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div[1]/div/div[1]/select[2]'))
    dropdown_kind.select_by_value(str(kind))
    
    #무슨 위원회?
    dropdown_comm = Select(driver.find_element(By.XPATH, '//*[@id="committeeSelectBox"]'))
    dropdown_comm.select_by_value(str(comm))
    
    
    #100건씩 보이게 하자
    dropdown_100 = Select(driver.find_element(By.XPATH,'//*[@id="pageSizeOption"]'))
    dropdown_100.select_by_value('100')
    
    
    #총 몇건
    text = driver.find_element(By.CSS_SELECTOR, 'body > div > div.contentWrap > div.subContents > p > span').text
    total_num = int(re.sub(r'[^0-9]', '', text))
    total_page = total_num//100 +1

    #필요한 리스트 만들기
    num = []
    name = []
    name_detail = []
    bywhom = []
    s_date = []
    r_date = []
    where = []
    d_date = []
    result = []
    
    #총 페이지 수 = total_page
    for pagenum in range(1,total_page+1):

        if pagenum <12:
            pagenum = pagenum

        else:
            if pagenum%10<2:
                pagenum = pagenum%10 + 12
            else:
                pagenum = pagenum%10 + 2

        try:
            driver.find_element(By.XPATH, f'//*[@id="pageListViewArea"]/a[{str(pagenum)}]').click()

        except NoSuchElementException:
            pass

        #개수 구해서 그거대로 돌리기
        howmany = driver.find_elements(By.CLASS_NAME, 'alignL')

        for i in range(1,len(howmany)+1):
            num.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(1)').text)
            name.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td.alignL > a').text)
            name_detail.append(driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[3]/table/tbody/tr[{str(i)}]/td[2]/a').get_attribute('href'))
            bywhom.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(3)').text)
            s_date.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(4)').text)
            r_date.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(5)').text)
            where.append(driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[3]/table/tbody/tr[{str(i)}]/td[6]').get_attribute('title'))
            d_date.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(7)').text)
            result.append(driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[3]/table/tbody/tr[{str(i)}]/td[8]').get_attribute('title'))


    rules = dict()
    rules['num'] = num
    rules['name'] = name
    rules['name_detail'] = name_detail
    rules['bywhom'] = bywhom
    rules['s_date'] = s_date
    rules['r_date'] = r_date
    rules['where'] = where
    rules['d_date'] = d_date
    rules['result'] = result

    rules_df = pd.DataFrame.from_dict(rules)
    name = '_'+str(year)+'_'+str(kind)+'_'+str(comm)
    rules_df.to_csv(f'/Users/admin/Documents/마부작침/의안정보크롤링/finish_{name}.csv')

    driver.quit()
