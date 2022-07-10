import requests
from bs4 import BeautifulSoup as bs
import nums_from_string as nfs
import re
import pymysql
from datetime import datetime

#執行www.py時才重新建立sofy_pad_29資料表
if __name__ == '__main__':
    #連接mysql資料庫
    db = pymysql.connect(host='localhost',
                    user='testuser',
                    password='test123',
                    database='project1')
    #建立操作游標
    cursor = db.cursor()
    cursor.execute('drop table if exists goods_pricing_sofy_pad_29')#刪除可能資料表，避免資料錯誤
    sql = """CREATE TABLE IF NOT EXISTS goods_pricing_sofy_pad_29 (
            market_name  CHAR(50) NOT NULL primary key,
            goods_price  SMALLINT(10) UNSIGNED,
            goods_num  SMALLINT(5) UNSIGNED,  
            unit_price  FLOAT(2) UNSIGNED, 
            sale_activity CHAR(10) DEFAULT 'none',
            timestamp TIMESTAMP NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
            goods_url VARCHAR(1000) DEFAULT 'none')
            """
    cursor.execute(sql)
    db.close()

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
        
        #找商品單位tag
        goods_title=market_soup.find(unit_tag,unit_class_attr).text
        #找出總數
        unit_num=unit_re(goods_title)
        #查詢是否有活動：有的話商品單位會變，沒有則為none
        if (sale_tag!='0') or (sale_class_attr!='0'):
            event=market_soup.find(sale_tag,sale_class_attr).text
            sales10,unit_num=sale_event(event,unit_num)
        else:
            sales10='none'
        
        #把資料寫入到sql
        update_sql(market_name, goods_price, unit_num,sales10,url)

        market_list=[market_name , goods_price , unit_num , round(goods_price/unit_num,2),sales10]        
        return market_list

def update_sql(market_name:str, goods_price:int, unit_num:int,sales10:str,url:str):
    #連接sql
    db = pymysql.connect(host='localhost',
                    user='testuser',
                    password='test123',
                    database='project1')
    #建立操作游標
    cursor = db.cursor()
    #sql指令
    inserting_sql = """
                INSERT INTO goods_pricing_sofy_pad_29
                (market_name,goods_price,goods_num,unit_price,sale_activity,goods_url)
                VALUES ('{}',{},{},{},'{}','{}')
                ON DUPLICATE KEY UPDATE
                goods_price={},goods_num={},unit_price={},sale_activity='{}',timestamp='{}'
                """.format(
                market_name , goods_price , unit_num , round(goods_price/unit_num,2),sales10,url,
                goods_price , unit_num , round(goods_price/unit_num,2),sales10,datetime.now())        
    try:
        cursor.execute(inserting_sql)
        # 提交到sql中執行
        db.commit()
    
    except Exception as e:#發生錯誤時回滾，撤銷已經做出的修改。
        db.rollback()
        print(e)

    cursor.close()
    db.close()

#找尋商品單位
def unit_re(goods_title):
    result=re.findall('(\d+)片',goods_title)+re.findall('(\d+)PC',goods_title)+re.findall('(\d+)包',goods_title)+re.findall('(\d+)入',goods_title)
    unit_num=1
    for i in result:
        unit_num*=int(i)
    return unit_num

def sale_event(event,unit_num):
    #查看是否有影響單位的活動，如果有unit_num*2
    if event.find('買一送一')!=-1:
        unit_num*=2
        sales10='買一送一'
    elif event.find('2件5折')!=-1& event.find('第2件5折')==-1:
        unit_num*=2
        sales10='2件5折'
    else:
        sales10='none'
    return sales10,unit_num