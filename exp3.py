from bs4 import BeautifulSoup
import requests, re
url = 'https://finance.naver.com/sise/sise_group.nhn?type=upjong'
temp = requests.get(url)
temp = BeautifulSoup(temp.text, 'html.parser')
# nos = temp.find_all('td', {'class':'no'})
print(temp)