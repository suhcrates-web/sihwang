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


#마감 기본문
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

    state, now,kospi_data['num'],kospi_data['point'],kospi_data['rate'], kospi_data['plma'], kospi_data['plma_ment'], \
    kosdaq_data['num'], kosdaq_data['point'], kosdaq_data['rate'],kosdaq_data['plma'],kosdaq_data['plma_ment'],\
    exch_data['num'], exch_data['point'], exch_data['plma'], exch_data['plma_ment']\
        =datas
    kospi_data['plma'] = str_to_plma(kospi_data['plma'])
    kosdaq_data['plma'] = str_to_plma(kosdaq_data['plma'])
    exch_data['plma'] = str_to_plma(exch_data['plma'])


    d['kospi']=kospi_data
    d['kosdaq'] = kosdaq_data
    d['원/달러'] = exch_data

    kospi_ment=f"""이날 코스피 지수는 전일 대비 {d['kospi']['point']}포인트(p)({d['kospi']['rate']}%) {d['kospi']['plma_ment']} """ \
               f"""{d['kospi']['num']}로 거래를 마쳤다."""
    kosdaq_ment=f"""코스닥 지수는 전일 대비 {d['kosdaq']['point']}p({d['kosdaq']['rate']}%) {d['kosdaq']['plma_ment']}\
{d['kosdaq']['num']}로 마감했다."""

    exch_ment=f"""서울외환시장에서 달러/원 환율은 {d['원/달러']['point']}원 {d['원/달러']['plma_ment']} {d['원/달러']['num']}원으로 마감했다."""
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


#코스피 업종별
def upjong_maker(kos, plma_g):
    try:

        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ##화면번호 211
        if kos=='kospi':
            a='fefd4d540000003030323531540002004e0153544f434b4700003030303032303137303231382020303231383030000043333373756863726174653030303030303030303030303031353833303133343430313236312020000000000000000000000000000000003030313534393030387f3030311e2430303030303032303137303035302020202020202020202020202020202030402020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020203030303236393030311f3330321f31301f32351f31311f31321f31331f3134'

        if kos == 'kosdaq':
            a = 'fefd4d540000003030323531540002004e0153544f434b4700003030303032303137303231382020303231383030000043333373756863726174653030303030303030303030303033333533303135303535323730322020000000000000000000000000000000003030313534393030387f3130311e2430303030303032303137303035302020202020202020202020202020202030402020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020203030303236393030311f3330321f31301f32351f31311f31321f31331f3134'

        ip = '211.115.74.81'

        a= codecs.decode(a, 'hex')
        clientSocket.connect((ip, 14811))
        line_bf = ''
        tik_dick= {}
        # while True:
        clientSocket.send(a)
        test =True
        skip = False
        data = clientSocket.recv(1024)
        time.sleep(3)
        data += clientSocket.recv(1024)

        data = data.hex()
        # print(data)
        # print(codecs.decode(data, 'hex').decode('cp949'))
        line = []
        han = False
        line = ''
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
                        try:
                            ps=data[i*2:i*2+4]
                            line += codecs.decode(ps,'hex').decode('cp949')
                            skip = True

                        # print('.',end='')
                        except:
                            line += '.'
                        # try:
                        #     print(codecs.decode(data[i*2:i*2+4],'hex').decode('cp949')  ,end='')
                        #     han = True
                        # except:
                        #     print('.', end='')
        # print(line)
        line= line[line.index('MT'):]
        line= re.sub('.*                              ','',line)
        line = line[5:]
        line = line.split(sep='\n')
        # print(line)
        dicts={}
        plus_num =0
        minus_num = 0
        for i in line:
            temp = i.split('|')
            if temp[1] in ['코스피배당성장50','코스피고배당50','종합(KOSPI)', '변동성지수']:
                pass
            else:
                rate = float(temp[5].replace('+',''))
                if rate >0 :
                    plus_num +=1
                elif rate <0:
                    minus_num +=1
                dicts[temp[1]]={'rate':rate}
        # print(dicts)

        dicts = dict_sort(dicts,'rate')
        # print(dicts)

        if plus_num <5:
            minus_num = 10 - plus_num
        elif minus_num <5:
            plus_num = 10 - minus_num
        else:
            plus_num, minus_num = 5,5

        plus = [*dicts][:plus_num]
        minus = [*dicts][-minus_num:][::-1]
        # print(plus)
        # print(minus)



        def ment_maker(plma_list):
            ment_temp = ''
            for i in plma_list:
                ment_temp += f"""{i}({dicts[i]['rate']}%), """
            ment_temp = ment_temp[:-2]
            return ment_temp

        plus_ment = ment_maker(plus)
        minus_ment = ment_maker(minus)

        ment =''
        if plma_g == True:
            ment = f"""업종별로 상승한 업종은 {plus_ment} 등이다. 하락한 업종은 {minus_ment} 등이다."""
        elif plma_g == False:
            ment = f"""업종별로 하락한 업종은 {minus_ment} 등이다. 상승한 업종은 {plus_ment} 등이다. """


        return(ment)
    except:
        time.sleep(3)
        upjong_maker(kos, plma_g)

#코스닥 업종별
def upjong_kosdaq(plma_g):
    # try:

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    dics = {103:{'name':'기타서비스'}, 104:{'name':'IT'} ,106:{'name':'제조'} \
        ,107 :{'name':'건설'}, 108 :{'name':'유통'}, 110:{'name':'운송'}, 111:{'name':'금융'}, 112:{'name':'통신방송서비스'} \
        ,115:{'name':'음식료/담배'}, 116:{'name':'섬유/의류'}, 117:{'name':'종이/목재'}, 118:{'name':'출판'} \
        , 119:{'name':'화학'}, 120:{'name':'제약'},121 :{'name':'비금속'}, 122:{'name':'금속'} \
        , 123 :{'name':'기계/장비'}, 124:{'name':'일반전기전자'}, 125:{'name':'의료/정밀기기'}, 126:{'name':'운송장비/부품'} \
        , 127 :{'name':'기타 제조'}, 128:{'name':'통신서비스'}, 129:{'name':'방송서비스'}, 130:{'name':'인터넷'}, \
            131:{'name':'디지털컨텐츠'}, 132:{'name':'소프트웨어'}, 133:{'name':'컴퓨터서비스'},134:{'name':'통신장비'}, \
            135:{'name':'정보기기'},136:{'name':'반도체'},137:{'name':'IT부품'},141:{'name':'오락,문화'}}

    cd_socket_list = []
    for i in [*dics]:
        ii = str(i)
        dics[i]['cd_in_socket'] = f'3{ii[0]}3{ii[1]}3{ii[2]}'

    ###0213 화면. 업종 하나씩 보내서 함. 여기는 업종번호 106에 보냄. 가운데 313036  이 그것. 그 번호만 바꾸면 됨.

    ip = '58.229.136.91'

    clientSocket.connect((ip, 14811))
    for ii in [*dics]:
        try:
            a=f'fefd4d54000000303031323654000200390155504a4f4e470000000000000000000030323133202' \
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
            # print(line + str(ii))
            temp_rate = line.split('|')[3]
            dics[ii]["rate"] =re.search(r'[+-]\d+\.\d\d',temp_rate)[0]
            time.sleep(0.3)
        except:
            dics[ii]["rate"] = '0'
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
    # print(plus)
    # print(minus)

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

if __name__ == '__main__':
    # print(kos_sentences('kospi',True))
    print(background())
    # print(kos_toojaja('kospi',True))

#코스피, 코스닥 메인 숫자
#거기서 나온 plma 넘기기

#업종별

#환율