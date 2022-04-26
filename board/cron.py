from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
from pymongo import MongoClient
from selenium import webdriver
import pymongo
import datetime
import time
import requests
import bs4
import cryptocode
import dns.resolver
import re
pk = 'test'
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']
p = "YXHVLgufTw61*dbtsFqBtJ1ukRN6TJAXyyg==*5ercXsjzHkKU3/nRlZDd5w==*5CM90YKrCDhYrQ5HdMUk6w=="
decoded = cryptocode.decrypt(p, pk)

userid = quote_plus('ttony0321')
password = quote_plus(decoded)
#uri = 'mongodb+srv://'+userid+':'+password+'@boardlist.lfr3b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
uri = 'mongodb+srv://'+userid+':'+password+'@boardlist.lfr3b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
print(uri)
#MongoDB 접근
client = pymongo.MongoClient(uri)
db = client.boardList

#utc 시간
dt_utc = datetime.datetime.utcnow()


session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}

def link_craw(url):
    req = requests.get(url, headers=headers)
    html = req.text
    # html1 = session.get()
    soup = BeautifulSoup(html, 'html.parser')
    return soup