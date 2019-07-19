avengers = [
    {
        "name": "tony stark",
        "gender": "male",
        "appearances": 3068,
        "years since joining": 52
    },
    {
        "name": "robert bruce banner",
        "gender": "male",
        "appearances": 2089,
        "years since joining": 52
    },
    {
        "name": "thor odinson",
        "gender": "male",
        "appearances": 2402,
        "years since joining": 52
    },
    {
        "name": "steven rogers",
        "gender": "male",
        "appearances": 3458,
        "years since joining": 51
    }
]

# 1. csv.DictWriter()
import csv
# with open('avengers.csv', 'w', newline='', encoding='utf-8') as f: # with 쓰면 close 쓸 필요 없음
#     # 저장할 데이터들의 필드 이름을 미리 정한다.
#     fieldnames = ('name', 'gender', 'appearances', 'years since joining')
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     # 필드 이름을 csv 파일 최상단에 작성한다.
#     writer.writeheader()

#     # 딕셔너리를 순회하며 key를 통해 한 줄씩(value를) 작성한다.
#     for avenger in avengers: # 리스트 안에 있는 딕셔너리를 갖는다.
#         writer.writerow(avenger)


# 2 csv.DictReader()
with open('avengers.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f) # 읽어올 파일만 입력=>reader에 파일이 들어있음

    # 한 줄씩 읽는다.
    for row in reader:
        # print(row)
        # print(row)
        print(row['name'])
        print(row['gender'])
        print(row['appearances'])
        print(row['years since joining'])

# decouple로 api 키 지우기!!

# targetDt 50번 반복! -> top10만 수집
# 일단 for문 없이 첫 주를 뽑는다.->for문 이용 3주 뽑아보기 -> ....-> 단계적으로 해서 50주 뽑기

# 각 영화별 최종 누적관객 수 = 
