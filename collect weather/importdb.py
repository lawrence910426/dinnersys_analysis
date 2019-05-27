import MySQLdb
import csv
from datetime import datetime
from dateutil.relativedelta import *


db  =  MySQLdb . connect ( 
     host = "localhost" ,     # 主機名
     user = "root" ,          # 用戶名
     passwd = "2rjurrru" ,    # 密碼
     db = "ai" )              # 數據庫名稱

# 查詢前，必須先獲取游標
cur = db.cursor()

start = datetime.strptime("2018-06-01" ,"%Y-%m-%d")
end = datetime.strptime("2019-05-18" ,"%Y-%m-%d")

while start != end:
     fname = "csv/" + start.strftime("%Y-%m-%d") + ".csv"
     with open(fname, newline='') as csvfile:
          rows = csv.reader(csvfile)
          for row in rows:
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
               cloud = None if row[16] == "..." else row[16]

               sql_command = """
               INSERT INTO `ai`.`weather`
               (`time`,`pressure`,`sea_pres`,`temp`,`dew_point`,`humidity`,`precp`,`cloud`)
               VALUES('{}','{}','{}','{}','{}','{}','{}','{}');
               """.format(time ,pressure ,sea_pres ,temp ,dew_point ,humidity ,precp ,cloud)
               # print(sql_command)
               cur.execute (sql_command)
     start += relativedelta(days=1)
db.close ()