from bs4 import BeautifulSoup
import requests, re
import socket, codecs, time, re
from toolbox import dict_sort, banolim
from datetime import date, timedelta, datetime

def temptemp(kos, plma_g):
    # try:

        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        ##화면번호 211
        if kos=='kospi':
            a='fefd4d540000003030323531540002004e0153544f434b4700003030303032303137303231382020303231383030000043333373756863726174653030303030303030303030303031353833303133343430313236312020000000000000000000000000000000003030313534393030387f3030311e2430303030303032303137303035302020202020202020202020202020202030402020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020203030303236393030311f3330321f31301f32351f31311f31321f31331f3134'

        if kos == 'kosdaq':
            a ='fefd4d540000003030323531540002004e0153544f434b4700003030303032303137303231382020303231383030000043333373756863726174653030303030303030303030303031393430323131313731333139352020000000000000000000000000000000003030313534393030387f3130311e2430303030303032303137303035302020202020202020202020202020202030402020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020202020203030303236393030311f3330321f31301f32351f31311f31321f31331f3134'

        ip = '211.115.74.81'

        a= codecs.decode(a, 'hex')
        clientSocket.connect((ip, 14811))

        line_bf = ''
        tik_dick= {}
        # while True:
        clientSocket.send(a)
        test =True
        skip = False
        line =''
        data = b''
        # data = clientSocket.recv(100000)
        # time.sleep(3)

        dics = {}
        for _ in range(0,10):
            new = clientSocket.recv(1000000)
            data_temp = new.hex()
            # num += len(data_temp)
            temp = ''
            han = False
            for i in range(len(data_temp)//2):
                if skip:
                    skip = False
                    pass
                else:
                    if han:
                        han = False
                    else:
                        try:
                            ps =data_temp[i*2:i*2+2]
                            if ps == '1f':
                                # print('|',end='')
                                temp +='|'
                            else:
                                # print(codecs.decode(ps,'hex').decode('cp949')  ,end='')
                                temp += codecs.decode(ps,'hex').decode('utf-8')

                        except:
                            temp += '.'
            # print(temp)
            line += temp
            time.sleep(3)

        # line_old =''
        # n = 0
        # while True :
        #     n+=1
        #     line = ''
        #     data = ''
        #     for _ in range(10):
        #         data += clientSocket.recv(1024)
        #         time.sleep(2)
        #
        #
        data = data.hex()
        # print(data)
        # print(codecs.decode(data, 'hex').decode('cp949'))
        # line = []
        han = False
        print('=====================================')

        line =line.replace('\n','')
        lines = line.split('\t')
        n =0
        print(lines)
        for i in lines:
            if bool(re.search('0J0',i)):
                try:
                    code = re.findall(r'(?<=0J0\d\d)\d\d\d',i)[0]
                    dics[code] = lines[n+4]
                except:
                    pass

            n +=1
        print(dics)
        # han = False
        # for i in range(len(data)//2):
        #     if skip:
        #         skip = False
        #         pass
        #     else:
        #         if han:
        #             han = False
        #         else:
        #             try:
        #                 ps =data[i*2:i*2+2]
        #                 if ps == '1f':
        #                     # print('|',end='')
        #                     line +='|'
        #                 else:
        #                     # print(codecs.decode(ps,'hex').decode('cp949')  ,end='')
        #                     line += codecs.decode(ps,'hex').decode('utf-8')
        #
        #             except:
        #                 line += '.'
        # print('=====================================')
        # print(line)
        #     line_old = line_old + line + f"씨발{n}{n}{n}{n}{n}{n}{n}{n}{n}{n}{n}{n}{n}{n}{n}{n}{n}{n}씨발"
        #     print("==============================================================================")
        #     print(n)
        #     print("==============================================================================")
        #     print(line_old)
        #     time.sleep(3)
    #     line= line[line.index('MT'):]
    #     line= re.sub('.*                              ','',line)
    #     line = line[5:]
    #     line = line.split(sep='\n')
    #     # print(line)
    #     dicts={}
    #     plus_num =0
    #     minus_num = 0
    #     for i in line:
    #         temp = i.split('|')
    #         if temp[1] in ['코스피배당성장50','코스피고배당50','종합(KOSPI)', '변동성지수']:
    #             pass
    #         else:
    #             rate = float(temp[5].replace('+',''))
    #             if rate >0 :
    #                 plus_num +=1
    #             elif rate <0:
    #                 minus_num +=1
    #             dicts[temp[1]]={'rate':rate}
    #     # print(dicts)
    #
    #     dicts = dict_sort(dicts,'rate')
    #     # print(dicts)
    #
    #     if plus_num <5:
    #         minus_num = 10 - plus_num
    #     elif minus_num <5:
    #         plus_num = 10 - minus_num
    #     else:
    #         plus_num, minus_num = 5,5
    #
    #     plus = [*dicts][:plus_num]
    #     minus = [*dicts][-minus_num:][::-1]
    #     # print(plus)
    #     # print(minus)
    #
    #
    #
    #     def ment_maker(plma_list):
    #         ment_temp = ''
    #         for i in plma_list:
    #             ment_temp += f"""{i}({dicts[i]['rate']}%), """
    #         ment_temp = ment_temp[:-2]
    #         return ment_temp
    #
    #     plus_ment = ment_maker(plus)
    #     minus_ment = ment_maker(minus)
    #
    #     ment =''
    #     if plma_g == True:
    #         ment = f"""업종별로 상승한 업종은 {plus_ment} 등이다. 하락한 업종은 {minus_ment} 등이다."""
    #     elif plma_g == False:
    #         ment = f"""업종별로 하락한 업종은 {minus_ment} 등이다. 상승한 업종은 {plus_ment} 등이다. """
    #
    #
    #     return(ment)
    # except:
    #     time.sleep(3)
    #     upjong_maker(kos, plma_g)
    # except:
    #     print('fail')
if __name__ == "__main__":
    temptemp('kosdaq',True)