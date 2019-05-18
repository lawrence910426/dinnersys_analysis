from bs4 import BeautifulSoup
import urllib.request
import csv
import re
from datetime import datetime
from dateutil.relativedelta import *

url = 'https://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=466880&stname=%25E6%259D%25BF%25E6%25A9%258B&datepicker=2019-05-14'
html = urllib.request.urlopen(url).read()
soup = BeautifulSoup(html, "lxml")
table = soup.select_one("#MyTable")
# python3 just use th.text
# headers = [th.text.encode("utf-8") for th in table.select("tr th")]
start = datetime.strptime("2018-06-01" ,"%Y-%m-%d")
end = datetime.strptime("2019-05-18" ,"%Y-%m-%d")

while start != end:
    path = "csv/" + start.strftime("%Y-%m-%d") + ".csv"
    with open(path, "w" ,newline='') as f:
        wr = csv.writer(f ,lineterminator='\r\n')
        # wr.writerow(headers)

        for row in table.select("tr"):
            row_data = []
            for td in row.find_all("td"):
                row_data.append(" ".join(re.findall(r'[0-9.]+' ,td.text)))
            if not (len(row_data) == 0):
                wr.writerow(row_data)
    start += relativedelta(days=1)
        
    
