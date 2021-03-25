import time
from datetime import datetime
from article import kos_toojaja, background, kos_sentences, background_magam

def jonghap(magam=False):


    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('data/jonghap_time.csv', 'w') as f:
        f.writelines([now])
    if not magam:
        bg = background()
    elif magam:
        bg = background_magam()
    kospi_toojaja = kos_toojaja('kospi', bg['kospi_plma'])
    time.sleep(3)
    kospi_jongmok = kos_sentences('kospi', bg['kospi_plma'])
    time.sleep(3)
    kosdaq_toojaja = kos_toojaja('kosdaq',bg['kosdaq_plma'])
    time.sleep(3)
    kosdaq_jongmok = kos_sentences('kosdaq', bg['kosdaq_plma'])
    ment = f"""<br><br>{bg['kospi_ment']}<br><br>{kospi_toojaja}<br><br>{kospi_jongmok}<br><br>{bg['kosdaq_ment']}<br><br>{kosdaq_toojaja}<br><br>{kosdaq_jongmok}<br><br>{bg['exch_ment']}<br><br>"""
    # return {'ment':ment}
    with open('data/jonghap.csv', 'w') as f:
        f.writelines([ment,'|',str(now)])
    return {'ment':ment, 'time':now}
# jonghap()
# print(datetime.now())
if __name__ == '__main__':
    print(jonghap()['ment'])