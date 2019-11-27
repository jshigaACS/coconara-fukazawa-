from itertools import groupby
import pandas as pd
df = pd.DataFrame()

df['sellprice']  =[10.0, 11.2,13.0]
df['shipcost'] = [0.0, 0.2,3.0]
df['viewurl'] = ['https://aaa', 'https://bbb', 'https://ccc']

new_df = pd.DataFrame()
new_dict = {}
for i, row in df.iterrows():
  print(i)
  print(row)
  print(row[0])
  print(row[1])
  new_dict['sellprice_'+str(i)] = row[0]
  new_dict['shippcost_' +str(i)] = row[1]
  print('^^^^^^^^')
#new_df['viewUrl'] = tuple(df['viewurl'])

a = pd.DataFrame(new_dict.values(),index=new_dict.keys()).T

a['itemType'] = 'refference'
a['itemid'] = 10001
a['url'] = ['https://aaa', 'https://bbb', 'https://ccc']
#b = {'url':['https://aaa', 'https://bbb', 'https://ccc']}
#c = a.update(b)
print(a)

