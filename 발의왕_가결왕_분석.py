#21대 국회 공동발의 의원 명단 뽑기 & 찬성의원

number = []
name = []
bal_people_list = []
bal_people_unique = []
chan_people_list = []
chan_people_unique = []

for each in range(20739,len(bill_unique)):
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
gongbal['bal_people_unique'] = bal_people_unique
gongbal['chan_people_list'] = chan_people_list
gongbal['chan_people_unique'] = chan_people_unique

gongbal_df = pd.DataFrame.from_dict(gongbal)

gongbal_df.to_csv('/Users/admin/Documents/마부작침/의안정보크롤링/gongbal_21re.csv')



#크롤링한 후 중복 제거
num2 = list(df2['num'])
empty = []

for i in range(len(num2)):
    if num1[i] not in empty:
        empty.append(num2[i])
    else:
        print(i)



#각각 크롤링해둔 공동발의자 명단 합침
gongbal21_total = pd.concat([gongbal21,gongbal21_2], ignore_index=True)

#의안별 대표 발의자 뽑기
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

#사람 리스트 가져오기
members = pd.read_csv('/Users/admin/Documents/마부작침/의안정보크롤링/국회의원 명단_1127.csv')
member = list(members['의원명'])

#동명이인 걍 다 한자로 처리하자! (이수진, 김병욱)
for i in range(len(member)):
    if member[i]=='이수진(비)':
        print(i)

member[193] = '李壽珍'



#(1) 전체 의안 (공동, 대표) => 11/23 기준 의원 발의 의안 23293건
repbal_cnt = [0 for i in range(len(member))]
bal_cnt = [0 for i in range(len(member))]

for num in range(len(gongbal21_total['number'])): #의안 돌기
    #대표 발의자 카운트
    rep = gongbal21_total.loc[num,'rep_bal']
    rep_ind = member.index(rep)
    repbal_cnt[rep_ind] += 1

    #공동 발의자 카운트
    gong = eval(gongbal21_total.loc[num,'bal_people_list'])
    for each in gong:
        name = each.split('(')[0]
        dang = each.split('(')[1].split('/')[0]
        han = each.split('(')[1].split('/')[1].replace(')','')
        
        if (name=='김병욱') and (dang=='더불어민주당'):
            unique = han
        elif (name=='이수진') and (han=='李壽珍'):
            unique = han
        else:
            unique = name

        bal_ind = member.index(unique)
        bal_cnt[bal_ind] += 1

#숫자맞는지 꼭 확인=========
total=0

for each in repbal_cnt:
    total+=each

total
#=======================

members['rep_bal'] = repbal_cnt
members['gongbal'] = bal_cnt



#(2) 법률안 (공동, 대표) => 11/23 기준 의원 발의 의안 22910건
laws = pd.read_csv('/Users/admin/Documents/마부작침/의안정보크롤링/rules_1127__21_21_법률안__전체_전체.csv')
## 법률안 중 겹치는 거 재껴
for i in range(len(laws)-1):
    if laws.loc[i,'num']==laws.loc[i+1,'num']:
        print(f"{i}, 의안번호 {laws.loc[i,'num']}")
##지우고 인덱스 맞춰주기
laws = laws[(laws.index!=10199) & (laws.index!=21999)].reset_index()
laws = laws.drop(['Unnamed: 0','status','name_detail','s_date','d_date','result','ongoing'], axis=1)
laws = laws[laws['bywhom']=='의원'].reset_index().drop(['index','bywhom','level_0'],axis=1)

##merge 위해 데이터 타입 str로
laws.columns = ['number','name']
laws['number'] = laws['number'].astype(str)

#na값들은 크롤링 시간 차이 나서 생긴 것들이라 지워줌!
gongbal_laws = pd.merge(laws, gongbal21_total, how = 'left', on = ['number'])
gongbal_laws = gongbal_laws[gongbal_laws['bal_people_list'].isna() == False].reset_index()
gongbal_laws = gongbal_laws.drop(['index', 'name_x', 'Unnamed: 0', 'name_y'], axis=1)

#각 사람에다가 weight 값 추가하듯 해보장

repbal_law_cnt = [0 for i in range(len(member))]
bal_law_cnt = [0 for i in range(len(member))]

for num in range(len(gongbal_laws['number'])): #의안 돌기
    #대표 발의자 카운트
    rep = gongbal_laws.loc[num,'rep_bal']
    rep_ind = member.index(rep)
    repbal_law_cnt[rep_ind] += 1

    #공동 발의자 카운트
    gong = eval(gongbal_laws.loc[num,'bal_people_list'])
    for each in gong:
        name = each.split('(')[0]
        dang = each.split('(')[1].split('/')[0]
        han = each.split('(')[1].split('/')[1].replace(')','')
        
        if (name=='김병욱') and (dang=='더불어민주당'):
            unique = han
        elif (name=='이수진') and (han=='李壽珍'):
            unique = han
        else:
            unique = name

        bal_ind = member.index(unique)
        bal_law_cnt[bal_ind] += 1

