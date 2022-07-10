from www import all_in_1

url='https://online.carrefour.com.tw/zh/蘇菲/1212306800102.html'
goods_url=url
price_tag='span'
price_class_attr='money'
unit_tag='div'
unit_class_attr='hot'
market_carrefour=all_in_1('家樂福線上購物',url,price_tag,price_class_attr,unit_tag,unit_class_attr)
"""
market_soup=bs(web.text,'lxml')
goods_price=market_soup.find(price_tag,price_class_attr).text
goods_price=nfs.get_nums(goods_price)
goods_price=goods_price[0]
print(goods_price)
goods_title=market_soup.find(unit_tag,unit_class_attr).text
print(goods_title)
result=re.findall('(\d+).*片',goods_title)+re.findall('(\d+)包',goods_title)+re.findall('(\d+)入',goods_title)
print(result)"""
print(market_carrefour)