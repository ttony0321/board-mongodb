from board import cron
import re


def Theqoocraw():
    Theqoo_craw = cron.link_craw("https://theqoo.net/hot")
    my_craws = Theqoo_craw.select("tbody >tr")
    url = ("https://theqoo.net")
    nodata = 1
    check = cron.db.Theqoo.find()
    c = list(check)
    #print(check)
    if (len(c) != 0):
        sort_db = cron.db.Theqoo.find().sort("date", -1)
        late = sort_db[0]['title']
        nodata = 0
        #print(len(c))
    for i, craw in enumerate(my_craws):
        i += 1
        if (5 < i < 10):
            title = craw.select_one(".title > a>span").text
            link = craw.select_one(".title > a")['href']
            url_link = url+link
            link_url = cron.link_craw(url_link)
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
                'createdAt': cron.dt_utc
            }
            #print(late)
            #print(title)
            if nodata == 0:
                if late != title:
                    cron.db.Theqoo.insert_one(doc)
                    cron.db.All.insert_one(doc)
                    print("Theqoo Data Insert")
                else:
                    break
            else:
                cron.db.Theqoo.insert_one(doc)
                cron.db.All.insert_one(doc)
                print("Theqoo Data Insert")


Theqoocraw()