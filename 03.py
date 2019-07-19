import csv
import requests
from decouple import config
from pprint import pprint

# 1 csv.DictReader()
with open('movie.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f) # 읽어올 파일만 입력=>reader에 파일이 들어있음
    # 한 줄씩 읽는다.
    people_Nm=[]
    for row in reader:
        people_Nm.append(row['directors'])

result={}
# key = config('KEY')
# url2 = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={key}&peopleNm={peopleNm}'
# api_data2 = requests.get(url2).json()


# people_cd=[]
# for i in range(0,len(api_data2.get('peopleListResult').get('peopleList'))):
#     if people_Nm[i] in api_data2.get('peopleListResult').get('peopleList')[i].get('peopleNm'):
#         people_cd.append(api_data2.get('peopleListResult').get('peopleList')[i].get('peopleCd'))

# pprint(people_cd)

for i in people_Nm:
    key = config('KEY')
    peopleNm = i
    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={key}&peopleNm={peopleNm}'
    api_data = requests.get(url).json() # 크롬에서 보이는 것과 같은 모습으로 표현해줌

    directors_info = api_data.get('peopleListResult').get('peopleList')

# peopleCd, peopleNm, peopleNmEn, filmoNames
    for info in directors_info:
        code = info.get('peopleCd')

        result[code] = {
                    '영화인 코드': info.get('peopleCd'),
                    '영화인명': info.get('peopleNm'),
                    '분야': info.get('repRoleNm'),
                    '필모리스트': info.get('filmoNames')
                    
            }


with open('director.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('영화인 코드', '영화인명', '분야', '필모리스트')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        print(value)
        writer.writerow(value)