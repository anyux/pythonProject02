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

# 表格路径配置
# excelPath = "./告警规则说明_20200409.xlsx"
excelPath = "./告警规则说明_20200409.xls"

# 百度翻译配置
appid = '20210402000758476'  # 填写appid
secretKey = 'uA5hr4Ql522_O5fMvssf'  # 填写密钥

'''
readTxt读取文本中邮件正文，然后进行中文冒号替换，替换完成后邮件正文转换为字典，新增“建议事项” “原因推测” “是否攻击成功” 字段内容
'''

# 定义空字典，用于存储邮件内容
dict_items = {}
dict_itemsTrans = {}


def readTxt():
    in_text = open('./mail2.txt', 'r', encoding="UTF-8-sig")
    for line in in_text.readlines():
        if line == '\r\n':
            pass
        elif line == '\n':
            pass
        else:
            # 替换成英文符号
            line = txtEdit(line)
            # 去空格
            line = line.strip()
            strToDict(line)
    print("开始格式化txt邮件正文")

    mailContentEdir(dict_items['告警名称'])
    print(dict_items)

    print("邮件正文格式化完成，开始生成邮件标题")
    # 邮件标题翻译 Incident creation: 4557824 - (Alarmlevel2) Shanghai Juniper FW 07: MSSQL service port scan:HSOC-(HCH)
    q = str(dict_items['告警名称']).strip()

    response = BaiduTransAPI('en', q)
    print(response);
    alarmNameEN = response['trans_result'][0]['dst']

    print(dict_items)
    alarmID = str(dict_items['告警ID']).strip()
    # 去掉alarmID中括号的内容
    alarmID = re.sub(u"\\(.*?\\)", "", alarmID)

    alarmLevel = str(dict_items['告警等级']).strip()

    ##去掉alarmDevice中括号的内容
    alarmDevice = str(dict_items['告警设备']).strip()
    alarmDevice = re.sub(u"\\(.*?\\)", "", alarmDevice)

    # 拼接邮件标题
    mailTitle = "Incident creation: " + alarmID + " - (Alarmlevel" + alarmLevel + ") " + alarmDevice + ": " + alarmNameEN + ":HSOC-(HCH)"
    print(mailTitle)
    print("邮件标题生成完成，开始翻译邮件正文为日文，翻译过程需要等待30秒左右...")

    # 邮件正文翻译
    time.sleep(2)

    '''
    q = ""
    for dictKey in dict_items.keys():
        if q.strip() == "":
            q = dictKey +":" + dict_items[dictKey] + "\n"
        else:
            q = q + dictKey + ":" + dict_items[dictKey] + "\n"

    print(q)
    mailbody = BaiduTransAPI('jp',q)
    print(mailbody)
    print(mailbody['trans_result'])
    '''
    q = ""
    for dictKey in dict_items.keys():
        if q.strip() == "":
            q = dictKey + "\n"
        else:
            q = q + dictKey + "\n"

    #    print(q)
    mailbody = BaiduTransAPI('jp', q)
    print(mailbody)
    #    print(mailbody['trans_result'])
    itemTransLen = len(mailbody['trans_result'])
    print(itemTransLen)
    itemTrans = mailbody['trans_result']
    for itemNum in range(itemTransLen):
        dictTransKey = itemTrans[itemNum]['dst']
        time.sleep(1)
        if itemTrans[itemNum]['src'] == '告警名称':
            q = dict_items[itemTrans[itemNum]['src']]
            response = BaiduTransAPI('jp', q)

            dictTransValue = response["trans_result"][0]['dst']
        #            print(dictTransValue)
        elif itemTrans[itemNum]['src'] == '告警内容':
            q = dict_items[itemTrans[itemNum]['src']]
            response = BaiduTransAPI('jp', q)
            dictTransValue = response["trans_result"][0]['dst']
        #            print(dictTransValue)
        elif itemTrans[itemNum]['src'] == '事件描述':
            q = dict_items[itemTrans[itemNum]['src']]
            print(q)
            # exit()
            response = BaiduTransAPI('jp', q)
            # time.sleep(1)

            dictTransValue = response["trans_result"][0]['dst']
        #            print(dictTransValue)
        elif itemTrans[itemNum]['src'] == '建议事项':
            q = dict_items[itemTrans[itemNum]['src']]
            #            print(q)
            # 按照{src_ip}|{dst_ip}|{src_port}|{dst_port}进行分隔，然后分隔后的内容翻译为日文，然后拼接上{src_ip}|{dst_ip}|{src_port}|{dst_port}对于的分隔符号，最后替换分隔符的内容
            strList = re.split('({src_ip}|{dst_ip}|{src_port}|{dst_port})', q)
            #            print(strList)
            str1 = "" \
                   ""
            for strItem in strList:
                time.sleep(1)
                if strItem in ["{src_ip}", "{dst_ip}", "{src_port}", "{dst_port}"]:
                    str1 = str1 + strItem
                else:
                    response = BaiduTransAPI('jp', strItem)
                    #                    print(response)
                    str1 = str1 + str(response["trans_result"][0]['dst']).replace("。", "")
            dictTransValue = ipportReplace(str1)

        elif itemTrans[itemNum]['src'] == '原因推测':
            print(itemTrans[itemNum]['src'])
            q = dict_items[itemTrans[itemNum]['src']]

            # 按照{src_ip}|{dst_ip}|{src_port}|{dst_port}进行分隔，然后分隔后的内容翻译为日文，然后拼接上{src_ip}|{dst_ip}|{src_port}|{dst_port}对于的分隔符号，最后替换日文中分隔符的内容
            strList = re.split('({src_ip}|{dst_ip}|{src_port}|{dst_port})', q)
            str2 = ""
            for strItem in strList:
                time.sleep(1)
                if strItem in ["{src_ip}", "{dst_ip}", "{src_port}", "{dst_port}"]:
                    str2 = str2 + strItem
                else:
                    response = BaiduTransAPI('jp', strItem)
                    str2 = str2 + str(response["trans_result"][0]['dst']).replace("。", "")
            dictTransValue = ipportReplace(str2)
        #            print(dictTransValue)

        elif itemTrans[itemNum]['src'] == '是否攻击成功':
            q = dict_items[itemTrans[itemNum]['src']]
            response = BaiduTransAPI('jp', q)
            dictTransValue = response["trans_result"][0]['dst']
        #            print(dictTransValue)
        else:
            dictTransValue = dict_items[itemTrans[itemNum]['src']]
        dict_itemsTrans[dictTransKey] = dictTransValue

    # 替换中文分隔符{src_ip}|{dst_ip}|{src_port}|{dst_port}为对应的IP和端口
    print(dict_items)
    dict_items['建议事项'] = ipportReplace(dict_items['建议事项'])
    dict_items['原因推测'] = ipportReplace(dict_items['原因推测'])

    #    print(dict_itemsTrans)
    print("邮件正文翻译完成...")

    '''
    for m in ["告警名称","告警内容","事件描述","建议事项","原因推测","是否攻击成功"]:
        print (m)
        q = dict_items[m]
        response = BaiduTransAPI('jp', q)
        dict_items
    '''


