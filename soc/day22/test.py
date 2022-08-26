import re

mypattern=r'^(?P<time>[A-Z][a-z]{2} {1,2}\d{1,2} \d{2}:\d{2}:\d{2}) (?P<host>[0-9a-zA-Z_-]*) (?P<process>[/0-9a-zA-Z_-]*\[?\d{0,9}\]?): (?P<message>.*)$'
mycompile = re.compile(mypattern)

count=0

with open('messages.log', 'r', encoding='utf-8') as f:
    for data in f.readlines():
        mydata = mycompile.search(data)
        if mydata is None:
            print(data,'======')
            exit()
            continue
        data = mydata.groupdict()
        count +=1
        print(data)
    print(count)



