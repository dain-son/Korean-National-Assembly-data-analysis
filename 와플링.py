from google.colab import drive
drive.mount('/content/drive')

import pandas as pd
balui = pd.read_csv('/content/drive/MyDrive/마부작침/21국회/gongbal20_unique.csv', encoding='utf-8')
pogyul = pd.read_csv('/content/drive/MyDrive/마부작침/21국회/pogyul_20_name_num.csv', encoding='utf-8')

balui['no'] = balui['co.title'].str.extract('(\d+)')
bal_df = balui[['no','co.member.no','co.member.name','names','dangs','unique_pyo','unique_net']]
bal_df['co.member.no'] = bal_df['co.member.no'].fillna(-1)
bal_df['co.member.no'] = bal_df['co.member.no'].astype(int)

# 의안번호 unique값 list
unique_num = bal_df['no'].unique().tolist()

# 의원번호 unique값 list
list = []
for i in range(len(pogyul)):
    name_num =eval(pogyul.iloc[i]['pros_name_num'])
    list.append(name_num)
uiwon = {'list':list}

unique_list= []
for i in range(len(uiwon)):
    for j in uiwon.iloc[i,0]:
        if j in unique_list:
            pass
        else:
            unique_list.append(j)

# 의원번호, 이름 unique값 들어있는 데이터프레임 만들기
df = pd.DataFrame(unique_list)

num_list = []
for i in unique_list:
    num = re.sub('[^0-9]','', i)
    num_list.append(num)

name_list = []
for i in unique_list:
    name = re.sub(r'[0-9]','', i)
    name_list.append(name)

uiwon_list = {'unique_pyo':name_list, 'num':num_list, 'name_num':unique_list}
uiwon_df = DataFrame(uiwon_list)


bal_df = pd.merge(bal_df, uiwon_df, on="unique_pyo", how="inner")
bal_df2 = bal_df[['no','unique_pyo','num','dangs']]
bal_df3 = bal_df2[['no','num']]
bal_df4 = bal_df3.groupby('no')['num'].apply(tuple).reset_index(name="bal_num")
bal_df4['no'] = bal_df4['no'].astype(int)
df = pogyul[['no','pros_num','cons_num','abs_num']]

# 의안별 찬성, 반대, 기권한 의원 데이터프레임 만들기
no_list=[]
chan_list=[]
ban_list=[]
abs_list=[]

for i in range(len(df)):

    no=df.iloc[i]['no']
    no_list.append(no)

    chan_num=eval(df.iloc[i]['pros_num'])
    chan_list.append(chan_num)

    ban_num=eval(df.iloc[i]['cons_num'])
    ban_list.append(ban_num)

    abs_num=eval(df.iloc[i]['abs_num'])
    abs_list.append(abs_num)

waff = {'no':no_list,'chan_num':chan_list, 'ban_num':ban_list, 'abs_num':abs_list}
waff_df = pd.DataFrame.from_dict(data=waff, orient='columns')

#의안별 와플링(참석x, 반대, 기권) 데이터프레임 만들기

df2 = pd.merge(waff_df, bal_df4, on='no', how='inner')

waff=[]
waff_ban=[]
waff_abs=[]

for i in range(len(df2)):
    bal = df2.iloc[i]['bal_num']
    chan = df2.iloc[i]['chan_num']
    ban = df2.iloc[i]['ban_num']
    abs = df2.iloc[i]['abs_num']

    waf = []
    waf_ban = []
    waf_abs = []

    for j in range(len(bal)):
        if bal[j] in ban:
            waf_ban.append(str(bal[j]))
        elif bal[j] in ban:
            waf_abs.append(str(bal[j]))
        elif bal[j] not in chan:
            waf.append(str(bal[j]))
        else:
            pass
    waff.append(waf)
    waff_ban.append(waf_ban)
    waff_abs.append(waf_abs)

dic = {'no':df2['no'], 'waffling_ban_uiwon':waff_ban, 'waffling_abs_uiwon':waff_abs,'waffling_uiwon':waff}
waffling_df = pd.DataFrame.from_dict(data=dic, orient='columns')

#의원별 와플링(참석x, 반대, 기권) count 데이터프레임 만들기
waff_list=[]
waff_ban_list=[]
waff_abs_list=[]

