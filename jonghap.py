import time
from datetime import datetime
from article import kos_toojaja, background, kos_sentences, background_magam, upjong_maker, upjong_kosdaq

def jonghap(magam=False, version ='1'):

    if version == '1':
        jong_time = 'jonghap_time'
        jong = 'jonghap'
    elif version == '2':
        jong_time = 'jonghap_time2'
        jong = 'jonghap2'

    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(f'data/{jong_time}.csv', 'w') as f:
        f.writelines([now])
    if not magam:
        # bg = background()
        pass
    elif magam:
        # bg = background_magam()
        pass
    bg = {}

    bg['kospi_plma'] = False
    bg['kosdaq_plma'] = False
    # bg['kospi_plma']

    kospi_toojaja = kos_toojaja('kospi', bg['kospi_plma'])
    time.sleep(3)
    kosdaq_toojaja = kos_toojaja('kosdaq',bg['kosdaq_plma'])
    time.sleep(3)
    kospi_upjong = upjong_maker('kospi',bg['kospi_plma'])
    kospi_jongmok = kos_sentences('kospi', bg['kospi_plma'])
    # try:
    kosdaq_upjong = upjong_kosdaq(bg['kosdaq_plma'])
    # except:
    #     kosdaq_upjong = "(코스닥 업종 없음)"
    kosdaq_jongmok = kos_sentences('kosdaq', bg['kosdaq_plma'])
#     ment = f"""<br><br>{bg['kospi_ment']}<br><br>{kospi_toojaja}<br><br>{kospi_jongmok}\
# <br><br>{kospi_upjong}<br><br>{bg['kosdaq_ment']}<br><br>{kosdaq_toojaja}<br><br>{kosdaq_jongmok}\
# <br><br>{kosdaq_upjong}<br><br>{bg['exch_ment']}<br><br>"""

    ment =f"""(코스피) <br><br>{kospi_toojaja}<br><br>{kospi_jongmok}\
<br><br>{kospi_upjong}<br>(코스닥)<br>{kosdaq_toojaja}<br><br>{kosdaq_jongmok}\
<br><br>{kosdaq_upjong}"""
    # return {'ment':ment}
    with open(f'data/{jong}.csv', 'w') as f:
        f.writelines([ment,'|',str(now)])
    return {'ment':ment, 'time':now}
# jonghap()
# print(datetime.now())
if __name__ == '__main__':
    print(jonghap()['ment'])