import os
import sys
import getopt
import time



def get_vm_detail():
    opts, args = getopt.getopt(sys.argv[0:], 'n:c:core:mem', ['name',"cpunum","corenum","memory"])
    print(opts)
    if len(args) <9:
        print("please check args, ths args too less!!!")
        time.sleep(10)
        exit(1)
    if not args[2] == '':
        return args[2],args[4],args[6],args[8]


vm_detail = get_vm_detail()
name = vm_detail[0]

inputlist = ['numvcpus', 'cpuid.coresPerSocket', 'memsize']

# numvcpus(处理器数量) * cpuid.coresPerSocket(处理器内核数量) =  处理器内核总数
# 4 * 2 = 8
# memize 8192 8192MB = 8G
inputdick = {}
inputdick.setdefault(inputlist[0],vm_detail[1])
inputdick.setdefault(inputlist[1],vm_detail[2])
inputdick.setdefault(inputlist[2],str(int(vm_detail[3])*1024))
#打印配置信息与vm名称
print(inputdick)
print(name)


mypath = r'E:\Virtual-Machines\{}\{}.vmx'.format(name, name)




# 修改文件内容
# path : 文件名称
def edit_file_content(path):
    if not os.access(path, os.R_OK):
        print("{} file is cloudt not read!!!please check file attribute".format(path))
        exit(999)
    # 切换目录到指定目录
    os.chdir(os.path.dirname(path))
    # 指定打开文件编码f1只读,f2只写
    with open(path, 'r', encoding='GBK') as f1, \
            open("%s.bak".format(path), "w", encoding="GBK") as f2:
        for line in f1.readlines():
            # print(line)
            if line.split('=')[0].strip() not in inputlist:
                print(line.split('=')[0].strip())
                print(line)
                f2.write("{}".format(line))
        for item in inputlist:
            myinput = '{} = "{}"'.format(item, inputdick[item])
            f2.write("{}\n".format(myinput))

    os.remove(path)
    os.rename("%s.bak".format(path), path)


if __name__ == '__main__':
    edit_file_content(mypath)
