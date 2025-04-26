import pandas as pd

list1={"A":[1,2,3],"B":[4,5,6]}
df1=pd.DataFrame(list1)
df=df1.to_html("daily_report.html")

with open(rf"D:\rp_test\rp.github.io") as f:
    f.write(df)