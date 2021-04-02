###코스닥 풀었다 #######

from bs4 import BeautifulSoup
import requests, re
import socket, codecs, time, re
from toolbox import dict_sort, banolim
from datetime import date, timedelta, datetime

def upjong_kosdaq(plma_g):
    # try:

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    dics = {103:{'name':'기타서비스'}, 104:{'name':'IT'} ,106:{'name':'제조'} \
    ,107 :{'name':'건설'}, 108 :{'name':'유통'}, 110:{'name':'운송'}, 111:{'name':'금융'}, 112:{'name':'통신방송서비스'}\
        ,115:{'name':'음식료/담배'}, 116:{'name':'섬유/의류'}, 117:{'name':'종이/목재'}, 118:{'name':'출판'}\
        , 119:{'name':'화학'}, 120:{'name':'제약'},121 :{'name':'비금속'}, 122:{'name':'금속'}\
        , 123 :{'name':'기계/장비'}, 124:{'name':'일반전기전자'}, 125:{'name':'의료/정밀기기'}, 126:{'name':'운송장비/부품'}\
    , 127 :{'name':'기타 제조'}, 128:{'name':'통신서비스'}, 129:{'name':'방송서비스'}, 130:{'name':'인터넷'},\
            131:{'name':'디지털컨텐츠'}, 132:{'name':'소프트웨어'}, 133:{'name':'컴퓨터서비스'},134:{'name':'통신장비'}, \
    135:{'name':'정보기기'},136:{'name':'반도체'},137:{'name':'IT부품'},141:{'name':'오락,문화'}}

    cd_socket_list = []
    for i in [*dics]:
        ii = str(i)
        dics[i]['cd_in_socket'] = f'3{ii[0]}3{ii[1]}3{ii[2]}'

    ###0213 화면. 업종 하나씩 보내서 함. 여기는 업종번호 106에 보냄. 가운데 313036  이 그것. 그 번호만 바꾸면 됨.

    ip = '211.115.74.81'

    clientSocket.connect((ip, 14811))
    for ii in [*dics]:
        a=f'fefd4d54000000303031323654000200390155504a4f4e470000000000000000000030323133202'\
          f'0303231333030000043333373756863726174653030303030303030303030303031343' \
          f'3303231353435303633353120200000000000000000000000000000000030303032393' \
          f'93030317f{dics[ii]["cd_in_socket"]}1e393030387f3130311e31301f32351f31' \
                                                '311f3132'
        a= codecs.decode(a, 'hex')
        clientSocket.send(a)
        skip = False
        line =''
        data = clientSocket.recv(1024)
        data = data.hex()
        han = False
        for i in range(len(data)//2):
            if skip:
                skip = False
                pass
            else:
                if han:
                    han = False
                else:
                    try:
                        ps =data[i*2:i*2+2]
                        if ps == '1f':
                            # print('|',end='')
                            line +='|'
                        else:
                            # print(codecs.decode(ps,'hex').decode('cp949')  ,end='')
                            line += codecs.decode(ps,'hex').decode('utf-8')

                    except:
                        line += '.'
        # print(line.split('|')[3])
        dics[ii]["rate"] =line.split('|')[3]
        time.sleep(0.3)
    # print(dics)


    plus_num =0
    minus_num = 0
    for i in dics:
        rate = dics[i]['rate']
        rate = float(rate.replace('+',''))
        if rate >0 :
            plus_num +=1
        elif rate <0:
            minus_num +=1
        dics[i]['rate'] = rate

    dics = dict_sort(dics,'rate')

    if plus_num <5:
        minus_num = 10 - plus_num
    elif minus_num <5:
        plus_num = 10 - minus_num
    else:
        plus_num, minus_num = 5,5

    plus = [*dics][:plus_num]
    minus = [*dics][-minus_num:][::-1]

    def ment_maker(plma_list):
        ment_temp = ''
        for i in plma_list:
            ment_temp += f"""{dics[i]['name']}({dics[i]['rate']}%), """
        ment_temp = ment_temp[:-2]
        return ment_temp

    plus_ment = ment_maker(plus)
    minus_ment = ment_maker(minus)

    ment =''
    if plma_g == True:
        ment = f"""업종별로 상승한 업종은 {plus_ment} 등이다. 하락한 업종은 {minus_ment} 등이다."""
    elif plma_g == False:
        ment = f"""업종별로 하락한 업종은 {minus_ment} 등이다. 상승한 업종은 {plus_ment} 등이다. """

    return (ment)
if __name__ == "__main__":
    print(upjong_kosdaq(True))