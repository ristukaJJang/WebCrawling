# 개요 : 종목코드(1,3), 업종(2,1), 기업구분(3,3)  ,매출액(7,1), 순이익(8,1), 자본금(8,3)
# 정보 : 주관사(=주간사), 희망공모가액, 확정공모가,청약경쟁률
# 일정 : 그룹별 배정 [그룹 , 주] , 환불일, 공모청약일, 배정공고일, 환불일,

# Company(기업명, 업종, 기업구분, 매출액, 순이익, 자본금)
# IPO(종목코드, 종목명, 확정공모가, 청약경쟁률, 주관사, 그룹별배정 ) +희망공모가 도있으면 좋을듯
# Schedule(종목명, 청약일, 배정공고일, 환불일, 상장일)
# 주가(종목명, 현재가, 전일비, 공모가대비 등락률, 시초가, 첫날종가 )

import requests
from bs4 import BeautifulSoup
import json
import re

#print(ssl.OPENSSL_VERSION)


companies_ipo = {}
ipo_summery = {}

def get_comp_list(page=1):
    total_data = []
    for p in range(1, page + 1):
        fullUrl = 'http://www.38.co.kr/html/fund/index.htm?o=nw&page=%s' % p
        response = requests.get(fullUrl, headers={'User-Agent': 'Mozilla/5.0'})
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        data = soup.find('table', {'summary': '신규상장종목'})
        data = data.find_all('tr')[2:]
        total_data = total_data + data

    filtered_datas = {}

    for row in range(0, len(total_data)):
        comp_id = total_data[row].find('a', href=True)['href']
        comp_id = re.sub(r'\D', '', comp_id)
        number = get_detail_info(comp_id)
        if number == 0:
            return 0
        data_list = total_data[row].text.replace('\xa0', '').replace('\t\t', '').split('\n')[1:-1]

        if len(data_list) < 9:
            continue
        filter_data={}
        filter_data["기업명"] = data_list[0].replace('(유가)', '').strip()
        filter_data["신규상장일"] = data_list[1].strip()
        filter_data["현재가(원)"] = data_list[2].strip()
        filter_data["전일비(%)"] = data_list[3].strip()
        filter_data["공모가대비등락률(%)"] = data_list[5].strip()
        filter_data["시초가(원)"] = data_list[6].strip()
        filter_data["첫날종가(원)"] = data_list[8].strip()
        # print(filter_data)
        filtered_datas[row] = filter_data
    # 첫페이지 : 종목명(=기업명) ,신규상장일(=상장일) ,현재가 ,전일비 ,시초가, 공모가대비등락률,첫날종가

    return filtered_datas


# https://www.38.co.kr/html/fund/?o=v&no=2044&l=
def get_detail_info(no):

    fullUrl = 'https://www.38.co.kr/html/fund/?o=v&no=%s' % no
    print(fullUrl)

    try:
        response = requests.get(fullUrl,headers={
            'Content-Type':'text/html;charset=euc-kr',
            'User-Agent': 'Mozilla/5.0'
        })
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        filtered_datas = {}
        ipo_summery = {}  # 각 기업에 대한 기업 개요 정보를 저장할 딕셔너리를 초기화합니다.

        complex_summary_table = soup.find('table', {'summary': '공모정보'})
        if complex_summary_table:
            complex_summary_data = complex_summary_table.find_all('tr')

        for row in complex_summary_data:
            data_list = row.text.replace('\xa0', '').replace('\t\t', '').split('\n')[1:-1]
            #print(data_list)

            ipo_summery[data_list[0]] = data_list[1]
            try:
                ipo_summery[data_list[2]] = data_list[3]
            except IndexError:
                continue

            if ' 신영스팩9호 ' in data_list:
                print("2022년 자료입니다.")
                return 0


        companies_ipo[no] = ipo_summery
        print(companies_ipo)
        print("\n")




        # for row in range(0, len(complex_summary_data)):
        #     data_list = complex_summary_data[row].text.replace('\xa0', '').replace('\t\t', '').split('\n')[1:-1]



        # ipo_info_data = soup.find('table', {'summary': '공모정보'}).find_all.find_all('tr')
        # ipo_schedule_data = soup.find('table', {'summary': '공모청약일정'})



    except Exception as e:
        print(e)

if __name__ == '__main__':
    filtered_datas = get_comp_list(8)
    # get_detail_info("1961")
    with open('test.json', 'w') as f:
        json.dump(filtered_datas, f,ensure_ascii=False, indent=4)