import requests
from bs4 import BeautifulSoup as bs
import nums_from_string as nfs
import re
all_markets=[]
market_list=[]
sales10='0'

def all_in_1( market_name, url, price_tag, price_class_attr, unit_tag, unit_class_attr ): 
    #url:目標網址，return bs物件
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    web=requests.get(url,headers=headers)
    if web.status_code==200:
        print('網路爬蟲成功')
        market_soup=bs(web.text,'lxml')
        goods_price=market_soup.find(price_tag,price_class_attr).text
        goods_price=nfs.get_nums(goods_price)
        goods_price=goods_price[0]
        goods_title=market_soup.find(unit_tag,unit_class_attr).text
        result=re.findall('(\d+)片',goods_title)+re.findall('(\d+)PC',goods_title)+re.findall('(\d+)包',goods_title)+re.findall('(\d+)入',goods_title)
        unit_num=1
        for i in result:
            unit_num*=int(i)
        market_list=[market_name , goods_price , unit_num , round(goods_price/unit_num,2),sales10]
        return market_list

def all_in_2( market_name, url, price_tag, price_class_attr, unit_tag, unit_class_attr, sale_tag, sale_class_attr ): 
    #url:目標網址，return bs物件
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
    web=requests.get(url,headers=headers)
    if web.status_code==200:   
        print('網路爬蟲成功')
        market_soup=bs(web.text,'lxml')
        goods_price=market_soup.find(price_tag,price_class_attr).text
        goods_price=nfs.get_nums(goods_price)
        goods_price=goods_price[0]
        goods_title=market_soup.find(unit_tag,unit_class_attr).text
        result=re.findall('(\d+)片',goods_title)+re.findall('(\d+)包',goods_title)
        unit_num=1

        event=market_soup.find(sale_tag,sale_class_attr).text
        if event.find('買一送一')!=-1:
            unit_num*=2
            sales10='買一送一'
        for i in result:
            unit_num*=int(i)
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

#pchome爬不下來
pchome_soup=url('https://24h.pchome.com.tw/prod/DAAB22-A900B8P97')
goodsPrice=pchome_soup.select('#NickContainer')
goodsPrice=pchome_soup.find('span',id='PriceTotal')
print(goodsPrice)
"""