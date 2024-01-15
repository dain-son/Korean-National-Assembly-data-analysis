
pogyul_nb = df_vote[['no','pros_num','cons_num','abs_num']]
pogyul_nb = pogyul_nb.reset_index(drop=True)

# 의원 이름 + 고유번호 있는 파일 불러오기
# 없으면 위 블럭 코드에서 실행한 후 googlesheet에서 파싱해서 저장 후 불러오면 됨
df = pd.read_csv('/Users/mabuintern/Desktop/mabujakchim/congress_activity/19_20_21/20대국회의원고유번호.csv', encoding='utf-8')
uiwon_nb = df['uniquenum']
uiwon = uiwon_nb.to_list()

# for문 돌려서 표결 df의 각 행에서 pros_num에 고유넘버 있으면 yes, cons_num에 고유넘버 있으면 no,
# abs_num에 고유넘버 있으면 abs 반환하는 함수

pg = dict()

for i in range(len(uiwon)): # 1~298
    uiwon_str = str(uiwon[i])
    uiwon_list = []
    for j in range(len(pogyul_nb)): # 1~2511
        if uiwon_str in ast.literal_eval(pogyul_nb.loc[j].to_list()[1]):
            uiwon_list.append(1)
            #dict[pogyul_nb.loc[j].to_list()[0]] = 1 #찬성
        elif uiwon_str in ast.literal_eval(pogyul_nb.loc[j].to_list()[2]):
            uiwon_list.append(2)
            #dict[pogyul_nb.loc[j].to_list()[0]] = 2 #반대
        elif uiwon_str in ast.literal_eval(pogyul_nb.loc[j].to_list()[3]):
            uiwon_list.append(3)
            #dict[pogyul_nb.loc[j].to_list()[0]] = 3 #기권
        else:
            uiwon_list.append(4)
            #dict[pogyul_nb.loc[j].to_list()[0]] = 4 #없음
    
    pg[f'{uiwon[i]}']= uiwon_list
    print(f'{i}' "is done")



# ‘표결현황.csv’와 ‘가결안.csv’을 의안고유번호로 join시켜서 위원회별 데이터프레임 만들기



# 위원회 별 의안 분리하기 - bill_voting_status_data.csv 만드는 코드는 아래에 !!
status = pd.read_csv('/Users/mabuintern/Desktop/21대국회/data/가결안_1209.csv', encoding="utf-8")
status = status[['num','name','where']]
status.rename(columns={"num":"no"}, inplace=True)

wnomi = pd.merge(pogyul_nb, status[['no','name','committee']], on='no', how='inner')

cmt = uiwon['committee'].unique().tolist()

# 노가다..ㅎㅎ
df정치개혁 = wnomi_2[wnomi_2['committee']=='정치개혁특별위원회']
df본회의 = wnomi_2[wnomi_2['committee']=='본회의']
df산업통상 = wnomi_2[wnomi_2['committee']=='산업통상자원중소벤처기업위원회']
df환노위 = wnomi_2[wnomi_2['committee']=='환경노동위원회']
df문체관광 = wnomi_2[wnomi_2['committee']=='문화체육관광위원회']
df보건복지 = wnomi_2[wnomi_2['committee']=='보건복지위원회']
df국토교통 = wnomi_2[wnomi_2['committee']=='국토교통위원회']
df행정안전 = wnomi_2[wnomi_2['committee']=='행정안전위원회']
df교육 = wnomi_2[wnomi_2['committee']=='교육위원회']
df외교통일 = wnomi_2[wnomi_2['committee']=='외교통일위원회']
df국방 = wnomi_2[wnomi_2['committee']=='국방위원회']
df법제사법 = wnomi_2[wnomi_2['committee']=='법제사법위원회']
df과기정통 = wnomi_2[wnomi_2['committee']=='과학기술정보방송통신위원회']

