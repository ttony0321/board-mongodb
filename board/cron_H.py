from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
#from board import cron
from selenium import webdriver
import re
import board.cron as cron



def Humorunicraw():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    url = "http://web.humoruniv.com/board/humor/list.html?table=pds"
    driver.get(url)

    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    mycraw = soup.select("#post_list > tbody > tr")
    n_url = "http://web.humoruniv.com/board/humor/"

    nodata = 1
    check = cron.db.Humoruni.find()
    c = list(check)
    if (len(c) != 0):
        sort_db = cron.db.Humoruni.find().sort("date", -1)
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
            t2 = craw.select_one("td.li_date > span.w_time").text
            time = t1 +" "+ t2
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
                'createdAt': cron.dt_utc
            }
            if nodata == 0:
                if late != t:
                    cron.db.Humoruni.insert_one(doc)
                    cron.db.All.insert_one(doc)
                    print("Hu Data Insert")
                else:
                    break
            else:
                cron.db.Humoruni.insert_one(doc)
                cron.db.All.insert_one(doc)
                print("Hu Data Insert")


Humorunicraw()