for i in range(len(waffling_df)):
    waff_ban_list.extend(waffling_df.iloc[i]['waffling_ban_uiwon'])
    waff_list.extend(waffling_df.iloc[i]['waffling_uiwon'])
    waff_abs_list.extend(waffling_df.iloc[i]['waffling_abs_uiwon'])

counting=[]
counting_ban=[]
counting_abs=[]
for i in unique_num:
    counting.append(waff_list.count(i))
    counting_ban.append(waff_ban_list.count(i))
    counting_abs.append(waff_abs_list.count(i))
dic1 = {'uiwon':unique_num, 'waff_count':counting, 'waff_ban_counting':counting_ban,'waff_abs_counting':counting_abs}
waff_count_df = pd.DataFrame.from_dict(data=dic1, orient='columns')

# 발의 수 count
bal_list = []
for i in range(len(df2)):
    bal_list.extend(df2.iloc[i]['bal_num'])

num_name = bal_df2[['unique_pyo','num','dangs']]
num_name = num_name.drop_duplicates(subset='num')
num_name = num_name.rename(columns ={"num":"uiwon"})

#waffling count 데이터프레임에 의원 고유번호 기준으로 이름, 정당 붙이기
waff_join= pd.merge(waff_count_df, num_name, on="uiwon", how="inner")

bal_counting=[]
for i in unique_num:
    bal_counting.append(bal_list.count(i))
dic2 = {'uiwon':unique_num, 'bal_count':bal_counting}
bal_count_df = pd.DataFrame.from_dict(data=dic2, orient='columns')

waff_join2 = pd.merge(waff_join, bal_count_df, on='uiwon', how='inner')
waff_join2['와플링/발의_비율']=waff_join2['waff_count']/waff_join2['bal_count']
waff_join2.to_csv('/content/drive/MyDrive/마부작침/21국회/20대_와플링_동명이인구분.csv', encoding='utf-8')



# 각 의원이 어떤 법안 와플링했는지 찾는 함수
import pandas as pd

gongbal = pd.read_csv('/Users/mabuintern/Desktop/21대국회/data/gongbal_1211_병합.csv', encoding="utf-8")
uiwon = pd.read_csv('/Users/mabuintern/Desktop/21대국회/data/국회의원명단_장관_사임_포함_1107.csv', encoding="utf-8")

rep_bal_df = uiwon[['정당','의원명']]
rep_bal_df.rename(columns={'의원명':'rep_bal'}, inplace=True)
rep_bal = pd.merge(gongbal[['number','rep_bal']],rep_bal_df, on='rep_bal', how="left")
rep_bal.rename(columns={"number":"num"}, inplace=True)

uiwon['uniquenum'] = uiwon['uniquenum'].fillna(0).astype(int)

waff_what = pd.read_csv('/Users/mabuintern/Desktop/21대국회/data/와플링_의원별_어떤의안.csv', encoding="utf-8")
waff_what.rename(columns={"Unnamed: 0":"uniquenum"}, inplace=True)
waff_what = pd.merge(waff_what, uiwon[['의원명','정당','uniquenum']], on='uniquenum', how="left")

rules = pd.read_csv('/Users/mabuintern/Desktop/21대국회/data/전체의안_1209.csv', encoding="utf-8")
rules = rules[['num','name','bywhom']]

# convert float columns to int columns
list2=[]
for x in list(range(0,50)):
    list2.append(str(x))
waff_what[list2] = waff_what[list2].fillna(0).astype(int)

def find_waff(uiwon_name):
    waff_list = []
    for i in range(50):
        waff_list.append(waff_what[waff_what['의원명']==uiwon_name][str(i)][waff_what[waff_what['의원명']==uiwon_name].index[0]])
    waff_list = [value for value in waff_list if value !=0]

    waff_df = pd.DataFrame(waff_list, columns=['num'])
    waff_df['num'] = waff_df['num'].astype(str)
    waff_df = pd.merge(waff_df, rules, on='num', how='left')
    waff_df = pd.merge(waff_df, rep_bal, on='num', how='left')
    waff_df.rename(columns={"num":"의안번호","name":"의안명","bywhom":"종류","rep_bal":"대표발의자"}, inplace=True)
    waff_df.to_csv(f'/Users/mabuintern/Desktop/21대국회/data/waffling/waff_{uiwon_name}.csv', encoding="utf-8")
    
    return waff_df
