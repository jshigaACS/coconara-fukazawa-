# -*- coding: utf-8 -*-
import sys
#sys.stdout.write("Content-type: application/json; charset=utf-8")
#sys.stdout.write("Content-type: text/plain; charset=utf-8")
#sys.stdout.write("Access-Control-Allow-Origin: *\r\n\r\n")
#sys.stdout.write("Content-Type: application/json\n")
#sys.stdout.write("\n")
#sys.stdout.write('hellow')
print ("Content-Type: text/plain\r\n")
print ("Access-Control-Allow-Origin: *\r\n")
print('hello')
import json

import requests
from xml.dom.minidom import parse,parseString
import jmespath
from pandas.io.json import json_normalize
import pandas as pd
from collections import OrderedDict
import io
from wsgiref.simple_server import make_server
from app import RequestHandler
"""
[機能概要]
 1. function.jsよりCallされる
 2. function.jsより引き渡されたパラメータ（JAN etc., )を受ける
 3. 受けた引数をパラメータにebay-apiをCall
 4. response-jsonをjsに返す＿＿
"""
#receive params
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
#data = sys.stdin.read()
#argvs = json.loads(data)


    #print('okだよ')

"""
file_data_cnt = len(file_data)



item_id_lists = {
    'ReferenceID':'153299370',
    #'ReferenceID':'9780764311222',
    #'ISBN':'9780764311222',
    #'UPC':'793389361342',
    #'EAN':'9780764311222'
}

cond = 1 #1:used, 0:new

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


    get_params ={
        "itemId":get_pid,
        "sellPrice":get_sellPrice,
        "shippingCost":get_shipCostS,
        "viewItemUrl":get_viewItemUrl
    }

    return get_params


def format_df(df):
    rows_num = len(df)

    
    df['condition'] = [cond_name for i in range(rows_num)]
    df['currencyID'] = ['USD' for i in range(rows_num)]
    df = df[['itemId','condition','sellPrice','shippingCost','viewItemUrl']]

    #きれいな要望通りのjson形式にそろえる
    return df


for code_type, i_id in item_id_lists.items():

    r = buildRequestsURL(code_type, i_id)

    if str(r.status_code) != '500':
        json_dict = json.loads(r.text)

        #print(json_dict)
        return_df = pd.DataFrame()
        return_df['code_type'] = [code_type for i in range(3)]    
        
        try:
            judge_ok = json_dict[response_name][0]['ack']

            #通信の確認
            if 'Success' in judge_ok:
                count_num = json_dict[response_name][0]['searchResult'][0]['@count']
                
                #成功カウント数の確認
                if 1 <= int(count_num):

                    params = setting()

                    for key,val in params.items():

                        #if val == 'findItemsByProductResponse[].searchResult[].item[]':#.conditionDisplayName':
                        res_list = jmespath.search(val,json_dict)
                        lower_3_list = res_list[:3]#上位三件を取得
                        lower_3_series = pd.Series(lower_3_list)#Series化

                        return_df[key] = lower_3_series

                    
                    return_df = format_df(return_df) #すべてのカラムがそろっていないから

                else:
                    print('connect:OK, count:zero')
        

        except Exception as e:
            print(e)
            print('exception-occured') 
            print(1)

        else:#end try
            print('正常に終了しました')

            print(return_df.to_json())
        

    else:#server error
        print('internal server error:500')
        print(r.url)
"""