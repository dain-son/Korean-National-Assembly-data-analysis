#표결한 의안(찬성, 반대, 기권) 크롤링한 것 가져오기
uiwon = pd.read_csv('표결현황_1212_병합.csv', encoding='utf-8')
uiwon = uiwon[['no','name', 'pros','cons','abs']]

#가결한 의안 크롤링한 것 가져오기
finish = pd.read_csv('finish_1211_병합.csv', encoding="utf-8")
finish = finish[['num','bywhom','s_date','r_date','where','d_date','result']]
# s_date: 제안일, r_date: 회부일, d_date: 의결일자

# 데이터 합치기
finish.rename(columns = {'num':'no'}, inplace=True)
uiwon = pd.merge(uiwon, finish, on="no", how="left")
# 중복되는 행 제거
uiwon = uiwon.drop_duplicates(['s_date','no','name'])

# 총 투표자 수 칼럼 추가하기
uiwon['attend'] = uiwon['pros']+ uiwon['cons'] + uiwon['abs']
# 찬성/반대/기권 비율 계산
uiwon['pros_ratio']=uiwon['pros']/uiwon['attend']
uiwon['cons_ratio']=uiwon['cons']/uiwon['attend']
uiwon['abs_ratio']=uiwon['abs']/uiwon['attend']

# 찬성율 100% 가결 의안
print(f"표결된 의안 {len(uiwon)}개 중 ",len(uiwon[uiwon['pros_ratio']==1.0]),"개(",round(len(uiwon[uiwon['pros_ratio']==1.0])/len(uiwon)*100,2),"%)는 만장일치로 가결")

uiwon = uiwon.rename(columns = {'no':'의안번호',
                        'name':'의안명',
                        'committee':'위원회',
                        'pros':'찬성',
                        'cons':'반대',
                        'abs':'기권',
                        'result':'결과',
                        'attend':'참석',
                        'pros_ratio':'찬성비율',
                        'cons_ratio':'반대비율',
                        'abs_ratio':'기권비율'})
uiwon['찬반_비율_차이'] = abs(uiwon['찬성비율']-uiwon['반대비율'])
uiwon.to_csv('/Users/mabuintern/Desktop/21대국회/표결분석_1209.csv', encoding="utf-8")

# 위원회별 의안
commi = pd.DataFrame({'count':uiwon.groupby(['위원회','결과']).size()}).reset_index().pivot_table(values='count',index='위원회', columns='결과').fillna(0)
commi['횟수'] = commi['수정가결']+commi['원안가결']
commi.to_csv('/Users/mabuintern/Desktop/21대국회/위원회별의안제출건수.csv',encoding='utf-8',sep=',')
