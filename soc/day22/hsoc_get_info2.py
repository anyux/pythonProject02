import json
import re

csvName= '2021-11.csv'
logName= '2021-11.log'

def my_replace(line):
    line = line.replace('\\\\','\\')
    line = line.replace('\\\\', '\\')
    return line

def get_asset():
    lines=0
    count = 0
    badcount=0
    mypattern = r'.*event@\d{5}\s{1}p1=\\\"(?P<hash>.*)\\\"\s{1}' \
                r'p2=\\\"(?P<fileName>.*)\\\"\s{1}p5=\\\"(?P<alarmReason>.*)\\\"\s{1}' \
                r'p7=\\\"(?P<user>.*)\\\"\s{1}p8=\\\"(?:.*)\\\"\s{1}p9=\\\"(?:.*)\\\"\s{1}' \
                r'et=\\\"(?P<alarmDescription>.*)\\\"\s{1}tdn=\\\"(?P<alarmAction>.*)\\\"\s{1}' \
                r'etdn=\\\"(?P<alarmBeahaivor>.*)\\\"\s{1}hdn=\\\"(?P<hostName>.*)\\\"\s{1}' \
                r'hip=\\\"(?P<hostIp>.*)\\\"\sgn.*'
    titleName = 'hash,fileName,alarmReason,user,alarmDescription,alarmAction,alarmBeahaivor,hostName,hostIp'
    mycompile = re.compile(mypattern)
    with open(csvName, 'a', encoding='gbk') as f2:
        print(titleName, sep=',', end=',', file=f2)
        print('', file=f2)
        with open(logName, 'r', encoding='utf-8') as f:
            for data in f.readlines():
                lines = lines + 1

                if mycompile.search(data):
                    print('第%s行获取内容' % lines,end=': ')
                    mydata = mycompile.search(data)
                    data = mydata.groupdict()
                    data['fileName'] = my_replace(data['fileName'])
                    data['user'] = my_replace(data['user'])
                    writeline= ''
                    for item in data.values():
                        writeline = writeline+item+','
                    print(writeline)
                    print(writeline, sep=',', end=',', file=f2)
                    print('', file=f2)
                    count = count + 1
                else:
                    print('第%s行获取内容: ' % lines ,end=':')
                    badcount = badcount + 1
                    print(data)

    print(logName,'总行数为:',lines)
    print(csvName,'写放行数为:',count)
    print('未找到匹配告警行数为:',badcount)


if __name__ == '__main__':
    get_asset()
