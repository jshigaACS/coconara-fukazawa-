# -*- coding: utf-8 -*-
import json
import sys
import requests
from xml.dom.minidom import parse,parseString
import jmespath
from pandas.io.json import json_normalize
import pandas as pd
from collections import OrderedDict
"""
[機能概要]
 1. function.jsよりCallされる
 2. function.jsより引き渡されたパラメータ（JAN etc., )を受ける
 3. 受けた引数をパラメータにebay-apiをCall
 4. response-jsonをjsに返す
"""

#receive params
#item_id_lists = json.loads(data)
#data = sys.stdin.read()

item_id_lists = {
    'ReferenceID':'153299370',
    'ISBN':'372840793269',
    'UPC':'786936834321',
    'EAN':'0889136068074'
}

#findProduct
#http://open.api.ebay.com/shopping?callname=FindProducts&responseencoding=JSON&appid=junshiga-Forcocon-PRD-340728b69-97233dce&siteid=0&version=967&QueryKeywords=The+Little+Mermaid&AvailableItemsOnly=true&MaxEntries=2

#https://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByProduct&SERVICE-VERSION=1.0.0&SECURITY-APPNAME=junshiga-Forcocon-PRD-340728b69-97233dce&RESPONSE-DATA-FORMAT=XML&REST-PAYLOAD&paginationInput.entriesPerPage=2&productId.@type=ReferenceID&productId=53039031

#api-call(findItemsByProduct)

dev_id = '8e15105d-93a7-4506-9fbe-2bea951c626b'
operation_name = 'findItemsByProduct'
response_name = 'findItemsByProductResponse'
app_id = 'junshiga-Forcocon-PRD-340728b69-97233dce'

base_url = 'https://svcs.ebay.com/services/search/FindingService/v1?'

def buildRequestsURL(type_, item_id):
    params = {
        #'SERVICE-NAME':'FindingService',
        'OPERATION-NAME':operation_name,
        'SERVICE-VERSION':'1.12.7',
        'SECURITY-APPNAME': app_id,
        #'GLOBAL-ID':0,
        'MESSAGE-ENCODING': 'UTF-8',
        'RESPONSE-DATA-FORMAT': 'JSON',
        'REST-PAYLOAD':True,
        'paginationInput.entriesPerPage':1000,#Responseする件数：10件分のJsonoデータ取得
        'productId.@type': type_,
        'productId': item_id,
        'sortOrder':'PricePlusShippingLowest',
        'itemFilter(0).name':'Condition',
        'itemFilter(0).value':1000,
    }    
    #'itemFilter(1).name':'FreeShippingOnly',
    #'itemFilter(1).value':False,
    
    r = requests.get(base_url,params=params)

    return r

def setting():
    get_params = OrderedDict()
    base_depth_sRes = 'findItemsByProductResponse[].searchResult[].item[]'
    get_viewItemUrl = '{}.viewItemURL[]'.format(base_depth_sRes)
    get_shipCostS = '{}.shippingInfo[].shippingServiceCost[].__value__'.format(base_depth_sRes)   
    get_pid = '{}.productId[].__value__'.format(base_depth_sRes)
    get_sellPrice = '{}.sellingStatus[].currentPrice[].__value__'.format(base_depth_sRes)    

    get_params["itemId"] = get_pid #code_type挿入
    #"CurrencyId":get_sellPriceCId,#決めうち USD
    get_params["sellPrice"] = get_sellPrice
    get_params["shippingCost"] = get_shipCostS
    get_params["viewItemUrl"] = get_viewItemUrl     

    return get_params

for code_type, i_id in item_id_lists.items():

    r = buildRequestsURL(code_type, i_id)

    if str(r.status_code) != '500':
        json_dict = json.loads(r.text)

        #print(json_dict)
        return_df = pd.DataFrame()
        #col=code_type, 
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
                        
                        #if val == 'findItemsByProductResponse[].searchResult[].item[].productId[]':
                        res_list = jmespath.search(val,json_dict)

                        lower_3_list = res_list[:3]#上位三件を取得
                        return_df[key] = lower_3_list


                else:
                    print('connect:OK, count:zero')


        except Exception as e:
            print(e)
            print('connection-error') 
            print(1)

        else:
            print('正常に終了しました')
            print(return_df)

    else:
        print('internal server error:500')