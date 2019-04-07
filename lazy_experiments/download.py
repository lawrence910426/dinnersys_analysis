import requests
data = [
    ["2018/09/13 00:00:00" ,"2018/09/13 00:00:00"] ,
    ["2018/09/13 00:00:00" ,"2018/09/13 00:00:00"] ,
    ["2018/09/13 00:00:00" ,"2018/09/13 00:00:00"] ,
    ["2018/09/13 00:00:00" ,"2018/09/13 00:00:00"] ,
    ["2018/09/13 00:00:00" ,"2018/09/13 00:00:00"]
]

for item in data:
    link = "https://dinnersystem.ddns.net/dinnersys_beta/backend/backend.php?cmd=select_other&esti_start=" + item[0] "&esti_end=" + item[1] 
    f = requests.get(link)
    text_file = open(item[0] + " " + item[1], "w")
    text_file.write(f.text)
    text_file.close()