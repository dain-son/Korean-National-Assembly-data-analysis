#20대

import pandas as pd
import re
import json
import numpy as np


#source & target
nodes = pd.read_csv('/Users/admin/Documents/마부작침/국회/20대 국회의원 명단.csv')

#의원명단 구성
target=[]

for each in list(nodes['name']):
    target.append(each)

#번호 Id 만들기
Id = []

for i in range(1,len(target)+1):
    Id.append(i)

#edges dict 구성
edges = dict()

for each in target:
    edges[f'{each}'] = target

#weight dict 구성
weight = dict()

for each in target:
    weight[f'{each}'] = list(0 for i in range(len(target)))

#의안 정보 가져오고 공동발의자 리스트로 묶기
gongbal_unique_merge = pd.read_csv('/Users/admin/Documents/마부작침/국회/gongbal20_unique.csv')
gonbal20_list = gongbal_unique_merge.groupby('co.title')['unique_net'].apply(list).reset_index(name='bal')

#대표발의자 뽑아내기
rep_bal = []

for i in range(len(list(gonbal20_list['bal']))):
    rep_bal.append(list(gonbal20_list['bal'])[i][0])

gonbal20_list['rep_bal'] = rep_bal

#edges 딕셔너리에 순서가 담겨 있고
#weight에다가 인덱스 맞춰서 숫자를 늘리는거야!!!

for num in range(len(gonbal20_list)): #의안 하나씩 도는거
    rep = gonbal20_list.loc[num,'rep_bal'] #박정
    gongbal = gonbal20_list.loc[num,'bal'] #박정, 김경협, 노웅래, ...
    for each in gongbal:
        if each != rep: #rep이 박정, each가 김경협인 상황
            wgt_ind = edges[rep].index(each)
            weight[rep][wgt_ind] += 1
        else:
            pass

#Source Target

st = dict()
st_source = []
st_target = []
st_type = []
st_weight = []

for each in target:
    for i in range(len(edges[each])):
        st_target.append(each)
        st_source.append(edges[each][i])
        st_weight.append(weight[each][i])
        st_type.append('Directed')

st['Source'] = st_source
st['Target'] = st_target
st['Type'] = st_type
st['Weight'] = st_weight

st_df = pd.DataFrame.from_dict(st)
st_df.head()
st_df.to_csv('/Users/admin/Documents/마부작침/공동발의네트워크/공동발의네트워크_20_edges.csv', index=False)


#기호로 바꾸기
#Id = 의원 아이디 / target = 의원명
st_df_copy = st_df

for i in range(len(st_df)):
    for n in range(len(target)):
        if st_df_copy.loc[i,'Source'] == target[n]:
            st_df_copy.loc[i,'Source'] = Id[n]
            
        if st_df_copy.loc[i,'Target'] == target[n]:
            st_df_copy.loc[i,'Target'] = Id[n]
    if i % 10000==0:
        print(f'{i} 완료')

st_df_copy.to_csv('/Users/admin/Documents/마부작침/공동발의네트워크/공동발의네트워크_20_edges_num.csv', index=False)



#21대

import pandas as pd
import re
import json
import numpy as np

#nodes dict rntjd
nodes = pd.read_csv('/Users/admin/Documents/마부작침/의안정보크롤링/국회의원 명단_1214.csv')

#의원명단 구성
target=[]

for each in list(nodes['의원명']):
    target.append(each)

#번호 Id 만들기
Id = []

for i in range(1,len(target)+1):
    Id.append(i)

#동명이인 걍 다 한자로 처리하자!
for i in range(len(target)):
    if target[i]=='이수진(비)':
        print(i)

target[193] = '李壽珍'

#노드 만들기

nodes_dict = dict()
nodes_dict['Id'] = Id
nodes_dict['Name'] = target
nodes_dict['dang'] = list(nodes['정당'])
nodes_df = pd.DataFrame.from_dict(nodes_dict)
nodes_df.to_csv('/Users/admin/Documents/마부작침/공동발의네트워크/공동발의네트워크_21_nodes_1214.csv', index=False)


#edges dict 구성
edges = dict()

for each in target:
    edges[f'{each}'] = target

#weight dict 구성
weight = dict()

for each in target:
    weight[f'{each}'] = list(0 for i in range(len(target)))

#의안정보 가져와
gongbal21_total = pd.read_csv('/Users/admin/Documents/마부작침/의안정보크롤링/gongbal21_total.csv')

#317명의 대표발의자 (318명 중 우신구 제외)
len(set(list(gongbal21_total['rep_bal'])))

#weight dict 채우기
for num in range(len(gongbal21_total)): #의안 하나씩 도는거
    rep = gongbal21_total.loc[num,'rep_bal'] #이종성
    gongbal = eval(gongbal21_total.loc[num,'bal_people_list']) #이종성, 구자근, 박대수... (당, 한자까지)
    for each in gongbal:
        name = each.split('(')[0]
        dang = each.split('(')[1].split('/')[0]
        han = each.split('(')[1].split('/')[1].replace(')','')

        if (name=='김병욱') and (dang=='더불어민주당'):
            unique = han
        elif (name=='이수진') and (han=='李壽珍'):
            unique = han
        else:
            unique = name
        
        if unique != rep: #rep이 이종성, unique가 구자근인 상황
            wgt_ind = edges[rep].index(unique) #이종성 리스트의 14번 인덱스
            weight[rep][wgt_ind] += 1
        else:
            pass

#Source Target

st = dict()
st_source = []
st_target = []
st_type = []
st_weight = []

for each in target:
    for i in range(len(edges[each])):
        st_target.append(each)
        st_source.append(edges[each][i])
        st_weight.append(weight[each][i])
        st_type.append('Directed')

st['Source'] = st_source
st['Target'] = st_target
st['Type'] = st_type
st['Weight'] = st_weight

st_df = pd.DataFrame.from_dict(st)
st_df.head()
st_df.to_csv('/Users/admin/Documents/마부작침/공동발의네트워크/공동발의네트워크_21_edges_1214.csv', index=False)

#기호로 바꾸기
#Id = 의원 아이디 / target = 의원명
st_df_copy = st_df

for i in range(len(st_df)):
    for n in range(len(target)):
        if st_df_copy.loc[i,'Source'] == target[n]:
            st_df_copy.loc[i,'Source'] = Id[n]
            
        if st_df_copy.loc[i,'Target'] == target[n]:
            st_df_copy.loc[i,'Target'] = Id[n]
    if i % 10000==0:
        print(f'{i} 완료')

st_df_copy.to_csv('/Users/admin/Documents/마부작침/공동발의네트워크/공동발의네트워크_21_edges_num_1214.csv', index=False)
