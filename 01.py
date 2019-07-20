import requests
import csv
from decouple import config
from datetime import datetime, timedelta
from pprint import pprint 
# datetime(2019,7,19) - timedelta(weeks=i) # i주 이전의 시각을 구함.
# targetDt.strftime('%Y%m%d') => 20190713형식으로 해줌.

# --------------------------------------------------------------------------------------------------------------------------------------
# 선생님 풀이
result = {}

for i in range(50):
    key = config('KEY')
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=i) #7월 13일부터 과거 50주간이 필요
    targetDt = targetDt.strftime('%Y%m%d') 

    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?&key={key}&targetDt={targetDt}&weekGb=0'
    api_data = requests.get(url).json() # 크롬에서 보이는 것과 같은 모습으로 표현해줌
    pprint(api_data)
    # 주간/주말 박스오피스 데이터 리스트로 가져오기.
    movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')

    # 영화 대표코드 / 영화명 / 누적관객수

    # 영화정보가 담긴 딕셔너리에서 영화 대표 코드를 추출
    for movie in movies:
        code = movie.get('movieCd') # 키 안에 딕셔너리 만들기
        # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어가 있다면,
        # 그게 가장 마지막 주 데이터다. 즉 기존 영화코드가 있다면 딕셔너리에 넣지 않는다.
        if code not in result: # result안에 없다면 추가
            result[code] = {
                'movieCd': movie.get('movieCd'),
                'movieNm': movie.get('movieNm'),
                'audiAcc': movie.get('audiAcc')
            }
  #  pprint(result)

with open('boxOffice.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movieCd', 'movieNm', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        print(value)
        writer.writerow(value)



#----------------------------------------------------------------------------------------------------------------------------------------
# key = config('KEY')
# targetDt='20190713'

# res = requests.get(f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?&key={key}&targetDt={targetDt}&weekGb=0') #회차정보 받아서 요청보냄
# movies = res.json()

# list_movies = movies['boxOfficeResult']['weeklyBoxOfficeList']
# movies_boxoffice=[]


# for i in range(0,len(list_movies)): 
#     if list_movies[i] not in movies_boxoffice:
#         movies_boxoffice.append(list_movies[i])
# print(movies_boxoffice)

# movieNm = []
# movieCd = []
# audiAcc = []
# for i in range(0,len(movies_boxoffice)):
#     movieNm.append(movies_boxoffice[i].get('movieNm'))
#     movieNm.append(movies_boxoffice[i].get('movieCd'))
#     movieNm.append(movies_boxoffice[i].get('audiAcc'))


           

# # 1. csv.DictWriter()
# with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f: # with 쓰면 close 쓸 필요 없음
#     # 저장할 데이터들의 필드 이름을 미리 정한다.
#     fieldnames = ('movieCd', 'movieNm', 'audiCnt')
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     # 필드 이름을 csv 파일 최상단에 작성한다.
#     writer.writeheader()

#     # 딕셔너리를 순회하며 key를 통해 한 줄씩(value를) 작성한다.
#     for movie in movies_boxoffice: # 리스트 안에 있는 딕셔너리를 갖는다.
#         writer.writerow(movie)

# # 2 csv.DictReader()
# with open('boxoffice.csv', newline='', encoding='utf-8') as f:
#     reader = csv.DictReader(f) # 읽어올 파일만 입력=>reader에 파일이 들어있음

#     # 한 줄씩 읽는다.
#     for row in reader:
#         print(row['movieCd'])
#         print(row['movieNm'])
#         print(row['audiCnt'])
        