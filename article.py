from bs4 import BeautifulSoup
import requests, re
import socket, codecs, time, re
from toolbox import dict_sort, banolim
from datetime import date, timedelta, datetime

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


        #증감율 구간
        rate = jisu[3].replace('%','').replace(' ','')
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
    kospi_ment=f"""이날 {ampm} {now} 기준 코스피 지수는 전일 대비 {d['kospi']['point']}({d['kospi']['rate']}%)
{d['kospi']['plma_ment']} {d['kospi']['num']}로 거래되고 있다."""
    # print(kospi_ment)
    kosdaq_ment=f"""코스닥 지수는 전일 대비 {d['kosdaq']['point']}({d['kosdaq']['rate']}%) {d['kosdaq']['plma_ment']} {d['kosdaq']['num']}로 거래되고 있다."""
    # print(kosdaq_ment)

    exch_ment=f"""달러/원 환율은 {d['원/달러']['point']}원 오른 {d['원/달러']['num']}원으로 거래되고 있다."""

    return {'kospi_ment':kospi_ment, 'kospi_plma':d['kospi']['plma'], 'kosdaq_ment':kosdaq_ment, 'kosdaq_plma':d[
        'kosdaq']['plma'], 'exch_ment':exch_ment}



#코스피, 코스닥 시가총액 10위 종목별
def kos_sentences(kos, plma_g):
    if kos=='kospi':
        url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0'
        kos_han ='코스피'
    if kos=='kosdaq':
        url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=1'
        kos_han ='코스닥'
    temp = requests.get(url)
    temp = BeautifulSoup(temp.text, 'html.parser')
    nos = temp.find_all('td', {'class':'no'})
    lists = []
    dicts = {}
    for i in nos[:10]:
        tr = i.find_parent('tr')
        # print(tr.find('a',{'class':'tltle'}).text)
        num = i.text
        dicts[num]={}
        dicts[num]['name']= tr.find('a',{'class':'tltle'}).text

        nums = tr.find_all('td', {'class':'number'})
        nums_list = []
        for ii in nums:
            nums_list.append(ii.text.replace('\n','').replace('\t',''))
        rate = nums_list[2]
        plma = ''
        plma_sign = ''
        if bool(re.search('\+', rate)):
            plma = True
            plma_sign = ''
        elif bool(re.search('\-', rate)):
            plma = False
            plma_sign = '-'
        rate = re.sub(r'[\+\-%]','', rate)
        dicts[num]['rate'] = rate
        dicts[num]['plma'] = plma
        dicts[num]['plma_sign'] = plma_sign

    plus={}
    minus={}
    for i in dicts:
        temp = dicts[i]
        if temp['plma']:
            plus[temp['name']]=temp
        elif temp['plma'] == False:  #rate '0'인건 빠짐.  걍 'not'으로 하면 값이''인것도 포함됨.
            minus[temp['name']]=temp


    #증가는 plus,  감소는 minus
    state = ''
    if len([*plus])==0:
        state = "only_minus"
    elif len([*minus])==0:
        state = "only_plus"
    else:
        state = "both"
    # print(plus)
    # print(minus)

    # print(minus.items())
    ####딕셔너리 정렬해서 문장 만들기 ####
    def plma_sent(dict, only=False):
        if dict == minus:
            plma0 = '하락'
        elif dict == plus:
            plma0 = '상승'
        dict = {k:v for k, v in sorted(dict.items(), reverse=True, key=lambda item: item[1]['rate'])}
        ##멘트제조###
        ment = ""

        if only:
            only_word ='이'
        else:
            only_word = '은'
        for i in dict:
            ment += f"{dict[i]['name']}({dict[i]['plma_sign']}{dict[i]['rate']}%), "
        ment = ment[:-2]+f" 등{only_word} {plma0}했다."
        return ment
    # plma_sent(minus)
    # plma_sent(plus)

    kos = '코스피'

    if state == 'only_minus':
        result = f"{kos_han} 시가총액 상위 10개 종목 중 {plma_sent(minus, only=True)}"
    elif state == 'only_plus':
        result = f"{kos_han} 시가총액 상위 10개 종목 중 {plma_sent(plus, only=True)}"
    elif state == 'both':
        if plma_g:
            result = f"{kos_han} 시가총액 상위 10개 종목 중 {plma_sent(plus)} {plma_sent(minus)}"
        else:
            result= f"{kos_han} 시가총액 상위 10개 종목 중 {plma_sent(minus)} {plma_sent(plus)}"
    return result



