import re
import os

path = r'D:\BaiduNetdiskDownload'
def get_path(path):
    path = path
    os.chdir(path)
    mypath_list = os.listdir()
    for mypath in mypath_list:
        target_path = os.path.join(path,mypath)
        if os.path.isdir(target_path):
            rename_path(target_path)




def rename_path(mypath):
    path = r'D:\BaiduNetdiskDownload\第2章 K8s必备知识-Docker容器基础入门'
    path = mypath

    print(os.chdir(path))
    data_list = os.listdir()
    mycomplie = re.compile(r'(?P<name>.*)_D.*(?P<suffix>\.vep)')
    for data in data_list:
        mydata = mycomplie.search(data)
        if mydata is not None:
            try:
                os.rename(data,mydata['name']+mydata['suffix'])
            except:
                os.rename(data, mydata['name'] +'-2-'+ mydata['suffix'])
            print(data)
            print(mydata['name']+mydata['suffix'])

    data_list = os.listdir()
    print(data_list)



if __name__ == '__main__':
    get_path(path)