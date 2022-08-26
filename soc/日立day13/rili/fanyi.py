# -*-coding:utf-8-*-

'''
脚本读取txt文件中邮件内容，并在邮件基础上补充“建议事项”、“原因推测”、“是否攻击成功”相关信息，然后翻译成日文，将邮件发出

邮件样例：

Incident creation: 4552507 - (Alarmlevel3) Hong Kong Network-box HK18: Server SSH connection attempt:HSOC-(HCH)

告警ID: 4571182(4574804)
告警名称： MSSQL服务端口扫描
告警等级： 2
发生时间： 2020-04-12 21:50:49
告警设备： Shanghai Juniper FW 07(10.96.212.7)
告警内容： MSSQL服务端口扫描
告警时间： 2020-04-12 21:50:49
源IP： 58.187.9.166
目的IP： 210.5.30.21
源端口： 43027
目的端口： 1433
受影响设备： 210.5.30.21
事件描述： SQL Server对外提供服务端口
建议事项： 关闭闲置端口，更改默认端口，防火墙添加端口扫描规则等
原因推测： 通过日志分析，发现该源IP 58.187.9.166，尝试对服务器210.5.30.21的SQL server端口进行探测，并尝试建立连接
是否攻击成功： 否



警告ID: 4571182(4574804)
アラーム名：MSSQLサービスポートスキャン
アラームレベル： 2
発生時間： 2020-04-12 21:50:49
警報設備： Shanghai Juniper FW 07(10.96.212.7)
アラーム内容：MSSQLサービスポートスキャン
アラーム時間： 2020-04-12 21:50:49
ソースIP： 58.187.9.166
目的IP： 210.5.30.21
ソースポート： 43027
行き先ポート： 1433
影響を受ける設備： 210.5.30.21
イベントの説明：SQL Server対外サービスポート
提案事項：アイドルポートを閉じ、デフォルトポートを変更し、ファイアウォールにポートスキャン規則などを追加します
原因推定：ログ解析により、このソースIPが見つかりました58.187.9.166を選択します210.5.30.21のSQL serverポートを探知し、接続の確立を試みます
攻撃に成功しましたか：いいえ、

'''

import os
import xlrd
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import http.client
import hashlib
import urllib
import random
import json
import time
import re
import warnings

# 表格路径配置
# excelPath = "./告警规则说明_20200409.xlsx"
excelPath = "./告警规则说明_20200409.xls"

# 百度翻译配置
appid = '20210402000758476'  # 填写appid
secretKey = 'uA5hr4Ql522_O5fMvssf'  # 填写密钥
white_list = ['告警名称','事件描述','建议事项']
block_list = ['告警ID','告警等级','发生时间','告警设备','告警内容','告警时间','源IP','Hash','恶意对象','告警动作','告警原因','影响设备','来源IP']

def BaiduTransAPI(toLang, q):
    httpClient = None
    myurl = '/api/trans/vip/translate'

    fromLang = 'auto'  # 原文语种
    toLang = toLang  # 译文语种
    salt = random.randint(32768, 65536)
    q = q
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
        q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
        salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)

        # response是HTTPResponse对象
        response = httpClient.getresponse()

        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        return (result)
    except Exception as e:
        print(e)
        print(e)
    finally:
        if httpClient:
            httpClient.close()




def readTxt():
    count=0
    in_text = open('./mail2.txt', 'r', encoding="UTF-8-sig")
    for line in in_text.readlines():
        line = clear_space(line)
        print(line)
    print()
    print()
    in_text = open('./mail2.txt', 'r', encoding="UTF-8-sig")
    for line in in_text.readlines():
        line = clear_space(line)
        res = fanyi(line)
        print(res)

def clear_space(line):
    line = line.split('\n')[0]
    line = line.split('\r\n')[0]
    line = line.split('\r')[0]
    line = line.split('\r')[0]
    return line

def fanyi(line):
    my_data=''
    #print(line[0:4])
    if line[0:4]  in white_list:
        time.sleep(2)
        #print(line[0:4])
        data =BaiduTransAPI('jp', line)
        #print(data[])
        my_data = data['trans_result'][0]['dst']

    elif line[0:4] in block_list:
        #data = line[0:4] + line.split(line[0:4])[1]

        time.sleep(2)
        data = BaiduTransAPI('jp', line[0:4])
                #print(data['trans_result'][0]['dst'])
        my_data = data['trans_result'][0]['dst'] + line.split(line[0:4])[1]
        #print(my_data)
    my_data = clear_space(my_data)
    return my_data


def get_title():
    count=0
    in_text = open('./mail2.txt', 'r', encoding="UTF-8-sig")
    data = in_text.readlines()
    new_data = []
    for item in data:
        new_data.append(item.replace('：',':'))

    alarmID = new_data[0].split(':')[1].split('\n')[0].lstrip()
    alarmNameEN = BaiduTransAPI('en',new_data[1].split(':')[1].split('\n')[0].lstrip())['trans_result'][0]['dst']
    alarmLevel = new_data[2].split(':')[1].split('\n')[0].lstrip()
    alarmDevice = new_data[4].split(':')[1].split('\n')[0].lstrip()

    mailTitle = "Incident creation: " + alarmID + " - (Alarmlevel" + alarmLevel + ") " + alarmDevice + ": " + alarmNameEN + ":HSOC-(HCH)"
    print(mailTitle)
    print("邮件标题生成完成，开始翻译邮件正文为日文，翻译过程需要等待30秒左右...")






if __name__ == '__main__':
    get_title()
    # readTxt()