
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome()
driver.get('https://likms.assembly.go.kr/bill/main.do')
click_box = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/a[2]/img')
click_box.click()

from selenium.webdriver.support.ui import Select
#21대 국회 선택시 안해도됨
#20대 국회 선택시 select_by_index(1)
#dropdown=Select(driver.find_element(By.XPATH, '//*[@id="searchAgeFrom"]')).select_by_index(1)

bill_vote = []

for i in range(1,351): # 맨 첫 페이지, 맨 마지막 페이지
    if i < 12:
        page=str(i)
    elif i %10 ==0:
        page=str(12)
    elif i %10 ==1:
        page=str(13)
    else:
        page = str(i%10 +2)
    
    driver.find_element(By.XPATH, f'//*[@id="pageListViewArea2"]/a[{page}]').click()
    time.sleep(2)
    
    for i in range(1,11):
        page1 = str(i) 
        no= driver.find_element(By.XPATH, f'//*[@id="tbody"]/tr[{page1}]/td[3]').text
        driver.find_element(By.XPATH, f'//*[@id="tbody"]/tr[{page1}]/td[4]/a').click()
        
        try:
            
            #의안명
            name = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/h3/a').text
            name = re.sub(r"[^가-힣]","",name) 
            #찬성 인원
            pros = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div/div[3]/p').text
            pros = re.sub(r'[^0-9]','',pros)
            #찬성 의원 이름
            pros_name = driver.find_element(By.XPATH, '//*[@id="tbody"]').text.replace("\n"," ").strip().replace(" ",",")
            pros_name = pros_name.split(',')
        
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            #찬성 의원 고유번호 href에서 가져오기
            pros_data = soup.find("tbody", id="tbody")
            pros_name1 = pros_data.find_all('a')
            pros_num = []
            for i in pros_name1:
                href = i.attrs['href']
                numbers = re.sub(r'[^0-9]','',href)
                pros_num.append(numbers)

            #찬성 의원 이름+고유번호 list 만들어놓기
            pros_name_num = [x+y for x,y in zip(pros_name, pros_num)]
        
            #반대 인원
            cons = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div/div[4]/p').text
            cons = re.sub(r'[^0-9]','',cons)
            #반대 의원 이름
            cons_name = driver.find_element(By.XPATH, '//*[@id="tbody1"]').text.replace("\n"," ").strip().replace(" ",",")
            cons_name = cons_name.split(',')
            #반대 의원 고유번호
            cons_data = soup.find("tbody", id="tbody1")
            cons_name1 = cons_data.find_all('a')
            cons_num = []
            for i in cons_name1:
                href = i.attrs['href']
                numbers = re.sub(r'[^0-9]','',href)
                cons_num.append(numbers)

            cons_name_num = [x+y for x,y in zip(cons_name, cons_num)]
        
            #기권 인원
            abs = driver.find_element(By.XPATH, '/html/body/div/div[2]/div/div[2]/div/div[5]/p').text
            abs = re.sub(r'[^0-9]','',abs)
            #기권 의원 이름
            abs_name = driver.find_element(By.XPATH, '//*[@id="tbody2"]/tr').text.replace("\n"," ").strip().replace(" ",",")
            abs_name = abs_name.split(',')
            #기권 의원 고유번호
            abs_data = soup.find("tbody", id="tbody2")
            abs_name1 = abs_data.find_all('a')
            abs_num = []
            for i in abs_name1:
                href = i.attrs['href']
                numbers = re.sub(r'[^0-9]','',href)
                abs_num.append(numbers)
            
            abs_name_num = [x+y for x,y in zip(abs_name, abs_num)]
        
            #dict 합치기
            dict = {'no':no, 'name':name, 'pros':pros, 'pros_name':pros_name, 'pros_num':pros_num, 'pros_name_num':pros_name_num, 
                'cons':cons, 'cons_name':cons_name,'cons_num':cons_num, 'cons_name_num':cons_name_num,
                'abs':abs, 'abs_name':abs_name, 'abs_num':abs_num, 'abs_name_num':abs_name_num}    
            bill_vote.append(dict)
        except:
            pass
            
        driver.back()

df_vote = pd.DataFrame.from_dict(data=bill_vote, orient='columns')
df_vote.to_csv('/Users/mabuintern/Desktop/mabujakchim/20_bill_voting_member_data_name_num.csv', encoding='utf-8')


# 국회의원 고유번호 df 만들기
name_num = []
for i in range(3492):
    txt = df_vote['pros_name_num'].to_list()[i]
    for j in txt:
        name_num.append(j)

name_num=set(name_num)
name_num = pd.DataFrame(name_num)
name_num.to_csv('/Users/mabuintern/Desktop/mabujakchim/20_name_unique_num.csv', encoding='utf-8')
