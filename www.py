import webbrowser as wb
import requests
from bs4 import BeautifulSoup as bs
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
all_markets=[]


def url(s:str):
    web=requests.get(s,headers=headers)
    if web.status_code==200:   
        print('網路爬蟲成功')
        soup=bs(web.text,'lxml')
        return soup


def unit_price(p:int):
    return round(p/num,2)

def num_only(total:str):
    j=1
    s = [int(s) for s in re.findall(r'-?\d+\.?\d*', total)]
    for i in s:
        j*=i
    return j

def market(s:str,p:int,unit:int,activity:str):
    s=['{}'.format(s),p,round(p/unit,2),activity]
    all_markets.append(s)
    return s




#momo
momo_soup=url('https://m.momoshop.com.tw/goods.momo?i_code=8764965&mdiv=searchEngine&oid=1_1&kw=蘇菲原生棉29'
)
goodsName=momo_soup.find(id='osmGoodsName')
#print(goodsName.text)
goodsPrice=momo_soup.find('p','priceTxtArea')
momo_price=num_only(goodsPrice.text)
total='15片*2包'
num=num_only(total)

market_momo=market('momo',momo_price,num,'0')
#print(market_momo)
print(all_markets)

"""pchome爬不下來
pchome_soup=url('https://24h.pchome.com.tw/prod/DAAB22-A900B8P97')
goodsPrice=pchome_soup.select('#NickContainer')

#goodsPrice=pchome_soup.find('span',id='PriceTotal')
print(goodsPrice)
"""
#屈臣氏 買一送一不知道怎麼辦
watsons_soup=url('https://www.watsons.com.tw/蘇菲極淨肌天然原生棉超薄潔翼夜用29cm-10片/p/BP_220711')
watsons_price=watsons_soup.find('div','displayPrice ng-star-inserted')
watsons_price=num_only(watsons_price.text)
watsons_unit=10
watsons_event=watsons_soup.find('span','remarks')
if watsons_event.text.find('買一送一')!=-1:
    watsons_unit*=2
market_watsons=market('屈臣氏官網',watsons_price,watsons_unit,'買一送一')
#print(market_watsons)
print(all_markets)

"""
#康是美官網、蝦皮失敗

cosmed_shopee_soup=url('https://shopee.tw/蘇菲極淨肌天然原生棉超薄29cm10片【任2件5折】-i.33206500.6583769178?sp_atk=f7577dfa-1fd5-4184-8858-88869ea1bcd1&xptdk=f7577dfa-1fd5-4184-8858-88869ea1bcd1')
cosmed_shopee_price=cosmed_shopee_soup.find('div',class_="pmmxKx")#salepage-price cms-moneyColor
print(cosmed_shopee_price)
cosmed_shopee_price=num_only(cosmed_shopee_price.text)
market_cosmed_shopee=market('康是美_shopee',cosmed_shopee_price,10,'0')
print(all_markets)
"""
#yahoo
yahoo_soup=url('https://tw.buy.yahoo.com/gdsale/蘇菲-極淨肌-天然原生棉超薄潔翼日用-29cm-15片x2包-組-9469988.html')
yahoo_price=yahoo_soup.find('div',class_="HeroInfo__mainPrice___1xP9H")
yahoo_price=num_only(yahoo_price.text)
market_yahoo=market('yahoo購物中心',yahoo_price,num,'0')
print(all_markets)
#寶雅線上買沒賣
#家樂福
carrefour_soup=url('https://online.carrefour.com.tw/zh/蘇菲/1212306800102.html')
carrefour_price=carrefour_soup.find('span','money')
carrefour_price=num_only(carrefour_price.text)
market_carrefour=market('家樂福線上購物',carrefour_price,num,'0')
print(all_markets)
#博客來
books_soup=url('https://www.books.com.tw/products/N001290805?sloc=main')
books_price=books_soup.find('strong')
books_price=num_only(books_price.text)
market_books=market('博客來',books_price,num,'0')
print(all_markets)