#코스피, 코스닥 투자자별
def kos_toojaja(kos, plma_glob):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ##화면번호 211
    if kos=='kospi':
        a='fefd4d540000003030333333540002004f0153544f434b47000030303030323330313037383220203037383230300000433333737568637261746530303030303030303030303030343630313931313430353039323120200000000000000000000000000000000030303233362430303030303032333031303230302020202020202020202020202020202030402020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020203030313137393030317f5430303130387f5430303130397f5430303131347f5430303130317f5430303130327f5430303130337f5430303130357f5430303130347f5430303130367f5430303131337f5430303131327f5430303130371f393030311f3230341f3230381f3231321f3230321f3230361f323130' #4번
    elif kos=='kosdaq':
        a='fefd4d540000003030333333540002004f0153544f434b47000030303030323330313037383220203037383230300000433333737568637261746530303030303030303030303030353937313931323435353538363720200000000000000000000000000000000030303233362430303030303032333031303230302020202020202020202020202020202030402020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020203030313137393030317f5431303130387f5431303130397f5431303131347f5431303130317f5431303130327f5431303130337f5431303130357f5431303130347f5431303130367f5431303131337f5431303131327f5431303130371f393030311f3230341f3230381f3231321f3230321f3230361f323130'

    ip = '211.115.74.81'

    a= codecs.decode(a, 'hex')
    clientSocket.connect((ip, 14811))
    line_bf = ''
    tik_dick= {}
    # while True:
    clientSocket.send(a)
    data = clientSocket.recv(1024)
    # print(data.hex())
    data = data.hex()

    # print(codecs.decode(data, 'hex').decode('cp949'))
    line = []
    han = False
    line = ''
    han = False
    for i in range(len(data)//2):
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
                    line += codecs.decode(ps,'hex').decode('cp949')
            except:
                # print('.',end='')
                line += '.'
                # try:
                #     print(codecs.decode(data[i*2:i*2+4],'hex').decode('cp949')  ,end='')
                #     han = True
                # except:
                #     print('.', end='')
    line= line[line.index('MT'):]
    line= re.sub('.*                              ','',line)
    # # line= re.sub('.*\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02\x02','',line)
    line = line[5:]
    line = line.split(sep='\n')
    dicts={}
    for i in line:
        temp = i.split('|')
        dicts[temp[0]]=temp

    dicts_word={}
    if kos=='kospi':
        names = {'T00108':'개인', 'T00109':'외국인', 'T00114':'기관'}
    if kos=='kosdaq':
        names = {'T10108':'개인', 'T10109':'외국인', 'T10114':'기관'}

    for i in names:
        dicts_word[names[i]] ={}

        if int(dicts[i][3]) >0:
            dicts_word[names[i]]['plma'] = True
            dicts_word[names[i]]['plma_ment'] = '순매수'
        elif int(dicts[i][3]) <0:
            dicts_word[names[i]]['plma'] = False
            dicts_word[names[i]]['plma_ment'] = '순매도'
        elif int(dicts[i][3]) ==0:
            dicts_word[names[i]]['plma'] = '보합'
            dicts_word[names[i]]['plma_ment'] = '보합'
        dicts_word[names[i]]['num'] =dicts[i][3].replace('-','')



    if plma_glob:
        plma_glob_ment = '순매수'
    else:
        plma_glob_ment = '순매도'


    first={}
    second={}
    third={}
    for i in dicts_word:
        if dicts_word[i]['plma']==plma_glob:
            first[i]=dicts_word[i]
        elif len([*second])==0:
            second[i]=dicts_word[i]
        else:
            if dicts_word[i]['plma'] == second[[*second][0]]['plma']:
                second[i]=dicts_word[i]
            else:
                third[i]=dicts_word[i]


    ment = ''

    def menter(dict0):
        ment0 = ''

        if len([*dict0])>1:
            gak='각각 '
        else:
            gak=''
        for i in [*dict0]:
            ment0 += f"{i}은 {banolim(dict0[i]['num'].replace('-',''),'억','억')}원, "
        ment0 = ment0[:-2] + f" {gak}{dict0[i]['plma_ment']}했다. "
        return ment0


    if len([*second])==0:
        first = dict_sort(first,'num')
        ment = menter(first)
    elif len([*third])==0:
        if len([*first])==0: #second밖에 없음
            second = dict_sort(second,'num')
            ment = menter(second)
        else:
            first = dict_sort(first,'num')
            second = dict_sort(second,'num')
            ment = menter(first)+menter(second)
    elif len([*third])!=0:
        ment = menter(first)+menter(second)+menter(third)


    # print(dicts_word)
    return ment

if __name__ == '__main__':
    # print(kos_sentences('kospi',True))
    # print(background())
    print(kos_toojaja('kospi',True))

#코스피, 코스닥 메인 숫자
#거기서 나온 plma 넘기기

#업종별

#환율