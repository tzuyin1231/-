from www import all_in_2


url='https://www.watsons.com.tw/蘇菲極淨肌天然原生棉超薄潔翼夜用29cm-10片/p/BP_220711'
price_tag='div'
price_class_attr='displayPrice'
unit_tag='h1'
unit_class_attr="ng-star-inserted"
sale_tag='span'
sale_class_attr='remarks'
market_watsons=all_in_2('watsons',url,price_tag,price_class_attr,unit_tag,unit_class_attr,sale_tag,sale_class_attr)
print(market_watsons)
