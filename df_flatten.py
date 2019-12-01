from itertools import groupby
import pandas as pd

df = pd.DataFrame(inde)

sell_price

df['sellprice']  =[10.0, 11.2,13.0]
df['shipcost'] = [0.0, 0.2,3.0]
df['viewurl'] = ["https://aaa", "https://bbb", "https://ccc"]
print(df)

new_dict = {}
for i, row in df.iterrows():
  print(i)
  print(row)
  print(row[0])
  print(row[1])
  new_dict['sellprice_'+str(i)] = row[0]
  new_dict['shippcost_' +str(i)] = row[1]
  new_dict['url_'+str(i)] = row[2]
  print('^^^^^^^^')

a = pd.DataFrame(new_dict.values(),index=new_dict.keys()).T
print(a)
