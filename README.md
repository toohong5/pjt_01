[TOC]



# pjt_01

## 1. 프로젝트

- 영화진흥위원회의 오픈 api를 이용한 데이터 수집 및 필요한 데이터 조작 및 가공

## 2.  `01.py`

### 1) 영화진흥위원회 오픈 API(주간/주말 박스오피스 데이터)

- 요청사항:
  1. 주간(월~일)까지 기간의 데이터를 조회합니다.
  2. 조회 기간은 총 50주이며, 기준일(마지막 일자)은 2019년 7월 13일입니다.
  3. 다양성 영화/상업 영화를 모두 포함하여야 합니다.
  4. 한국/외국 영화를 모두 포함하여야 합니다.
  5. 모든 상영지역을 포함하여야 합니다.
- 주간(월~일)까지의 데이터를 조회하기 위해 `weekGb=0`을 사용했다.

- url에서 `key`값과 `targetDt`를 변수로 설정해  API를 요청한다.

- `targetDt`는 2019년 7월 13일 기준으로 과거 50주간의 데이터를 뽑아오기 위해 아래의 방법을 사용했다.

  ```python
  datetime(2019,7,19) - timedelta(weeks=i) # i주 이전의 시각을 구함.
  targetDt.strftime('%Y%m%d') # 20190713형식으로 해줌.
  ```

- 완성된 코드

```python
import requests
import csv
from decouple import config
from datetime import datetime, timedelta
from pprint import pprint 
# datetime(2019,7,19) - timedelta(weeks=i) # i주 이전의 시각을 구함.
# targetDt.strftime('%Y%m%d') => 20190713형식으로 해줌.

# -----------------------------------------------------------------------------

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

    # 필요한 정보 : 영화 대표코드 / 영화명 / 누적관객수

    # 영화정보가 담긴 딕셔너리에서 영화 대표 코드를 추출
    for movie in movies:
        code = movie.get('movieCd') # 키 안에 딕셔너리 만들기
        # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어가 있다면,
        # 그게 가장 마지막 주 데이터다. 즉 기존 영화코드가 있다면 딕셔너리에 넣지 않는다.
        if code not in result: # result안에 없다면 추가
            result[code] = {
                '영화 대표코드': movie.get('movieCd'),
                '영화명': movie.get('movieNm'),
                '해당일 누적관객수': movie.get('audiAcc')
            }

with open('boxOffice.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('영화 대표코드', '영화명', '해당일 누적관객수')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        print(value)
        writer.writerow(value)

```

- boxOffice.csv

  - csv파일에는 50주간 데이터 중에 주간 박스오피스 TOP10 데이터가 저장되어있다.
  - 영화별로 영화 대표코드, 영화명, 해당일 누적관객수가 기록되어 있고 누적관객수는 가장 최신정보를 반영했다.

  

- 실패한 코드

  ```python
  key = config('KEY')
  targetDt='20190713'
  
  res =requests.get(f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?&key={key}&targetDt={targetDt}&weekGb=0') #회차정보 받아서 요청보냄
  movies = res.json()
  
  list_movies = movies['boxOfficeResult']['weeklyBoxOfficeList']
  movies_boxoffice=[]
  
  
  for i in range(0,len(list_movies)): 
      if list_movies[i] not in movies_boxoffice:
          movies_boxoffice.append(list_movies[i])
  print(movies_boxoffice)
  
  movieNm = []
  movieCd = []
  audiAcc = []
  for i in range(0,len(movies_boxoffice)):
      movieNm.append(movies_boxoffice[i].get('movieNm'))
      movieNm.append(movies_boxoffice[i].get('movieCd'))
      movieNm.append(movies_boxoffice[i].get('audiAcc'))
  
  ```

  - movieNm, movieCd, audiAcc를 각각 리스트로 저장했지만 이를 한번에 딕셔너리 형태로 저장하는 과정을 마무리 하지 못했다.
  
  

## 3. `02.py`

### 1) 영화진흥위원회 오픈 API(영화 상세정보)

- 위에서 수집한 영화 대표코드를 활용하여 상세 정보를 수집한다.

- 먼저, `boxOffice.csv`에서 영화 코드를 읽어와 `movie_Cd`라는 리스트에 저장한다.
- for문을 돌면서 `movie_Cd`를 하나씩 가져와 `movies_info`에 영화의 상세정보를 저장한다.



- 완성된 코드

