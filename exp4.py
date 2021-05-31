from bs4 import BeautifulSoup
import requests, re
import socket, codecs, time, re
from toolbox import dict_sort, banolim
from datetime import date, timedelta, datetime

url = 'https://finance.naver.com/sise/sise_index.nhn?code=KOSPI'
req = requests.post(url)
be_0 = BeautifulSoup(req.text, 'html.parser')
print(be_0)


#영웅문 시작페이지에서 코스피, 코스닥 기본값 멘트와 plma 가져옴
def background(be_0 = 'None'):
    if be_0 =='None':
        url = 'https://www.kiwoom.com/nkw.HeroFrontJisu3.do'
        req = requests.post(url)
        be_0 = BeautifulSoup(req.text, 'html.parser')
        # print(be_0)

    be = be_0.find_all('li')
    jisu_dict_s= {}
    for i in be:
        plma = None
        jisu_dict = {}
        jisu = i.get_text(separator='|').split('|')

        #이름 구간
        name = jisu[0].replace(' ','')
        jisu_dict['name'] = name

        #지수구간
        num_0 = jisu[1]
        if bool(re.search('▲',num_0)):
            plma = True
            plma_ment ='오른'
            num= num_0.replace(',','').replace('▲','').replace(' ','')

        elif bool(re.search('▼', num_0)):
            plma = False
            plma_ment = '내린'
            num= num_0.replace(',','').replace('▼','').replace(' ','')
        jisu_dict['num'] = num
        jisu_dict['plma'] = plma
        jisu_dict['plma_ment'] = plma_ment

        #포인트 구간
        point = jisu[2].replace(' ','')
        jisu_dict['point'] = point
        # print(jisu)

        #증감율 구간
        try:
            rate = jisu[3].replace('%','').replace(' ','')
        except:
            rate='0'
        jisu_dict['rate'] = rate

        name = name.lower()
        jisu_dict_s[name] =jisu_dict

    d = jisu_dict_s
    # print(d)
    h = datetime.now().hour
    ampm= '오전'
    if h<=12:
        ampm= '오전'
    else:
        ampm = '오후'
        h = h-12
    now = f"{h}시 {datetime.now().minute}분"
    kospi_ment=f"""이날 {ampm} {now} 기준 코스피 지수는 전일 대비 {d['kospi']['point']}포인트(p)(\
{d['kospi']['rate']}%){d['kospi']['plma_ment']} {d['kospi']['num']}로 거래되고 있다."""
    # print(kospi_ment)
    kosdaq_ment=f"""코스닥 지수는 전일 대비 {d['kosdaq']['point']}p({d['kosdaq']['rate']}%)\
{d['kosdaq']['plma_ment']} {d['kosdaq']['num']}로 거래되고 있다."""
    # print(kosdaq_ment)

    exch_ment=f"""서울외환시장에서 달러/원 환율은 {d['원/달러']['point']}원 {d['원/달러']['plma_ment']} {d['원/달러']['num']}원으로 거래되고 있다."""

    return {'kospi_ment':kospi_ment, 'kospi_plma':d['kospi']['plma'], 'kosdaq_ment':kosdaq_ment, 'kosdaq_plma':d['kosdaq']['plma'], 'exch_ment':exch_ment}