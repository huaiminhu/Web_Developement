import mysql.connector
import requests as rs
from bs4 import BeautifulSoup as bs
import re

conn = mysql.connector.connect(host = "localhost", port = "3306",
                               user = "root", password = *****,
                               database = "account")

cursor = conn.cursor()
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"}

# 爬取各網頁並把資料新增至MySQL Database Topics表格
url1 = "https://news.tvbs.com.tw/health"
# r1 = rs.get(url1, headers = headers)
# if r1.status_code == 200:
#     s1 = bs(r1.text, "html.parser")
#     name1 = s1.find_all("h2", class_ = "txt")
#     time1 = s1.find_all("div", class_ = "time")
#     urls1 = s1.find_all("a", attrs = {"target" : "_blank"})
#     for i, j, k in zip(name1[6:], time1, urls1[39:]):
#         print(i.text.strip(), "\n", j.text.strip()[:-6], "\n", "https://news.tvbs.com.tw" + k.get("href").strip())
#         sqlstr1 = 'INSERT INTO Topics (category, name, date, resource, url) VALUES ("健康飲食", "{}", "{}", "TVBS新聞網", "https://news.tvbs.com.tw{}")'.format(i.text.strip(), j.text.strip()[:-6], k.get("href").strip())
#         cursor.execute(sqlstr1)

url2 = "https://health.udn.com/health/rank/newest/1005?from=udn-indexbtn1_ch1005"
# r2 = rs.get(url2, headers = headers)
# for p in range(2, 101):
#     if r2.status_code == 200:
#         s2 = bs(r2.text, "html.parser")
#         name2 = s2.find_all("h3")
#         time2 = s2.find_all("p", class_ = "pic-8to5-item__note")
#         urls2 = s2.find_all("a", class_ = "pic-8to5-item__substance")
#         for i, j, k in zip(name2[13:], time2, urls2):
#             print("1.", i.text.strip(), "\n", "2.", "/".join(j.text.strip()[:11].split("-")), "\n", "3.", "https://health.udn.com" + k.get("href"))
#             sqlstr2 = 'INSERT INTO Topics (category, name, date, resource, url) VALUES ("健康飲食", "{}", "{}", "元氣網", "https://health.udn.com{}")'.format(i.text.strip(), "/".join(j.text.strip()[:11].split("-")), k.get("href"))
#             cursor.execute(sqlstr2)
#         r2 = rs.get("https://health.udn.com/health/rank/newest/1005?page={}".format(p), headers = headers)

# url3 = "https://news.tvbs.com.tw/world"
# r1 = rs.get(url3, headers = headers)
# if r1.status_code == 200:
#     s1 = bs(r1.text, "html.parser")
#     name1 = s1.find_all("h2", class_ = "txt")
#     time1 = s1.find_all("div", class_ = "time")
#     urls1 = s1.find_all("a", attrs = {"target" : "_blank"})
#     for i, j, k in zip(name1[6:], time1, urls1[39:]):
#         # print(i.text.strip(), "\n", j.text.strip()[:-6], "\n", "https://news.tvbs.com.tw" + k.get("href").strip())
#         sqlstr1 = 'INSERT INTO Topics (category, name, date, resource, url) VALUES ("國際情勢", "{}", "{}", "TVBS新聞網", "https://news.tvbs.com.tw{}")'.format(i.text.strip(), j.text.strip()[:-6], k.get("href").strip())
#         cursor.execute(sqlstr1)

# url4 = "https://www.cna.com.tw/topic/newstopic/300.aspx"
# r1 = rs.get(url4, headers = headers)
# if r1.status_code == 200:
#     s1 = bs(r1.text, "html.parser")
#     title = s1.find_all("h2")
#     u1 = s1.select("ul#jsMainList a")
#     for i, j in zip(title[5:], u1):
#         # print(i.text, "\n", j.get("href"), "\n")
#         r2 = rs.get(j.get("href"), headers = headers)
#         if r2.status_code == 200:
#             s2 = bs(r2.text, "html.parser")
#             u2 = s2.select("p a")
#             for k in u2[:11]:
#                 # print(k.get("href"), "\n")
#                 r3 = rs.get(k.get("href"), headers = headers)
#                 if r3.status_code == 200:
#                     s3 = bs(r3.text, "html.parser")
#                     name2 = s3.find("h1")
#                     time = s3.find("div", class_ = "updatetime")
#                     try:
#                         # print(name2.text, "\n", time.text.split(" ")[0], "\n", k.get("href"), "\n")
#                         sqlstr = 'INSERT INTO Topics (category, name, date, resource, url) VALUES ("國際情勢", "{}", "{}", "中央社CNA", "{}")'.format(name2.text.strip(), time.text.split(' ')[0], k.get("href"))
#                         cursor.execute(sqlstr)
#                     except:
#                         pass

