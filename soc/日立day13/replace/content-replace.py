import os

os.getcwd()
os.chdir(r'E:\pythonProject02\soc\日立day13\replace')

def my_replace(data):
    return data.replace("，",",")\
        .replace("）",")")\
        .replace("（","(")\
        .replace("\n","")\
        .replace("：",":")\
        .replace("。",".")\
        .replace(": //","://")\
        .replace(": <",":<")\
        .replace("、",",")\
        .replace("；",";")\
        .replace("“", "\"")\
        .replace("”","\"")\
        .replace(". ",".\n\n")\
        .replace(", ",",")\
        .replace("( ","(")\
        .replace("？","?")


with open('content2.txt', 'w',encoding='utf8') as f2:

    with open('content.txt','r',encoding='utf8') as f1:
        for item in f1:
            print(my_replace(item),end='',file=f2)

os.remove('content.txt')
os.renames('content2.txt','content.txt')