```python
import csv
import requests
from decouple import config
from pprint import pprint

# 1 csv.DictReader() _ boxoffice에서 영화코드 읽어오기
with open('boxoffice.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f) # 읽어올 파일만 입력=>reader에 파일이 들어있음
    # 한 줄씩 읽는다.
    movie_Cd=[]
    for row in reader:
        movie_Cd.append(row['영화 대표코드'])
#pprint(movie_Cd)

result={}
for code in movie_Cd:
    key = config('KEY')
    movieCd = code

    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json?key={key}&movieCd={movieCd}'
    api_data = requests.get(url).json() # 크롬에서 보이는 것과 같은 모습으로 표현해줌

    movies_info = api_data.get('movieInfoResult').get('movieInfo')
    
# 필요정보 : movieCd, movieNm, movieNmE, movieNmOg, watchGradeNm, openDt, showTm, genreNm, directors


    for info in movies_info:
        code = movies_info.get('movieCd')

        result[code] = {
                    '영화 대표코드': movies_info.get('movieCd'),
                    '영화명(국문)': movies_info.get('movieNm'),
                    '영화명(영문)': movies_info.get('movieNmEn'),
                    '영화명(원문)': movies_info.get('movieNmOg'),
                    '관람등급': movies_info.get('audits')[0].get('watchGradeNm') if movies_info.get('audits') else None,
                    '개봉연도': movies_info.get('openDt'),
                    '상영시간': movies_info.get('showTm'),
                    '장르': movies_info.get('genres')[0].get('genreNm'),
                    '감독명': movies_info.get('directors')[0].get('peopleNm') if movies_info.get('directors') else None
            }
# 조건표현식을 사용하여 if안의 내용이 true이면 왼쪽을 false이면 오른쪽을 실행하도록 했다.


with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('영화 대표코드', '영화명(국문)', '영화명(영문)', '영화명(원문)', '관람등급', '개봉연도', '상영시간', '장르', '감독명')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        print(value)
        writer.writerow(value)

```

- `movie.csv`

  - csv파일에는 영화별 상세정보가 저장되어있다.

  - 영화별로 '영화 대표코드', '영화명(국문)', '영화명(영문)', '영화명(원문)', '관람등급', '개봉연도', '상영시간', '장르', '감독명'가 기록되어 있다.

    

- 실패한 코드

  ```python
  
  for info in movies_info:
          code = movie.get('movieCd') # 키 안에 딕셔너리 만들기
          # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어가 있다면,
          # 그게 가장 마지막 주 데이터다. 즉 기존 영화코드가 있다면 딕셔너리에 넣지 않는다.
          if Null not in movies_info.values(): # result안에 없다면 추가
              result[code] = {
                  'movieCd': movie.get('movieCd'),
                  'movieNm': movie.get('movieNm'),
                  'movieNmEn': movie.get('movieNmEn'),
                  'movieNmOg': movie.get('movieNmOg'),
                  'watchGradeNm': movie.get('audits')[0].get('watchGradeNm'),
                  'openDt': movie.get('openDt'),
                  'showTm': movie.get('showTm'),
                  'genreNm': movie.get('genres')[0].get('genreNm'),
                  'directors': movie.get('directors')[0].get('peopleNm')
              }
  ```

- `watchGradeNm`와 `directors`에서 None이 있을 경우 None값을 저장하는 if문을 작성하려 했으나 하지 못했다.

  

## 4. `03.py`

### 1) 영화진흥위원회 오픈 API(영화인 정보)

- 위에서 수집한 영화 감독정보를 활용하여 상세 정보를 수집한다.

- 먼저, `movie.csv`에서 감독명과 영화명을 읽어와 `people_Nm`에 (감독명, 영화명) 튜플형식으로 한 줄씩 읽어온다.
- for문을 돌면서 `people_Nm`을 하나씩 가져와 `directors_info`에 감독의 상세정보를 저장한다.



- 완성된 코드

```python
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
        url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key={key}&peopleNm={people_Nm[0]}' # people_Nm[0] : 감독명이 저장되어 있음.
        api_data = requests.get(url).json() # 크롬에서 보이는 것과 같은 모습으로 표현해줌

        directors_info = api_data.get('peopleListResult').get('peopleList')
        for info in directors_info:
            code = info.get('peopleCd')
            if people_Nm[0] == info.get('peopleNm') and people_Nm[1] in info.get('filmoNames'):
                
# people_Nm[0] : 감독명이 info의 이름과 같고, people_Nm[1] : 영화명이 info에 있는 경우만 result	에 저장.   
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

```

- `director.csv`
  - csv파일에는 영화감독에 대한 상세정보가 저장되어있다.
  - 감독별로 '영화인 코드', '영화인명', '분야', '필모리스트'가 기록되어 있다.