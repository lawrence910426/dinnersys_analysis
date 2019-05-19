from bs4 import BeautifulSoup
import urllib.request
import csv
import re
from datetime import datetime
from dateutil.relativedelta import *
import MySQLdb

db  =  MySQLdb . connect ( 
     host = "localhost" ,     # 主機名
     user = "root" ,          # 用戶名
     passwd = "2rjurrru" ,    # 密碼
     db = "ai" )              # 數據庫名稱
cur = db.cursor()
sql_command = "DELETE FROM `ai`.`weather`;"
cur.execute (sql_command)

url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=466880&stname=%25E6%259D%25BF%25E6%25A9%258B&datepicker=2019-05-14'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "lxml")
table = soup.select_one("#MyTable")

start = datetime.strptime("2018-09-01" ,"%Y-%m-%d")
end = datetime.strptime(input("Enter time upper bound(%Y-%m-%d)") ,"%Y-%m-%d")

while start != end:
    rows = []
    for r in table.select("tr"):
        row = []
        for td in r.find_all("td"):
            row.append(" ".join(re.findall(r'[0-9.]+' ,td.text)))
        rows.append(row)
    
    for row in rows:
        if len(row) == 0:
            continue
        
        if row[0] == "24":
            time = (start + relativedelta(days=1)).strftime("%Y-%m-%d") + " 00:00:00"
        else:
            time = start.strftime("%Y-%m-%d") + " " + row[0] + ":00:00"
        pressure = row[1]
        sea_pres = row[2]
        temp = row[3]
        dew_point = row[4]
        humidity = row[5]
        precp = row[10]
        cloud = -1 if row[16] == "..." else row[16]

        sql_command = """
        INSERT INTO `ai`.`weather`
        (`time`,`pressure`,`sea_pres`,`temp`,`dew_point`,`humidity`,`precp`,`cloud`)
        VALUES('{}','{}','{}','{}','{}','{}','{}','{}');
        """.format(time ,pressure ,sea_pres ,temp ,dew_point ,humidity ,precp ,cloud)
        print(sql_command)
        cur.execute (sql_command)
    start += relativedelta(days=1)

sql_command = "UPDATE `ai`.`weather` SET cloud = null WHERE cloud = -1;"
cur.execute (sql_command)
db.close ()
