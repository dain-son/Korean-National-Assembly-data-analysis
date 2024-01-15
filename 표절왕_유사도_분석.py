#이걸로 불러오장
detail_who_clean = pd.read_csv('/Users/admin/Documents/마부작침/의안정보크롤링/rules_detail_who_clean.csv')

#유사도 행렬 구하기
tfidf = TfidfVectorizer(stop_words=['제안이유','주요내용','제안', '이유','주요','내용','안이유','대안'], min_df = 1)
tfidf_mat = tfidf.fit_transform(detail_who_clean['detail_clean_2'])

#23411개의 주요내용 / 274069개의 단어!
print(tfidf_mat.shape)

distance = (tfidf_mat * tfidf_mat.T)
adjm = distance.toarray()
print(len(adjm)) #23411

#유사도 경계 설정 후 0, 1 변환
adjm[adjm<0.8] = 0
adjm[adjm>=0.8] = 1

graph = nx.from_numpy_array(adjm)
PR = graph.to_undirected(adjm)
GC_list = list(PR.subgraph(c) for c in nx.connected_components(PR))
GC = sorted(GC_list, key=len, reverse=True)

cheatnodes = []

i=0
while True:
    if nx.number_of_nodes(GC[i]) >= 10:
        cheatnodes.append(nx.number_of_nodes(GC[i]))
        i+=1
    else:
        break

print(f'howmany={len(cheatnodes)} / {cheatnodes}')

# result: howmany=14 / [120, 44, 26, 19, 16, 15, 15, 15, 14, 12, 12, 12, 12, 10]

# 이제 내용을 살펴보장 
GC_detail_list = sorted(nx.connected_components(PR))
for each in GC_detail_list:
    if len(each)>=10:
        print(each)
