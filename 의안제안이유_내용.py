#의안 표 불러와서 유니크 값 골라내기
total_bill = pd.read_csv('/Users/admin/Documents/마부작침/의안정보크롤링/전체의안_2_1123.csv')

bill_unique = []

for each in total_bill['name_detail']:
    bill_unique.append(each.split("('")[1].split("'")[0])

total_bill['bill_unique'] = bill_unique

#의원발의 의안만!
bill_unique = list(total_bill[total_bill['bywhom']=='의원']['bill_unique'])
ori_num = list(total_bill[total_bill['bywhom']=='의원']['number'])


number = []
detail = []

#url 돌면서... 어어 가져오렴
for each in range(len(bill_unique)):
    url = f'https://likms.assembly.go.kr/bill/summaryPopup.do?billId={bill_unique[each]}'
    time.sleep(random.randint(1,3))
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    
    #의안 번호 뽑기
    number.append(soup.find_all('p', {'class':'textType01'})[0].text[-8:-1])
    
    #주요내용 뽑기
    try:    
        #내용 따
        texts = soup.find_all('div',{'class':'textType02 mt30'})
        text = ''
        for eachtext in texts:
            text+=eachtext.text
            text+='\n'
        detail.append(text)

    except (NoSuchElementException, IndexError):
        detail.append('no detail')

    #궁금하니깐요
    if each%100==99:
        print(f'{each+1}번째 완료')

rules_d = dict()
rules_d['ori_num'] = ori_num
rules_d['num'] = number
rules_d['detail'] = detail

rules_d_df = pd.DataFrame.from_dict(rules_d)
rules_d_df.to_csv(f'/Users/admin/Documents/마부작침/의안정보크롤링/rules_detail_1123.csv')


#------------------------------------------
#셀레니움으로 하려고 했던 것
#------------------------------------------

#re _ 아 이거는 너무 막힌다앙...
driver = webdriver.Chrome()
url = "https://likms.assembly.go.kr/bill/BillSearchResult.do"
driver.get(url)
time.sleep(3)

#몇대부터 몇대까지?
dropdown_from = Select(driver.find_element(By.XPATH,'//*[@id="si1_label01"]'))
dropdown_from.select_by_value('21')
dropdown_to = Select(driver.find_element(By.XPATH,'//*[@id="srchForm"]/div/div[1]/select[2]'))
dropdown_to.select_by_value('21')

#의안종류
dropdown_kind = Select(driver.find_element(By.XPATH,'//*[@id="si1_label02"]'))
dropdown_kind.select_by_value('전체')

#처리 상황
dropdown_stat = Select(driver.find_element(By.XPATH,'//*[@id="srchForm"]/div/div[2]/select[2]'))
dropdown_stat.select_by_value('')

#제안종류 (누가)
dropdown_who = Select(driver.find_element(By.XPATH,'//*[@id="srchForm"]/div/div[3]/select[1]'))
dropdown_who.select_by_value('전체')

#발의종류 (1인, 공동, 대표)
dropdown_who2 = Select(driver.find_element(By.XPATH,'//*[@id="si1_label03"]'))
dropdown_who2.select_by_value('전체')

#검색 버튼!
driver.find_element(By.XPATH, '//*[@id="srchForm"]/div/div[6]/button[1]').click()

#총 몇건?
text = driver.find_element(By.CSS_SELECTOR, 'body > div > div.contentWrap > div.subContents > div > p > span').text
total_num = int(re.sub(r'[^0-9]', '', text))
total_page = total_num//100 +1

#100건씩 보이게 하자
dropdown_100 = Select(driver.find_element(By.XPATH,'//*[@id="pageSizeOption"]'))
dropdown_100.select_by_value('100')



#필요한 리스트 만들기
#포함되어야 하는 것: 의안번호, 계류or처리, 의안명, 의안코드, 제안자구분, 제안일자, 의결일자, 의결결과, 주요내용, 심사진행상태
num = []
detail = []

 #총 페이지 수 = total_page
for pagenum in range(1,total_page+1):

    if pagenum <12:
        pagenum = pagenum
    else:
        if pagenum%10<2:
            pagenum = pagenum%10 + 12
        else:
            pagenum = pagenum%10 + 2

    #페이지 버튼 눌러
    try:
        driver.find_element(By.XPATH, f'//*[@id="pageListViewArea"]/a[{str(pagenum)}]').click()
    except NoSuchElementException:
        pass

    #개수 구해서 그거대로 돌리기 (번호 & 제안 이유 및 내용)
    howmany = driver.find_elements(By.CLASS_NAME, 'alignL')

    for i in range(1,len(howmany)+1):
        #번호 따
        num.append(driver.find_element(By.CSS_SELECTOR, f'body > div > div.contentWrap > div.subContents > div > div.tableCol01 > table > tbody > tr:nth-child({str(i)}) > td:nth-child(1)').text)
        #디테일 따
        try:
            #클릭해서 들어가
            driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr[{str(i)}]/td[7]/a').click()
            driver.switch_to.window(window_name = driver.window_handles[-1])
            #내용 따
            texts = driver.find_elements(By.CSS_SELECTOR, '#periodDiv > div > div')
            text = ''
            for each in texts:
                text+=each.text
                text+='\n'
            detail.append(text)
            #다시 돌아왕
            driver.close()
            driver.switch_to.window(window_name = driver.window_handles[0])
        except NoSuchElementException:
            detail.append('no_detail')

    #궁금하니까요
    if pagenum%10==0:
        print(pagenum + '페이지 완료')

rules_d = dict()
rules_d['num'] = num
rules_d['detail'] = detail

rules_d_df = pd.DataFrame.from_dict(rules_d)
name = '_'+str(fr)+'_'+str(to)+'_'+str(kind)+'_'+str(stat)+'_'+str(who)+'_'+str(who2)
rules_d_df.to_csv(f'/Users/admin/Documents/마부작침/의안정보크롤링/rules_detail_{name}.csv')

driver.quit()
