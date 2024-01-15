

import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

from selenium.common.exceptions import NoSuchElementException

#의안 표 불러와서 유니크 값 골라내기
total_bill = pd.read_csv('/Users/admin/Documents/마부작침/의안정보크롤링/전체의안_0904.csv')

bill_unique = []

for each in total_bill['name_detail']:
    bill_unique.append(each.split("('")[1].split("'")[0])

total_bill['bill_unique'] = bill_unique

total_bill_filt = total_bill[total_bill['bywhom']=='의원'].drop(['Unnamed: 0.1','Unnamed: 0','status','s_date','d_date','result','ongoing','name_detail'], axis=1).reset_index().drop('index',axis=1)

bill_unique = total_bill_filt['bill_unique']

#21대 국회 공동발의 의원 명단 다시!!!!!!!!! 뽑기 & 찬성의원

number = []
name = []
bal_people_list = []
bal_people_unique = []
chan_people_list = []
chan_people_unique = []

for each in range(len(bill_unique)):
    url = f'https://likms.assembly.go.kr/bill/coactorListPopup.do?billId={bill_unique[each]}'
    time.sleep(2)
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html,'html.parser')
    
    #의안 관련 정보 뽑기
    number.append(soup.find_all('p', {'class':'textType01 mt30'})[0].text.split(']')[0].replace('[',''))
    name.append(soup.find_all('p', {'class':'textType01 mt30'})[0].text.split(']')[1])
    
    #발의의원 명단 뽑기
    try:    
        div1 = soup.find_all('div',{'class':'links textType02 mt20'})[0]
        info1 = div1.find_all('a')

        person1 = []
        unique1 = []

        for num in range(len(info1)):
            person1.append(info1[num].text.strip())
            try: #잘했다 모거나
                unique1.append(int(re.sub(r'[^0-9]', '', info1[num]['href'])))
            except KeyError:
                unique1.append('no info')

        bal_people_list.append(person1)
        bal_people_unique.append(unique1)
        

    except (NoSuchElementException, IndexError):
        bal_people_list.append('')
        
    #찬성의원 명단 뽑기
    try:    
        div2 = soup.find_all('div',{'class':'links textType02 mt30'})[0]
        info2 = div2.find_all('a')

        person2 = []
        unique2 = []


        for num in range(len(info2)):
            person2.append(info2[num].text.strip())
            try:
                unique2.append(int(re.sub(r'[^0-9]', '', info2[num]['href'])))
            except KeyError:
                unique2.append('no info')

        chan_people_list.append(person2)
        chan_people_unique.append(unique2)

    except (NoSuchElementException, IndexError):
        chan_people_list.append('')    

    if each%100==99:
        print(f'{each+1}번째 완료')


gongbal = dict()
gongbal['number'] = number
gongbal['name'] = name
gongbal['bal_people_list'] = bal_people_list
gongbal['chan_people_list'] = chan_people_list

gongbal_df = pd.DataFrame.from_dict(gongbal)

gongbal_df.to_csv('/Users/admin/Documents/마부작침/의안정보크롤링/gongbal_Oct25.csv')


#----------------------------------------
# 의안별 대표 발의자 뽑기 
#----------------------------------------

rep_bal = []

bal = list(gongbal21_total['bal_people_list'])

for each in bal:
    repdetail = eval(each)[0]
    name = repdetail.split('(')[0]
    dang = repdetail.split('(')[1].split('/')[0]
    han = repdetail.split('(')[1].split('/')[1].replace(')','')
    
    if (name=='김병욱') and (dang=='더불어민주당'):
        rep_bal.append(han)
    elif (name=='이수진') and (han=='李壽珍'):
        rep_bal.append(han)
    else:
        rep_bal.append(name)

#----------------------------------------
#공동발의 명단 뽑기
#----------------------------------------

#안건 하나
url = 'https://likms.assembly.go.kr/bill/coactorListPopup.do?billId=PRC_L2J3K0I9J0H1P1Q5O2P7N0O8M9U1V9'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html,'html.parser')
info = soup.find_all('a', {'target':'_blank'}) #만악의 근원

name = []
dang = []
han_num = []
unique = []

for num in range(len(info)):
    name.append(info[num].text.split('(')[0])
    dang.append(info[num].text.split('(')[1].split('/')[0])
    han_num.append(info[num].text.split('(')[1].split('/')[1].replace(')',''))
    unique.append(int(re.sub(r'[^0-9]', '', info[num]['href'])))

names = dict()
names['name'] = name
names['dang'] = dang
names['han_num'] = han_num
names['unique'] = unique

print(names)
