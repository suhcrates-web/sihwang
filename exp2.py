from bs4 import BeautifulSoup
import requests, re

def kos_sentences(kos, plma):
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
    print(plus)
    print(minus)
    
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
        print(f"{kos_han} 시가총액 상위 10개 종목 중 {plma_sent(minus, only=True)}")
    elif state == 'only_plus':
        print(f"{kos_han} 시가총액 상위 10개 종목 중 {plma_sent(plus, only=True)}")
    elif state == 'both':
        if plma:
            print(f"{kos_han} 시가총액 상위 10개 종목 중 {plma_sent(plus)} {plma_sent(minus)}")
        else:
            print(f"{kos_han} 시가총액 상위 10개 종목 중 {plma_sent(minus)} {plma_sent(plus)}")
kos_sentences('kospi', True)