# -*- coding:utf-8 -*-
import json
import requests
from www import update_sql,unit_re,sale_event
#通路資訊
market_name='poya寶雅線上買'
goods_url='https://shop.cosmed.com.tw/SalePage/index/6890668'

#爬蟲資訊
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
url='https://www.poyabuy.com.tw/webapi/salepage/GetSalepageDataByIds?ids=7183451&v=0&shopId=40916&lang=zh-TW'
r = requests.get(url)
if r.status_code != requests.codes.ok:
    print(f'網頁載入發生問題：{url}')
data=r.text
data = json.loads(data)
goods_title=data['SalepageList'][0]['Title']
goods_price=data['SalepageList'][0]['Price']
print(goods_title,goods_price)
unit_num=unit_re(goods_title)
sales10='none'
sales10,unit_num=sale_event(goods_title,unit_num)
print(unit_num)

#寫入資料庫
update_sql(market_name, goods_price, unit_num,sales10,url)

market_list=[market_name , goods_price , unit_num , round(goods_price/unit_num,2),sales10]
print(market_list)     
