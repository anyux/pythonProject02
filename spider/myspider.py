import json
import os
import os.path as path
import re
#载入自动化测试工具
from selenium import webdriver
#载入异常
from selenium.common.exceptions import NoSuchElementException
#载入chrome选项
from selenium.webdriver import ChromeOptions
#载入数据类型
from typing import List, Dict

# 定义保存的json文件的文件名
FILE_NAME = "user.json"
# 设置爬虫的过程中是否显示浏览器，true - 显示，false - 不显示
IS_HEADLESS = False


class Spiders(object):
    def __init__(self, url: str, save_path: str):
        self.__url = url
        self.__save_path = save_path
        self.__result = list()

    def spider(self):
        """爬虫主程序，url:待爬取的链接，save_path:json 文件保存的目录"""
        # 新建浏览器对象
        #是否显示浏览器
        if not IS_HEADLESS:
            option = ChromeOptions()
            option.add_argument('--headless')
            browser = webdriver.Chrome(options=option)
        else:
            browser = webdriver.Chrome()

        # 尝试连接远程url
        try:
            browser.get(self.__url)
        #异常状态获取
        except Exception as err:
            print(f"get url:{self.__url} error:{err}")
        # 匹配查看按钮
        login_button = browser.find_element_by_xpath("//button[@id='login-btn' and @type='submit']")
        # 点击查看按钮
        login_button.click()
        # 如果想要快速的预览程序的效果，可以将下面一行代码取消注释，然后将爬取所有分页的数据那一部分的代码注释，这样就可以看到爬取单页时的效果
        #parse_users_page(browser, self.__result)

        # 爬取所有分页的数据（如果要看爬取单个页面的结果，注释下面的部分）
        while True:
            try:
                # 获取用户数据,并将数据写入到指定文件
                parse_users_page(browser, self.__result)
                # 获取下一页
                next_page_button = browser.find_element_by_xpath("//a[.='下一页']")
                # 点击下一页
                next_page_button.click()
            except NoSuchElementException:
                break
        # 爬取所有分页的数据
            # 保存数据
        data = {"users": self.__result}
        # 结果保存到指定的路径中
        save_json(data, self.__save_path)
        browser.close()

    def get_user_info(self, username: str):
        # 暴力遍历
        #如果结果为空,则返回
        if len(self.__result) == 0:
            print("还没爬取数据，无法查询")
            return
        #查询正则
        reg = f"{username}"
        #返回结果列表
        result = list()
        #正则查询
        for i in range(len(self.__result)):
            if re.search(reg, self.__result[i]["username"]) is not None:
                # 结果合并
                result.append(self.__result[i])
        # 返回结果
        return result

#处理用户页面
def parse_users_page(browser_d: webdriver.Chrome, result: List[Dict]):
    """处理 users 页面"""
    names = list()

    # 匹配当前页面中的 tr 节点，排除掉表格第一行的数据，剩余的数据格式：["id name info", "id name info"]
    trs = browser_d.find_elements_by_xpath("//tr")[1:]
    for tr in trs:
        name = tr.text.split(" ")[1]
        # 将名字添加到列表中
        names.append(name)
    # 匹配所有文本是”查看详细节点“的超链接
    info_buttons = browser_d.find_elements_by_xpath("//a[.='查看详细信息']")
    # 点击所有的超链接按钮，并处理
    for i in range(len(info_buttons)):
        # 点击用户详情页面
        info_buttons[i].click()
        # 开始处理用户详情页面
        parse_info_page(browser_d, result, names[i])
        # 处理完用户详情页之后返回到 users 页面
        browser_d.back()
        # 页面返回之后需要匹配所有文本是”查看详细节点“的超链接，因为之前的浏览器堆栈信息被改变了
        info_buttons = browser_d.find_elements_by_xpath("//a[.='查看详细信息']")


def parse_info_page(browser_d: webdriver.Chrome, result: List[Dict], name: str):
    """处理用户详情页"""
    # 匹配 tr 节点，排除掉表格第一行的数据，剩余的数据格式：["id country address job phone_number", "id country address job phone_number"]
    tr = browser_d.find_elements_by_xpath("//tr")[1:]
    for t in tr:
        infos = t.text.split(" ")
        data = {
            "id": infos[0],
            "username": name,
            "country": infos[1],
            "address": f"{infos[2]} {infos[3]}",
            "job": infos[4],
            "phone_number": infos[5],
        }
        result.append(data)


def save_json(data: dict, save_path: str):
    if not path.exists(save_path):
        os.makedirs(save_path)
    json_file_save_path = path.join(save_path, FILE_NAME)
    with open(json_file_save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"成功保存爬虫结果，结果文件位于:{path.abspath(json_file_save_path)}")


if __name__ == '__main__':
    s = Spiders("http://124.222.151.161:7777/", "./data")
    #https://www.yuque.com/docs/share/303138f8-e480-4495-a978-31bd2c7d14a0?#
    s.spider()
    print(s.get_user_info("兰"))