for i in range(1, 51):
    url7 = "https://www.bbc.com/zhongwen/trad/topics/c83plve5vmjt?page={}".format(i)
    r1 = rs.get(url7, headers = headers)
    if r1.status_code == 200:
        s1 = bs(r1.text, "html.parser")
        name = s1.find_all("h2")
        time = s1.find_all("time", class_ = "promo-timestamp bbc-1qkagz5 e1mklfmt0")
        urls = s1.find_all("a", class_ = "focusIndicatorDisplayBlock bbc-uk8dsi e1d658bg0")
        for m, n, o in zip(name, time, urls):
            if "節目全長," in m.text:
                new_m = m.text.strip().split(", ")[1][:-4]
                # print(new_m, "\n", "/".join(n.get("datetime").split('-')), "\n", o.get("href"))
                sqlstr = 'INSERT INTO Topics (category, name, date, resource, url) VALUES ("國際情勢", "{}", "{}", "BBC News 中文", "{}")'.format(new_m, "/".join(n.get("datetime").split('-')), o.get("href"))
                cursor.execute(sqlstr)
            else:
                # print(m.text.strip(), "\n", "/".join(n.get("datetime").split('-')), "\n", o.get("href"))
                sqlstr = 'INSERT INTO Topics (category, name, date, resource, url) VALUES ("國際情勢", "{}", "{}", "BBC News 中文", "{}")'.format(m.text.strip(), "/".join(n.get("datetime").split('-')), o.get("href"))
                cursor.execute(sqlstr)

# for i in range(52, 101):
#     url5 = "https://e-info.org.tw/taxonomy/term/258/all?page={}".format(i)
#     r1 = rs.get(url5, headers = headers)
#     r1.encoding = "utf8"
#     if r1.status_code == 200:
#         s1 = bs(r1.text, "html.parser")
#         name = s1.find_all("div", class_ = "views-field views-field-title")
#         time = s1.find_all("span", class_ = "views-field views-field-created")
#         urls = s1.find_all("a", class_ = "readmore")
#         for m, n, o in zip(name, time, urls):
#             # print(m.text.strip(), "\n", "/".join(n.text[:11].split('-')), "\n", "https://e-info.org.tw" + o.get("href"))
#             sqlstr = 'INSERT INTO Topics (category, name, date, resource, url) VALUES ("氣候環境", "{}", "{}", "環境資訊中心 環境新聞", "{}")'.format(m.text.strip(), "/".join(n.text[:11].split('-')), "https://e-info.org.tw" + o.get("href"))
#             cursor.execute(sqlstr)

# for i in range(1, 51):
#     url6 = "https://www.scimonth.com.tw/article/scitech?page={}".format(i)
#     r1 = rs.get(url6, headers = headers)
#     if r1.status_code == 200:
#         s1 = bs(r1.text, "html.parser")
#         name = s1.find_all("div", class_ = "title")
#         time = s1.find_all("small", class_ = "data_t")
#         urls = s1.find_all("a", id = re.compile("ctl00_content_holder_articleRepeater1_ctl\d+_LinkB"))
#         for m, n, o in zip(name, time, urls):
#             # print(m.text.strip(), "\n", "/".join(n.text.split(".")), "\n", "https://www.scimonth.com.tw" + o.get("href"))
#             sqlstr = 'INSERT INTO Topics (category, name, date, resource, url) VALUES ("科學科技", "{}", "{}", "科學月刊", "{}")'.format(m.text.strip(), "/".join(n.text.split(".")), "https://www.scimonth.com.tw" + o.get("href"))
#             cursor.execute(sqlstr)

conn.commit()
conn.close()