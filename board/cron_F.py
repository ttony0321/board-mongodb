from board import cron
import time
import bs4

def Fmkoreacraw():
    Fmkorea_craw = cron.link_craw("https://www.fmkorea.com/best")
    url = ("https://www.fmkorea.com/best")
    my_craws = Fmkorea_craw.select("div.fm_best_widget >ul >li:nth-child(n+5)")
    nodata = 1
    check = cron.db.FMKorea.find()
    c = list(check)
    if (len(c) != 0):
        #sort_db = db.FMKorea.find().sort("createdAt", 1)
        sort_db = cron.db.FMKorea.find().sort("date", -1)
        late = sort_db[0]['link']
        #print(late)
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
            l = cron.link_craw(links)
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
            date = cron.datetime.date.today().strftime("%Y.%m.%d ")
            date_t = date + comment
            #print(date_t)
            doc = {
                'title': tt,
                'link': links,
                'writer': w,
                'viewers': viewer,
                'date': date_t,
                'site': site,
                'comments': comments,
                'createdAt': cron.dt_utc
            }
            if nodata == 0:
                if late != links:
                    cron.db.FMKorea.insert_one(doc)
                    cron.db.All.insert_one(doc)
                    print("FM Data Insert")
                    time.sleep(1)
                elif(late == links):
                    break
            else:
                cron.db.FMKorea.insert_one(doc)
                cron.db.All.insert_one(doc)
                time.sleep(1)
                print("FM Data Insert")

Fmkoreacraw()