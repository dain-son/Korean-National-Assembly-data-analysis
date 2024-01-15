uiwon_list = []

for no1 in range(379, 411):
    no2 = 1
    
    while True:
        try:
            uiwon=[]
            
            #열어
            HTMLFile = open(f"/Users/mabuintern/Downloads/drive-download-20230907T064116Z-001/국회회의록_21대_{str(no1)}회_{str(no2)}차_국회본회의.html", "rt", encoding='utf-8').read()
            soup = BeautifulSoup(HTMLFile, 'html.parser')

            #몇회 몇차인지 적어
            uiwon.append(str(no1)+"회 "+str(no2)+"차")

            #출석 명단 찾아서 적어
            try:
                attr = soup.select('p')
                for i in range(len(attr)):
                    if "출석 의원" in attr[i].text:
                        j = i
                    elif "국회 참석자" in attr[i].text:
                        k = i
                # html에서 '출석 의원'과 '국회 참석자' 사이 모든 텍스트 붙이기
                for a in range(j,k):
                    uiwon.append(attr[a].text)
            except:
                pass
            uiwon_list.append(uiwon)
            #몇회 몇차인지 알려줘
            print(f'{str(no1)}회 {str(no2)}차 완료')   
            
            #차수 하나 올려
            no2+=1
        
            
        
        except FileNotFoundError:
            break
