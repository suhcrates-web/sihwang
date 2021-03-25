from flask import Flask, render_template, url_for, request, redirect, jsonify
from datetime import datetime, timedelta
from jonghap import jonghap

app = Flask(__name__)

@app.route('/sihwang/', methods = ['GET'])
def index():
    with open('C:/stamp/sihwang.csv', 'r') as f:
        state_file = f.readlines()[0].split(',')
    state = state_file[0]
    article=''
    now = ''
    state_m = ''

    print(state)
    if state == '1':
        state_m = '장중'
        with open('data/jonghap.csv', 'r') as f:
            data = f.readlines()[0].split('|')
        
        article = data[0]
        now = data[1]
    elif state == '0':
        this_time = datetime.strptime(state_file[1], '%Y-%m-%d %H:%M:%S')
        if this_time.day != datetime.today().day:
            state_m = '개장전'
            article = '개장전'
        else:
            state = '2'
            state_m = '장마감'
            with open('data/jonghap.csv', 'r') as f:
                data = f.readlines()[0].split('|')
            article = data[0]
            now = data[1]
    elif state == '2':
            state_m = '장마감'
            with open('data/jonghap.csv', 'r') as f:
                data = f.readlines()[0].split('|')
            article = data[0]
            now = data[1]
    with open('C:/stamp/dangbun_id.txt', 'r') as f:
            id_0 = f.readlines()[0]



    return render_template('sihwang.html', article=article, now=now, id_0=id_0, state=state, state_m = state_m)

@app.route('/sihwang_post', methods = ['POST'])
def si_post():
    if request.method =='POST':
        cmd = request.form['cmd']
        state = request.form['state']
        if state == '2':
            magam = True
        else:
            magam = False

        if cmd == 'giveme':
            now =datetime.today()
            with open('data/jonghap_time.csv', 'r') as f:
                ago = f.readlines()[0]
            
            ago =datetime.strptime(ago, '%Y-%m-%d %H:%M:%S')
            if (now-ago)<timedelta(minutes=2): #2분미만
                message = "다른 사람이 생성중이거나 최근 생성 2분 미만입니다…좀만 기다려보세요"
                cmd = 'not_yet'
                time = ''
            else:
                if magam:
                    result = jonghap(magam)
                elif state == '1':
                    result = jonghap()
                elif state == '0':
                    result = {'ment':'개장전', 'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                message = result['ment']
                time = result['time']
                cmd  = 'ok'
            return {"message": message , "cmd":cmd, "time":time}


@app.route('/change_dangbun', methods = ['POST'])
def change():
    if request.method =='POST':
        id_num = request.form['id']  
        print(id_num)
        with open('C:/stamp/dangbun_id.txt', 'w') as f:
            f.writelines([id_num])

    return ''


if __name__ == "__main__":
    # serve(app, host = '0.0.0.0', port = '3389', threads=1)
    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')[0]#노트북 5232, 데스크탑 5231
        # port = port[0]
    # print(port)
    if port == '5232':
        host = '172.30.1.53'
    elif port == '5231':
        host= '0.0.0.0'
    port=5233
    #172.30.1.53
    #0.0.0.0
    app.run(host = host, port = port, debug=True)
