import csv
import requests
from decouple import config
from pprint import pprint

# 1 csv.DictReader()
with open('movie.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f) # 읽어올 파일만 입력=>reader에 파일이 들어있음
    # 한 줄씩 읽는다.
    people_Cd=[]
    for row in reader:
        movie_Cd.append(row['peopleCd'])