from bs4 import BeautifulSoup
import requests, re
import socket, codecs, time, re
from toolbox import dict_sort, banolim
from datetime import date, timedelta, datetime


def background_magam():

    with open('C:/stamp/sihwang.csv', 'r') as f:
        datas = f.readlines()[0].split(',')

    def str_to_plma(x):
        if x=='True':
            x=True
        elif x== 'False':
            x=False
        return x
    kospi_data ={}
    kosdaq_data ={}
    exch_data ={}
    d={}

    state, now,kospi_data['num'],kospi_data['point'],kospi_data['rate'], kospi_data['plma'], kospi_data[
        'plma_ment'], \
    kosdaq_data['num'], kosdaq_data['point'], kosdaq_data['rate'],kosdaq_data['plma'],kosdaq_data['plma_ment']=datas
    kospi_data['plma'] = str_to_plma(kospi_data['plma'])
    kosdaq_data['plma'] = str_to_plma(kosdaq_data['plma'])
    # exch_data['plma'] = str_to_plma(exch_data['plma'])


    d['kospi']=kospi_data
    d['kosdaq'] = kosdaq_data
    d['원/달러'] = exch_data

    kospi_ment=f"""이날 코스피 지수는 전일 대비 {d['kospi']['point']}({d['kospi']['rate']}%) {d['kospi']['plma_ment']} """\
f"""{d['kospi']['num']}로 거래를 마쳤다."""
    kosdaq_ment=f"""코스닥 지수는 전일 대비 {d['kosdaq']['point']}({d['kosdaq']['rate']}%) {d['kosdaq']['plma_ment']} {d['kosdaq']['num']}로 마감했다."""

    exch_ment=f"""달러/원 환율은 {d['원/달러']['point']}원 오른 {d['원/달러']['num']}원으로 마감했다."""
    return {'kospi_ment':kospi_ment, 'kospi_plma':d['kospi']['plma'], 'kosdaq_ment':kosdaq_ment, 'kosdaq_plma':d[
        'kosdaq']['plma'], 'exch_ment':exch_ment}
print(background_magam())