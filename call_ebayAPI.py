#!/usr/bin/python3.5
# -*- coding: utf-8 -*-

import sys
import json
import requests
from xml.dom.minidom import parse,parseString
import jmespath
from pandas.io.json import json_normalize
import pandas as pd
from collections import OrderedDict
import io


"""
[機能概要]
 1. function.jsよりCallされる
 2. function.jsより引き渡されたパラメータ（JAN etc., )を受ける
 3. 受けた引数をパラメータにebay-apiをCall
 4. response-jsonをjsに返す＿＿
"""
#receive params
file_name = sys.argv[1]
file_data = sys.argv[2]
#cond = 1 #1:used, 0:new
cond = int(sys.argv[3])

item_id_lists = {
    'ReferenceID':'153299370',
    #'ReferenceID':'9780764311222',
    #'ISBN':'9780764311222',
    #'UPC':'793389361342',
    #'EAN':'9780764311222'
}


if cond == 1:#used
  condition_param = 3000
  cond_name = 'Used'

else:#new
  condition_param = 1000
  cond_name = 'New'


#findProduct

#api-call(findItemsByProduct)

dev_id = '8e15105d-93a7-4506-9fbe-2bea951c626b'
operation_name = 'findItemsByProduct'
response_name = 'findItemsByProductResponse'
app_id = 'junshiga-Forcocon-PRD-340728b69-97233dce'

base_url = 'https://svcs.ebay.com/services/search/FindingService/v1?'


def buildRequestsURL(type_, item_id):
    if  condition_param == 3000: #used
        value_1 = 4000
        value_2 = 5000

    else:#new
        value_1 = 2000
        value_2 = 2500

    params = OrderedDict()
    params['OPERATION-NAME'] = operation_name
    params['SERVICE-VERSION'] = '1.13.0'
    params['SECURITY-APPNAME'] = app_id
    params['MESSAGE-ENCODING'] = 'UTF-8'
    params['RESPONSE-DATA-FORMAT'] = 'JSON'
    params['REST-PAYLOAD'] = 'true'
    params['paginationInput.entriesPerPage'] = 1000
    params['productId.@type'] = type_
    params['productId'] = item_id
    params['sortOrder'] = 'PricePlusShippingLowest'
    params['itemFilter(0).name'] = 'Condition'
    params['itemFilter(0).value(0)'] = cond_name
    params['itemFilter(0).value(1)'] = value_1
    params['itemFilter(0).value(2)'] = value_2
    params['itemFilter(1).name'] = 'ListingType'
    params['itemFilter(1).value(0)'] = 'AuctionWithBIN'


    r = requests.get(base_url,params=params)
    #r = requests.post(base_url,data=params)

    return r

def setting():
    get_params = OrderedDict()
    base_depth_sRes = 'findItemsByProductResponse[].searchResult[].item[]'

    get_viewItemUrl = '{}.viewItemURL[]'.format(base_depth_sRes)
    get_shipCostS = '{}.shippingInfo[].shippingServiceCost[].__value__'.format(base_depth_sRes)   
    get_pid = '{}.productId[].__value__'.format(base_depth_sRes)
    get_sellPrice = '{}.sellingStatus[].currentPrice[].__value__'.format(base_depth_sRes)
    get_shippingType = '{}.shippingInfo[].shippingType[]'.format(base_depth_sRes)

    get_params ={
        "itemId":get_pid,
        "sellPrice":get_sellPrice,
        "shippingCost":get_shipCostS,
        "shippingType":get_shippingType,
        "viewItemUrl":get_viewItemUrl
    }

    return get_params


def format_df(df,cnt):
    rows_num = len(df)

    
    df['condition'] = [cond_name for i in range(rows_num)]
    df['currencyID'] = ['USD' for i in range(rows_num)]
    df = df[['code_type','itemId','condition','currencyID','sellPrice','shippingType','shippingCost','viewItemUrl']]

    new_dict = OrderedDict()
    for i, row in df.iterrows():
        #print(row[0])
        #print(row[1])
        #print(row[2])
        #print(row[3])
        #print(row[4])
        
        new_dict['code_type_'+str(i)] = row[0]
        new_dict['itemId_'+str(i)] = row[1]
        new_dict['condition_'+str(i)] = row[2]
        new_dict['currencyID_'+str(i)] = row[3]
        new_dict['sellPrice'+str(i)] = row[4]
        new_dict['shippingType_'+str(i)] = row[5]
        new_dict['shippingCost_' +str(i)] = row[6]
        new_dict['viewItemUrl_'+str(i)] = row[7]

    new_dict['count'] = cnt
    rt_df = pd.DataFrame(new_dict.values(),index=new_dict.keys()).T
    
    #きれいな要望通りのjson形式にそろえる
    return rt_df



r = buildRequestsURL(file_name, file_data)

if str(r.status_code) != '500':
    json_dict = json.loads(r.text)

    #print(json_dict)
    return_df = pd.DataFrame()
    return_df['code_type'] = [file_name for i in range(3)]    
    
    try:
        judge_ok = json_dict[response_name][0]['ack']

        #通信の確認
        if 'Success' in judge_ok:
            count_num = json_dict[response_name][0]['searchResult'][0]['@count']
            #print(count_num)         
            #成功カウント数の確認
            if 1 <= int(count_num):

                params = setting()

                for key,val in params.items():

                    #if val == 'findItemsByProductResponse[].searchResult[].item[]':#.conditionDisplayName':
                    res_list = jmespath.search(val,json_dict)
                    lower_3_list = res_list[:3]#上位三件を取得
                    lower_3_series = pd.Series(lower_3_list)#Series化

                    return_df[key] = lower_3_series

                
                rtn_df = format_df(return_df,count_num) #すべてのカラムがそろっていないから

            #else:
            #print('connect:OK, count:zero')
    

    except Exception as e:
        print(e)
        print('exception-occured') 
        print(1)

    else:#end try

        #print(return_df)        
        #return_df.to_csv('/home/ubuntu/coconara/'+'rtn_'+file_name+'.csv',sep=',',index=False)
        print(rtn_df.to_csv(sep=',',index=False,header=False),end="")

else:#server error
    print('internal server error:500')
    #print(r.url)
