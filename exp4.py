import socket, codecs, time, re

data = 'c1bec7d5284b4f53504929'
line = []
a='c1'
print( codecs.decode(a,'hex').decode('cp949'))
# for i in range(len(data)//4):
#     if han:
#         han = False
#     else:
#         try:
#             ps =data[i*2:i*2+2]
#             if ps == '1f':
#                 # print('|',end='')
#                 line +='|'
#             else:
#                 # print(codecs.decode(ps,'hex').decode('cp949')  ,end='')
#                 line += codecs.decode(ps,'hex').decode('utf-8')
#         except:
#             # print('.',end='')
#             line += '.'
#             # try:
#             #     print(codecs.decode(data[i*2:i*2+4],'hex').decode('cp949')  ,end='')
#             #     han = True
#             # except:
#             #     print('.', end='')
# print(line)