#노가다2
df국방 = df국방.loc[:,['no','pros_num','cons_num','abs_num']]
df보건복지 = df보건복지.loc[:,['no','pros_num','cons_num','abs_num']]
df정치개혁 = df정치개혁.loc[:,['no','pros_num','cons_num','abs_num']]
df본회의 = df본회의.loc[:,['no','pros_num','cons_num','abs_num']]
df산업통상 = df산업통상.loc[:,['no','pros_num','cons_num','abs_num']]
df환노위 = df환노위.loc[:,['no','pros_num','cons_num','abs_num']]
df문체관광 = df문체관광.loc[:,['no','pros_num','cons_num','abs_num']]
df행정안전 = df행정안전.loc[:,['no','pros_num','cons_num','abs_num']]
df교육 = df교육.loc[:,['no','pros_num','cons_num','abs_num']]
df외교통일 = df외교통일.loc[:,['no','pros_num','cons_num','abs_num']]
df법제사법 = df법제사법.loc[:,['no','pros_num','cons_num','abs_num']]

#노가다3
df국방 = df국방.reset_index(drop=True)
df보건복지 = df보건복지.reset_index(drop=True)
df정치개혁 = df정치개혁.reset_index(drop=True)
df본회의 = df본회의.reset_index(drop=True)
df산업통상 = df산업통상.reset_index(drop=True)
df환노위 = df환노위.reset_index(drop=True)
df문체관광 = df문체관광.reset_index(drop=True)
df행정안전 = df행정안전.reset_index(drop=True)
df교육 = df교육.reset_index(drop=True)
df외교통일 = df외교통일.reset_index(drop=True)
df법제사법 = df법제사법.reset_index(drop=True)

# w-nominate 형태의 데이터프레임 만들기 (ex: 법제사법위원회)
df = dict()

for i in range(len(uiwon)): # 1~298
    uiwon_str = str(uiwon[i])
    uiwon_list = []
    for j in range(len(df법제사법)): 
        if uiwon_str in ast.literal_eval(df법제사법.loc[j].to_list()[1]):
            uiwon_list.append(1)
            #dict[pogyul_nb.loc[j].to_list()[0]] = 1 #찬성
        elif uiwon_str in ast.literal_eval(df법제사법.loc[j].to_list()[2]):
            uiwon_list.append(2)
            #dict[pogyul_nb.loc[j].to_list()[0]] = 2 #반대
        elif uiwon_str in ast.literal_eval(df법제사법.loc[j].to_list()[3]):
            uiwon_list.append(3)
            #dict[pogyul_nb.loc[j].to_list()[0]] = 3 #기권
        else:
            uiwon_list.append(4)
            #dict[pogyul_nb.loc[j].to_list()[0]] = 4 #없음
    
    df[f'{uiwon[i]}']= uiwon_list
    print(f'{i}' "is done")
    
df = pd.DataFrame.from_dict(data=df, orient='columns')
df = df.T
df.to_csv('/Users/mabuintern/Desktop/mabujakchim/congress_activity/committee/법제사법_wnm.csv', encoding='utf-8')

# 표결현황(법률안 번호, 법률안 이름, 위원회, 찬성 수, 반대 수, 기권 수, 결과) 데이터프레임 만들기
driver = webdriver.Chrome()
driver.get('https://likms.assembly.go.kr/bill/main.do')
click_box = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/a[2]/img')
click_box.click()

bill_list = []

for i in range(1,252): # 맨 첫 페이지, 맨 마지막 페이지 
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
    
    tbody = driver.find_element(By.ID, 'tbody')
    rows = tbody.find_elements(By.TAG_NAME, "tr")

    for index, value in enumerate(rows):
        id=value.find_elements(By.TAG_NAME, "td")[0]
        date=value.find_elements(By.TAG_NAME, "td")[1]
        no=value.find_elements(By.TAG_NAME, "td")[2]
        name=value.find_elements(By.TAG_NAME, "td")[3]
        committee=value.find_elements(By.TAG_NAME, "td")[4]
        agree=value.find_elements(By.TAG_NAME, "td")[5]
        oppos=value.find_elements(By.TAG_NAME, "td")[6]
        abstention=value.find_elements(By.TAG_NAME, "td")[7]
        result=value.find_elements(By.TAG_NAME, "td")[8]
    
        dict = {'id':id.text, 'date':date.text, 'no':no.text, 'name':name.text, 'committee':committee.text, 
                'agree':agree.text, 'oppos':oppos.text, 'abstention':abstention.text, 'result':result.text}
    
        bill_list.append(dict)
    
df = pd.DataFrame.from_dict(data=bill_list, orient='columns')

df.to_csv('/Users/mabuintern/Desktop/mabujakchim/bill_voting_status_data.csv', encoding='utf-8')
