from pymongo import MongoClient
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import json
import time
import datetime
import bs4
import os
import re
import pymongo
import django


url = 'mongodb+srv://'+id+':'+password+'@boardlist.lfr3b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
#UTC 시간
dt_utc = datetime.datetime.utcnow()

#파이선 파일 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

client = pymongo.MongoClient(url)
db = client.boardList

def create_index():
    db.All.create_index('title')
    db.All.create_index('link')
    db.All.create_index('writer')
    db.All.create_index('time')
    db.All.create_index('site')
    db.All.create_index('comments')
    db.All.create_index('viewers')
    db.All.create_index("createdAt", expireAfterSeconds=259200)
    db.Theqoo.create_index('title')
    db.Theqoo.create_index('link')
    db.Theqoo.create_index('writer')
    db.Theqoo.create_index('time')
    db.Theqoo.create_index('site')
    db.Theqoo.create_index('comments')
    db.Theqoo.create_index('viewers')
    db.Theqoo.create_index("createdAt", expireAfterSeconds=259200)
    db.FMKorea.create_index('title')
    db.FMKorea.create_index('link')
    db.FMKorea.create_index('writer')
    db.FMKorea.create_index('time')
    db.FMKorea.create_index('site')
    db.FMKorea.create_index('comments')
    db.FMKorea.create_index('viewers')
    db.FMKorea.create_index("createdAt", expireAfterSeconds=259200)
    db.Humoruni.create_index('title')
    db.Humoruni.create_index('link')
    db.Humoruni.create_index('writer')
    db.Humoruni.create_index('time')
    db.Humoruni.create_index('site')
    db.Humoruni.create_index('comments')
    db.Humoruni.create_index('viewers')
    db.Humoruni.create_index("createdAt", expireAfterSeconds=259200)

#Create Index
#Test

print("끝")
session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
}
def now():
    now = datetime.datetime.now()
    print(now)

def link_craw(url):
    req = requests.get(url, headers = headers)
    html = req.text
    # html1 = session.get()
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def test_craw():
    Theqoo_craw = link_craw("https://theqoo.net/hot")
    test_craw = link_craw("https://theqoo.net/square")
    my_craws = test_craw.select("tbody >tr")
    url = ("https://theqoo.net")
    nodata = 1
    check = db.Test.find()
    c = list(check)
    late = []
    if(len(c) != 0):
        sort_db = db.Test.find().sort("createdAt", -1)
        for i in range(5):
            late.append(sort_db[i]['link'])
        #late = sort_db[0]['title']
        nodata = 0
    for i, craw in enumerate(my_craws):
        i += 1
        if (9 < i < 15):
            title = craw.select_one(".title > a>span").text
            link = craw.select_one(".title > a")['href']
            url_link = url+link
            link_url = link_craw(url_link)
            c = link_url.select_one(".rd_hd")
            links = c.select_one(".board >div> .side >.link")['href']
            time = c.select_one(".board >.btm_area > div > span").text
            v = c.select_one(".theqoo_document_header >.count_container").text
            n = v.split()
            viewers = n[0]
            c = n[1]
            comments = int(c)
            print(type(comments))
            writer = "무명의 더쿠"
            site = "더쿠"
            doc = {
                'title': title,
                'link': links,
                'writer':writer,
                'viewers': viewers,
                'date': time,
                'site': site,
                'comments': comments,
                'createdAt': dt_utc
            }
            if nodata == 0:
                if links not in late:
                    db.Test.insert_one(doc)
                    db.All.insert_one(doc)
                    print("Data Insert")
                else:
                    break
            else:
                db.Test.insert_one(doc)
                db.All.insert_one(doc)





def Theqoocraw():
    Theqoo_craw = link_craw("https://theqoo.net/hot")
    my_craws = Theqoo_craw.select("tbody >tr")
    url = ("https://theqoo.net")
    nodata = 1
    check = db.Theqoo.find()
    c = list(check)
    print(check)
    if (len(c) != 0):
        sort_db = db.Theqoo.find().sort("date", -1)
        late = sort_db[0]['title']
        nodata = 0
        print(len(c))
    for i, craw in enumerate(my_craws):
        i += 1
        if (5 < i < 10):
            title = craw.select_one(".title > a>span").text
            link = craw.select_one(".title > a")['href']
            url_link = url+link
            link_url = link_craw(url_link)
            c = link_url.select_one(".rd_hd")
            links = c.select_one(".board >div> .side >.link")['href']
            time = c.select_one(".board >.btm_area > div > span").text
            v = c.select_one(".theqoo_document_header >.count_container").text
            n = v.split()
            viewers = int(re.sub(r'[^0-9]', '', n[0]))
            comments = int(n[1])
            writer = "무명의 더쿠"
            site = "더쿠"
            doc = {
                'title': title,
                'link': links,
                'writer':writer,
                'viewers': viewers,
                'date': time,
                'site': site,
                'comments': comments,
                'createdAt': dt_utc
            }
            #print(late)
            #print(title)
            if nodata == 0:
                if late != title:
                    db.Theqoo.insert_one(doc)
                    db.All.insert_one(doc)
                    print("Data Insert")
                else:
                    break
            else:
                db.Theqoo.insert_one(doc)
                db.All.insert_one(doc)
