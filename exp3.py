from datetime import datetime
h = datetime.now().hour
ampm= '오전'
if h<=12:
    ampm= '오전'
else:
    ampm = '오후'
    h = h-12


print(h)