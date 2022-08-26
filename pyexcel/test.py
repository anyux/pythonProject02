import pandas as pd
mydata1 = {
    '公司':['恒盛', '创锐', '快学'],
    '分数':[90, 95, 85]
}
mydata2 = {
    '公司':['恒盛', '创锐', '惊喜'],
    '股价':[20, 180, 30]
}
df1 = pd.DataFrame(mydata1)
df2 = pd.DataFrame(mydata2)

df3 = pd.merge(df1, df2, left_index=True, right_index=True)
print(df3)

#return
