import requests
from bs4 import BeautifulSoup as bs
import nums_from_string as nfs
import re
import pymysql
from datetime import datetime
 
#連接mysql資料庫
db = pymysql.connect(host='localhost',
                    user='testuser',
                    password='test123',
                    database='project1')
#建立操作游標
cursor = db.cursor()
#刪除可能資料表，避免資料錯誤
#cursor.execute("DROP TABLE IF EXISTS sofy_pad_29")

#執行www.py時才重新建立sofy_pad_29資料表
if __name__ == '__main__':
    cursor.execute('drop table if exists goods_pricing_sofy_pad_29')
    sql = """CREATE TABLE IF NOT EXISTS goods_pricing_sofy_pad_29 (
            market_name  CHAR(50) NOT NULL primary key,
            goods_price  SMALLINT(10) UNSIGNED,
            goods_num  SMALLINT(5) UNSIGNED,  
            unit_price  FLOAT(2) UNSIGNED, 
            sale_activity CHAR(10) DEFAULT 'none',
            timestamp TIMESTAMP NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP)"""
    cursor.execute(sql)
    db.close()


all_markets=[]
col=['通路名稱','商品價格','商品單位','單位價格','促銷活動有無']
market_list=[]

def all_in_1( market_name, url, price_tag, price_class_attr, unit_tag, unit_class_attr, sale_tag='0', sale_class_attr='0' ): 
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    web=requests.get(url,headers=headers)
    if web.status_code==200:   
        print('網路爬蟲成功')
        market_soup=bs(web.text,'lxml')

        #找商品價格
        goods_price=market_soup.find(price_tag,price_class_attr).text
        goods_price=nfs.get_nums(goods_price)
        goods_price=goods_price[0]
        
        #找商品單位
        goods_title=market_soup.find(unit_tag,unit_class_attr).text
        result=re.findall('(\d+)片',goods_title)+re.findall('(\d+)PC',goods_title)+re.findall('(\d+)包',goods_title)+re.findall('(\d+)入',goods_title)
        unit_num=1
        #查看是否有影響單位的活動，如果有unit_num*2
        if (sale_tag!='0') or (sale_class_attr!='0'):
            event=market_soup.find(sale_tag,sale_class_attr).text
            if event.find('買一送一')!=-1:
                unit_num*=2
                sales10='買一送一'
            elif event.find('2件5折')!=-1:
                unit_num*=2
                sales10='2件5折'
            for i in result:
                unit_num*=int(i)
        
        else:
            for i in result:
                unit_num*=int(i)
            sales10='none'

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
        return market_list

#寶雅線上買沒賣
"""
#博客來爬蟲失敗
books_soup=url('https://www.books.com.tw/products/N001290805?sloc=main')
books_price=books_soup.find('strong')
books_price=num_only(books_price.text)
market_books=market('博客來',books_price,num,'0')
print(all_markets)

#康是美官網、蝦皮失敗
cosmed_shopee_soup=url('https://shopee.tw/蘇菲極淨肌天然原生棉超薄29cm10片【任2件5折】-i.33206500.6583769178?sp_atk=f7577dfa-1fd5-4184-8858-88869ea1bcd1&xptdk=f7577dfa-1fd5-4184-8858-88869ea1bcd1')
cosmed_shopee_price=cosmed_shopee_soup.find('div',class_="pmmxKx")#salepage-price cms-moneyColor
print(cosmed_shopee_price)
cosmed_shopee_price=num_only(cosmed_shopee_price.text)
market_cosmed_shopee=market('康是美_shopee',cosmed_shopee_price,10,'0')
print(all_markets)
"""