'''
邮件中，中文冒号替换为英文冒号
'''


def txtEdit(line):
    colonC = '：'
    colonE = ': '
    res = colonC in line
    #    print(res)
    if res is True:
        line = line.replace(colonC, colonE)
    return (line)


'''
邮件转换为字典格式，然后新增“建议事项” “原因推测” “是否攻击成功” 字段内容
'''


def strToDict(line):
    lineKey = line.split(':')[0]
    lineValue = line.split(':')[1:]

    # 可能存在多个英文冒号，因此需要进行拼接
    valueNum = len(lineValue)
    if valueNum > 1:
        strValue = ":".join(map(str, lineValue))
        dict_items[lineKey] = strValue
    else:
        strValue = ''.join(map(str, lineValue))
        dict_items[lineKey] = strValue


def mailContentEdir(alarmName):
    # 增加“建议事项” “原因推测” “是否攻击成功” 字段内容，更新dict_items中“建议事项”的内容

    workBook = xlrd.open_workbook(excelPath);
    sheet = workBook.sheet_by_index(0)

    alarmName = alarmName
    alarmCols = sheet.ncols
    alarmnrows = sheet.nrows
    for alarmNameNum in range(1, alarmnrows):
        alarmItem = sheet.row_values(alarmNameNum)
        #        print (str(alarmItem[0]))
        #        print(str(alarmItem[12]))
        #        print(str(alarmItem[13]))

        # alarmItem[0]是excel表中告警名称，alarmName是邮件中告警名称
        if str(alarmItem[0]).encode("utf-8").strip() == str(alarmName).encode("utf-8").strip():
            # 替换原因推测中五元组信息
            src_ip = dict_items['源IP'].strip()
            dst_ip = dict_items['目的IP'].strip()
            src_port = dict_items['源端口'].strip()
            dst_port = dict_items['目的端口'].strip()

            '''
            s = str(alarmItem[13])
            s = s.replace('{src_ip}',src_ip)
            s = s.replace('{dst_ip}', dst_ip)
            s = s.replace('{src_port}', src_port)
            s = s.replace('{dst_port}', dst_port)
            '''
            dict_items['建议事项'] = ' ' + str(alarmItem[12])
            # dict_items['原因推测'] = ' ' + s
            dict_items['原因推测'] = ' ' + str(alarmItem[13])
            dict_items['是否攻击成功'] = ' 否'


#        else:
#            print("不等")


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


def ipportReplace(s):
    # 替换原因推测中五元组信息
    src_ip = dict_items['源IP'].strip()
    dst_ip = dict_items['目的IP'].strip()
    src_port = dict_items['源端口'].strip()
    dst_port = dict_items['目的端口'].strip()

    s = s
    s = s.replace('{src_ip}', src_ip)
    s = s.replace('{dst_ip}', dst_ip)
    s = s.replace('{src_port}', src_port)
    s = s.replace('{dst_port}', dst_port)
    return s


if __name__ == '__main__':
    readTxt()

    #    print(dict_items)
    #    print(dict_itemsTrans)

    dictItemPrint = ""
    for dictKey in dict_items.keys():
        if dictItemPrint.strip() == "":
            dictItemPrint = dictKey + ":" + dict_items[dictKey] + "\n"
        else:
            dictItemPrint = dictItemPrint + dictKey + "：" + dict_items[dictKey] + "\n"
    print(dictItemPrint)

    print("\n")

    dictItemTransPrint = ""
    for dictKey in dict_itemsTrans.keys():
        if dictItemTransPrint.strip() == "":
            dictItemTransPrint = dictKey + ":" + dict_itemsTrans[dictKey] + "\n"
        else:
            dictItemTransPrint = dictItemTransPrint + dictKey + "：" + dict_itemsTrans[dictKey] + "\n"
    print(dictItemTransPrint)