members['repbal_law_cnt'] = repbal_law_cnt
members['bal_law_cnt'] = bal_law_cnt



#(3) 전체 의안 중 가결 (대표) => 11/23 기준 의원 발의 의안 1238건
rules_ok = pd.read_csv('/Users/admin/Documents/마부작침/의안정보크롤링/finish_1127__21_전체_소관위원회전체.csv')
rules_ok = rules_ok.drop(['Unnamed: 0','name_detail','s_date','r_date','where','d_date','result'], axis=1)
rules_ok = rules_ok[rules_ok['bywhom']=='의원'].reset_index().drop(['index','bywhom'],axis=1)
rules_ok.columns = ['number','name']
##문자로
rules_ok['number'] = rules_ok['number'].astype(str)

gongbal_ok = pd.merge(rules_ok, gongbal21_total, how = 'left', on = 'number')

repbal_ok_cnt = [0 for i in range(len(member))]

for num in range(len(gongbal_ok['number'])): #의안 돌기
    #대표 발의자 카운트
    rep = gongbal_ok.loc[num,'rep_bal']
    rep_ind = member.index(rep)
    repbal_ok_cnt[rep_ind] += 1

members['repbal_ok_cnt'] = repbal_ok_cnt

#(4) 법률안 중 가결 (대표) => 11/23 기준 의원 발의 의안 1110건
laws_ok = pd.read_csv('/Users/admin/Documents/마부작침/의안정보크롤링/finish_1127__21_법률안_소관위원회전체.csv')
laws_ok = laws_ok.drop(['Unnamed: 0','name_detail','s_date','r_date','where','d_date','result'], axis=1)
laws_ok = laws_ok[laws_ok['bywhom']=='의원'].reset_index().drop(['index','bywhom'],axis=1)
laws_ok.columns = ['number','name']
##문자로
laws_ok['number'] = laws_ok['number'].astype(str)

gongbal_laws_ok = pd.merge(laws_ok, gongbal21_total, how = 'left', on = ['number','name'])

repbal_laws_ok_cnt = [0 for i in range(len(member))]

for num in range(len(gongbal_laws_ok['number'])): #의안 돌기
    #대표 발의자 카운트
    rep = gongbal_laws_ok.loc[num,'rep_bal']
    rep_ind = member.index(rep)
    repbal_laws_ok_cnt[rep_ind] += 1

members['repbal_laws_ok_cnt'] = repbal_laws_ok_cnt



# R
#발의왕 분석
##공동발의
balking21_2 %>% filter(구분 %in% c('기본','장관')) %>%
	arrange((gongbal)) %>% select(의원명, 정당, 당선횟수, 구분, gongbal) %>% View()

##대표발의
balking21_2 %>% filter(구분 %in% c('기본','장관')) %>%
	arrange((rep_bal)) %>% select(의원명, 정당, 당선횟수, 구분, rep_bal) %>% View()

##법률안 공동발의 참여 횟수
balking21_2 %>% filter(구분 %in% c('기본','장관')) %>%
	arrange((bal_law_cnt)) %>% select(의원명, 정당, 당선횟수, 구분, bal_law_cnt) %>% View()

##법률안 대표발의 횟수
balking21_2 %>% filter(구분 %in% c('기본','장관')) %>%
	arrange((repbal_law_cnt)) %>% select(의원명, 정당, 당선횟수, 구분, repbal_law_cnt) %>% View()

##대표발의한 전체 의안 중 가결된 건수
balking21_2 %>% filter(구분 %in% c('기본','장관')) %>%
	arrange((repbal_ok_cnt)) %>% select(의원명, 정당, 당선횟수, 구분, repbal_ok_cnt) %>% View()

#대표발의한 전체 의안 중 가결률
balking21_2 %>% mutate(ratio=repbal_ok_cnt/rep_bal) %>%
	filter(ratio!=0) %>% filter(구분 %in% c('기본','장관')) %>%
	arrange((ratio)) %>% select(의원명, 정당, 당선횟수, 구분, ratio, repbal_ok_cnt, rep_bal) %>% View()

##대표발의한 법률안 중 가결된 건수
balking21_2 %>% filter(구분 %in% c('기본','장관')) %>%
	arrange((repbal_laws_ok_cnt)) %>% select(의원명, 정당, 당선횟수, 구분, repbal_laws_ok_cnt) %>% View()

##대표발의한 법률안 중 가결률
balking21_2 %>% mutate(ratio_law = repbal_laws_ok_cnt/repbal_law_cnt) %>%
	filter(ratio_law!=0) %>%
	arrange((ratio_law)) %>% select(의원명, 정당, 당선횟수, 구분, ratio_law, repbal_laws_ok_cnt, repbal_law_cnt) %>% View()
