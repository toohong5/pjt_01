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
    
    # movieCd, movieNm, movieNmE, movieNmOg, watchGradeNm, openDt, showTm, genreNm, directors


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



with open('movie.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('영화 대표코드', '영화명(국문)', '영화명(영문)', '영화명(원문)', '관람등급', '개봉연도', '상영시간', '장르', '감독명')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        print(value)
        writer.writerow(value)


# for info in movies_info:
#         code = movie.get('movieCd') # 키 안에 딕셔너리 만들기
#         # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어가 있다면,
#         # 그게 가장 마지막 주 데이터다. 즉 기존 영화코드가 있다면 딕셔너리에 넣지 않는다.
#         if Null not in movies_info.values(): # result안에 없다면 추가
#             result[code] = {
#                 'movieCd': movie.get('movieCd'),
#                 'movieNm': movie.get('movieNm'),
#                 'movieNmEn': movie.get('movieNmEn'),
#                 'movieNmOg': movie.get('movieNmOg'),
#                 'watchGradeNm': movie.get('audits')[0].get('watchGradeNm'),
#                 'openDt': movie.get('openDt'),
#                 'showTm': movie.get('showTm'),
#                 'genreNm': movie.get('genres')[0].get('genreNm'),
#                 'directors': movie.get('directors')[0].get('peopleNm')
#             }
        
#     pprint(result)