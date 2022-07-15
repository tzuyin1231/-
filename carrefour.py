from www import all_in_1

url='https://online.carrefour.com.tw/zh/蘇菲/1212306800102.html'
goods_url=url
price_tag='span'
price_class_attr='money'
unit_tag='div'
unit_class_attr='title'
son_tag='p'
market_carrefour=all_in_1('家樂福線上購物',url,price_tag,price_class_attr,unit_tag,unit_class_attr,son_tag)
print(market_carrefour)