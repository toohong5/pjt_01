import csv
import requests
from decouple import config
from pprint import pprint


result={}
# 1 csv.DictReader()
with open('movie.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f) # 읽어올 파일만 입력=>reader에 파일이 들어있음
    # 한 줄씩 읽는다.
    for row in reader:
        people_Nm = (row['감독명'],row['영화명(국문)']) # (감독명, 영화명) 튜플형식으로 저장.
        key = config('KEY')
        url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={key}&peopleNm={people_Nm[0]}'
        api_data = requests.get(url).json() # 크롬에서 보이는 것과 같은 모습으로 표현해줌

        directors_info = api_data.get('peopleListResult').get('peopleList')
        for info in directors_info:
            code = info.get('peopleCd')
            if people_Nm[0] == info.get('peopleNm') and people_Nm[1] in info.get('filmoNames'):
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
