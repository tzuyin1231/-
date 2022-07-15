# -*- coding:utf-8 -*-
import json
import requests
from www import update_sql,unit_re,sale_event
#通路資訊
market_name='pchome'
goods_url='https://24h.pchome.com.tw/prod/DAAB22-A900B8P97'#商品購買網頁

#爬蟲資訊
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36'}
url='https://ecapi.pchome.com.tw/ecshop/prodapi/v2/prod/'
product_id='DAAB22-A900B8P97'
fields='Name,Price'
url += product_id
url += '&fields={}'.format(fields)
url += '&_callback=jsonp_prod'

r = requests.get(url)
if r.status_code != requests.codes.ok:
    print(f'網頁載入發生問題：{url}')
data=r.text
data = json.loads(data[15:-48])#加這行出來的才是中文不知為何#去除前後 JS 語法字串[15:-48]
#print(data)
goods_title=data['{}-000'.format(product_id)]['Name']
goods_price=data['{}-000'.format(product_id)]['Price']['P']

unit_num=unit_re(goods_title)
sales10='none'
sale_event(goods_title,unit_num)

#寫入資料庫
update_sql(market_name,goods_title, goods_price, unit_num,sales10,url)

#顯示執行結果
market_list=[market_name , goods_price , unit_num , round(goods_price/unit_num,2),sales10]
print(market_list)     
