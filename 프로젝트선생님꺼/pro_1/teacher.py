import csv
import requests, json
from datetime import datetime, timedelta
from decouple import config
from pprint import pprint

result = {}
for i in range(1): 
    key = config('SH_KEY') 
    targetDt = datetime(2019, 7, 13) - timedelta(weeks=i)
    targetDt = targetDt.strftime('%Y%m%d')

    url = f'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json?weekGb=0&key={key}&targetDt={targetDt}'
    api_data = requests.get(url).json()
    # pprint(api_data)


    #주간/주말 박스오피스 데이터 리스트 가져오기. 
    movies = api_data.get('boxOfficeResult').get('weeklyBoxOfficeList')
    # pprint(movies)

    # 영화 정보가 담긴 딕셔너리에서 영화 대표 코드를 추출
    for movie in movies:
        code = movie.get('movieCd')
    # 날짜를 거꾸로 돌아가면서 데이터를 얻기 때문에, 기존에 이미 영화코드가 들어가 있다면,
    # 그게 가장 마지막 주 데이터다. 즉 기존 영화 코드가 있다면 딕셔너리에 넣지 않는다. 
        if code not in result:
            result[code] = {
                'movieCd' : movie.get('movieCd'),
                'movieNm' : movie.get('movieNm'),
                'audiAcc' : movie.get('audiAcc')
            }
    # pprint(result)

with open ('boxoffice.csv', 'w', encoding='utf-8', newline='') as f:
    fieldnames = ('movieCd', 'movieNm', 'audiAcc')
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for value in result.values():
        print(value)
        writer.writerow(value)