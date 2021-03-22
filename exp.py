import socket, codecs, time, re
from datetime import date, timedelta, datetime
from bs4 import BeautifulSoup
import os, glob, json, requests
import time
import math
from toolbox import dict_sort, banolim
from article import kos_toojaja, background, kos_sentences

with open('data/jonghap.csv', 'r') as f:
    data = f.readlines()[0].split('|')
    article = data[0]
    now = data[1]

print(data)