def Fmkoreacraw():
    Fmkorea_craw = link_craw("https://www.fmkorea.com/best")
    url = ("https://www.fmkorea.com/best")
    my_craws = Fmkorea_craw.select("div.fm_best_widget >ul >li:nth-child(n+5)")
    nodata = 1
    check = db.FMKorea.find()
    c = list(check)
    if (len(c) != 0):
        #sort_db = db.FMKorea.find().sort("createdAt", 1)
        sort_db = db.FMKorea.find().sort("date", -1)
        late = sort_db[0]['link']
        print(late)
        nodata = 0
    for i, craw in enumerate(my_craws):
        i += 1
        if (i < 6):

            title = craw.select_one("div.li > h3.title> a").text
            #tt = l.select_one("div#bd_capture> div.rd_hd> div.board > div.top_area>h1>span").text
            t = title[:-6]
            tt = t.lstrip()
            link = craw.select_one("div.li > h3.title> a")['href']
            links = url + link
            l = link_craw(links)
            writer = craw.select_one("div.li >div> span.author").text
            w = writer[3:]
            v = l.select_one("div#bd_capture> div.rd_hd> div.board > div.btm_area> div:nth-child(2)>span:nth-child(1)>b").text
            viewer = int(v)
            co = l.select_one("div#bd_capture> div.rd_hd> div.board > div.btm_area> div:nth-child(2)>span:nth-child(3)>b").text
            comments = int(co)
            site = "에펨"
            c = craw.select_one("span.regdate")
            cs = c.find(text=lambda text:isinstance(text, bs4.Comment))
            comment = cs.replace('\t', '').replace('\n', '')
            #date = l.select_one("div#bd_capture> div.rd_hd> div.board > div.top_area>span").text[:11]
            date = datetime.date.today().strftime("%Y.%m.%d ")
            date_t = date + comment
            print(date_t)
            doc = {
                'title': tt,
                'link': links,
                'writer': w,
                'viewers': viewer,
                'date': date_t,
                'site': site,
                'comments': comments,
                'createdAt': dt_utc
            }
            if nodata == 0:
                if late != links:
                    db.FMKorea.insert_one(doc)
                    db.All.insert_one(doc)
                    print("Data Insert")
                    time.sleep(1)
                elif(late == links):
                    break
            else:
                db.FMKorea.insert_one(doc)
                db.All.insert_one(doc)
                time.sleep(1)


def Humorunicraw():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = "http://web.humoruniv.com/board/humor/list.html?table=pds"
    driver.get(url)

    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    mycraw = soup.select("#post_list > tbody > tr")
    n_url = "http://web.humoruniv.com/board/humor/"

    nodata = 1
    check = db.Humoruni.find()
    c = list(check)
    if (len(c) != 0):
        sort_db = db.Humoruni.find().sort("date", -1)
        late = sort_db[0]['title']
        nodata = 0
    for i, craw in enumerate(mycraw):
        if i < 5:
            co = craw.select_one("td.li_sbj > a> span.list_comment_num").text[2:-1]
            comments = int(co)
            craw.select_one("td.li_sbj > a").span.decompose()
            t = craw.select_one("td.li_sbj > a").text.strip()

            sample_link = craw.select_one("td.li_sbj > a")["href"]
            link = n_url + sample_link
            t1 = craw.select_one("td.li_date > span.w_date").text
            t1_r = t1.replace('-', '.')

            t2 = craw.select_one("td.li_date > span.w_time").text
            time = t1_r +" "+ t2
            vi = craw.select_one("td:nth-child(5)").text.replace('\t', '').replace('\n', '')
            viewers = int(re.sub(r'[^0-9]', '', vi))
            writer = craw.select_one("td.li_icn> table> tbody> tr>td:nth-child(2)> span> span").text
            site = "웃긴대학"
            doc = {
                'title':t,
                'link': link,
                'writer':writer,
                'date': time,
                'site': site,
                'comments': comments,
                'viewers': viewers,
                'createdAt': dt_utc
            }
            if nodata == 0:
                if late != t:
                    db.Humoruni.insert_one(doc)
                    db.All.insert_one(doc)
                    print("Data Insert")
                else:
                    break
            else:
                db.Humoruni.insert_one(doc)
                db.All.insert_one(doc)


def craw():
    Fmkoreacraw()
    Theqoocraw()
    Humorunicraw()


craw()
#test_craw()
#test_craw()
#3일 = 259200
# schedule.every(10).seconds.do(now)
# schedule.every(1).minutes.do(craw)
# while True:
#     schedule.run_pending()
#     time.sleep(1)
# 6일 518400  28800 1200
# 12 시간 5시49
# 10 시간 3시 49
# 8시간 1시 49
# 8시간 20
