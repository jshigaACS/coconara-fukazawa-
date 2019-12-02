from itertools import groupby
import pandas as pd

df = pd.DataFrame()

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

    """
    params = {
        #'SERVICE-NAME':'FindingService',
        'OPERATION-NAME':operation_name,
        'SERVICE-VERSION':'1.13.0',
        'SECURITY-APPNAME': app_id,
        #'GLOBAL-ID':0,
        'MESSAGE-ENCODING': 'UTF-8',
        'RESPONSE-DATA-FORMAT': 'JSON',
        'REST-PAYLOAD':True,
        'paginationInput.entriesPerPage':1000,#Responseする件数：10件分のJsonoデータ取得
        'productId.@type': type_,
        'productId': item_id,
        'sortOrder':'PricePlusShippingLowest',
        #'itemFilter(0).name':'FreeShippingOnly',#,calculatedが含まれるため、cost-カラムが存在しないケースがある
        #'itemFilter(0).value':False,
        'itemFilter(0).name':'Condition',#可変
        'itemFilter(0).value(0)':cond_name,#condition_param,
        'itemFilter(0).value(1)':value_1,
        'itemFilter(0).value(2)':value_2,
        'itemFilter(1).name':'ListingType',#可変
        'itemFilter(1).value(0)':'AuctionWithBIN',
    }    
    """