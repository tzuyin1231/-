from www import all_in_1

url='https://m.momoshop.com.tw/goods.momo?i_code=8764965&mdiv=searchEngine&oid=1_1&kw=蘇菲原生棉29'
goods_url=url
price_tag='p'
price_class_attr='priceTxtArea'
unit_tag='p'
unit_class_attr="fprdTitle"
market_momo=all_in_1('momo',url,price_tag,price_class_attr,unit_tag,unit_class_attr)
print(market_momo)


