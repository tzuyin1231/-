from django.db import models
from datetime import datetime
class sofy_pad_29(models.Model):
    market_name = models.CharField(max_length=50,null=False,primary_key=True) #通路名稱
    goods_price = models.DecimalField(max_digits=10,decimal_places=0) #商品價格
    goods_num = models.DecimalField(max_digits=10,decimal_places=0) #商品單位
    unit_price = models.DecimalField(max_digits=10,decimal_places=2) #單位價格
    sale_activity = models.CharField(max_length=10,default='none') #促銷活動
    timestamp = models.DateTimeField(default=datetime.now)
    goods_url = models.CharField(max_length=1000) #通路名稱
    def __str__(self):
        return self.name
    
    class Meta:#預設按照商品價格排序
        ordering = ['goods_price']
