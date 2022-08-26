# coding=utf-8
import time
import datetime

def get_time():
    # 获取当前datetime类型时间
    now_time = datetime.datetime.now()
    # 当前时间减去一天 获得昨天当前时间
    yes_time = now_time + datetime.timedelta(days=-1)
    # 格式化输出
    yes_time_str = yes_time.strftime('%Y-%m-%d %H:%M:%S')
    return (yes_time_str)  # 2017-11-01 22:56:02

def dif_time():
    # 使用datetime类型计算两个时间之间差值
    now_time = datetime.datetime.now()
    now_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
    d1 = datetime.datetime.strptime('2017-10-16 19:21:22', '%Y-%m-%d %H:%M:%S')
    d2 = datetime.datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    #间隔天数
    day = (d2 - d1).days
    #间隔秒数
    second = (d2 - d1).seconds
    print (day)   #17
    return (second)  #13475  注意这样计算出的秒数只有小时之后的计算额 也就是不包含天之间差数

def unix_time():
    #将python的datetime转换为unix时间戳
    dtime = datetime.datetime.now()
    un_time = time.mktime(dtime.timetuple())
    print (un_time)
    #将unix时间戳转换为python的datetime
    unix_ts = 1509636585.0
    times = datetime.datetime.fromtimestamp(unix_ts)
    return (times)  #2017-11-02 23:29:45

if __name__ == "__main__":
    get_time()
    dif_time()
