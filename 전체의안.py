#전체의안 긁기 (계류+처리 / 안 종류 상관 없이)

def bill(fr, to, kind, stat, who, who2):
    #창 열기
    driver = webdriver.Chrome()
    url = "https://likms.assembly.go.kr/bill/BillSearchResult.do"
    driver.get(url)
    time.sleep(3)
    
    #몇대부터 몇대까지?
    dropdown_from = Select(driver.find_element(By.XPATH,'//*[@id="si1_label01"]'))
    dropdown_from.select_by_value(str(fr))
    dropdown_to = Select(driver.find_element(By.XPATH,'//*[@id="srchForm"]/div/div[1]/select[2]'))
    dropdown_to.select_by_value(str(to))
    
    #의안종류
    dropdown_kind = Select(driver.find_element(By.XPATH,'//*[@id="si1_label02"]'))
    dropdown_kind.select_by_value(str(kind))
    
    #처리 상황
    dropdown_stat = Select(driver.find_element(By.XPATH,'//*[@id="srchForm"]/div/div[2]/select[2]'))
    dropdown_stat.select_by_value(str(stat))
    
    #제안종류 (누가)
    dropdown_who = Select(driver.find_element(By.XPATH,'//*[@id="srchForm"]/div/div[3]/select[1]'))
    dropdown_who.select_by_value(str(who))
    
    #발의종류 (1인, 공동, 대표)
    dropdown_who2 = Select(driver.find_element(By.XPATH,'//*[@id="si1_label03"]'))
    dropdown_who2.select_by_value(str(who2))
    
    #검색 버튼!
    driver.find_element(By.XPATH, '//*[@id="srchForm"]/div/div[6]/button[1]').click()
    
    #필요한 리스트 만들기
    #포함되어야 하는 것: 의안번호, 계류or처리, 의안명, 의안코드, 제안자구분, 제안일자, 의결일자, 의결결과, 주요내용, 심사진행상태
    num = []
    status = []
    name = []
    name_detail = []
    bywhom = []
    s_date = []
    d_date = []
    result = []
    ongoing = []

    #총 몇건?
    text = driver.find_element(By.CSS_SELECTOR, 'body > div > div.contentWrap > div.subContents > div > p > span').text
    total_num = int(re.sub(r'[^0-9]', '', text))
    total_page = total_num//100 +1

    #100건씩 보이게 하자
    dropdown_100 = Select(driver.find_element(By.XPATH,'//*[@id="pageSizeOption"]'))
    dropdown_100.select_by_value('100')
    
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
            status.append(driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr[{str(i)}]/td[2]/div[1]/img').get_attribute('alt'))
            name.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td.alignL > div.pl25 > a').text)
            name_detail.append(driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr[{str(i)}]/td[2]/div[2]/a').get_attribute('href'))
            bywhom.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(3)').text)
            s_date.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(4)').text)
            d_date.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(5)').text)
            result.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(6)').text)
            ongoing.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(8)').text)

    rules = dict()
    rules['num'] = num
    rules['status'] = status
    rules['name'] = name
    rules['name_detail'] = name_detail
    rules['bywhom'] = bywhom
    rules['s_date'] = s_date
    rules['d_date'] = d_date
    rules['result'] = result
    rules['ongoing'] = ongoing

    rules_df = pd.DataFrame.from_dict(rules)
    name = '_'+str(fr)+'_'+str(to)+'_'+str(kind)+'_'+str(stat)+'_'+str(who)+'_'+str(who2)
    rules_df.to_csv(f'/Users/admin/Documents/마부작침/의안정보크롤링/rules{name}.csv')

    driver.quit()
