import MySQLdb

db  =  MySQLdb . connect ( 
     host = "localhost" ,     #主機名
     user = "john" ,          #用戶名
     passwd = "megajonhy" ,   #密碼
     db = "jonhydb" )         #數據庫名稱

#查詢前，必須先獲取游標
cur = db.cursor()

#執行的都是原生SQL語句
cur.execute ( "SELECT * FROM YOUR_TABLE_NAME" )

db . close ()