# -*- coding:utf-8 -*-
import json
import requests
import re
import pymysql
from datetime import datetime

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
data = json.loads(data[15:-48])#加這行出來的才是中文不知為何#去除前後 JS 語法字串
print(data)
goods_title=data['{}-000'.format(product_id)]['Name']
goods_price=data['{}-000'.format(product_id)]['Price']['P']
result=re.findall('(\d+)片',goods_title)+re.findall('(\d+)PC',goods_title)+re.findall('(\d+)包',goods_title)+re.findall('(\d+)入',goods_title)
unit_num=1
sales10='none'
for i in result:
    unit_num*=int(i)
print(unit_num)
 
#連接mysql資料庫
db = pymysql.connect(host='localhost',
                    user='testuser',
                    password='test123',
                    database='project1')
#建立操作游標
cursor = db.cursor()

all_markets=[]
col=['通路名稱','商品價格','商品單位','單位價格','促銷活動有無']
market_list=[]
market_name='pchome'

    

        # #將資料寫入sofy_pad_29資料表
inserting_sql = """
                INSERT INTO goods_pricing_sofy_pad_29
                (market_name,goods_price,goods_num,unit_price,sale_activity)
                VALUES ('{}',{},{},{},'{}')
                ON DUPLICATE KEY UPDATE
                goods_price={},goods_num={},unit_price={},sale_activity='{}',timestamp='{}'
                """.format(
                market_name , goods_price , unit_num , round(goods_price/unit_num,2),sales10,
                goods_price , unit_num , round(goods_price/unit_num,2),sales10,datetime.now())
        
# 執行sql
cursor.execute(inserting_sql)
# 提交到sql中執行
db.commit() 
db.close()

market_list=[market_name , goods_price , unit_num , round(goods_price/unit_num,2),sales10]
print(market_list)     
