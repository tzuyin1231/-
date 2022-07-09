from django.shortcuts import render
#from sofy.models import forms
from goods_pricing.models import sofy_pad_29    #插入表

def table(request):
  #table_form=forms.SignupForm()  #樣式 ，在forms.py裡配置好了
  markets=sofy_pad_29.objects.all()  #獲取我們的資料庫資訊到names裡
  return render(request,"markets.html",locals()) #必須用這個return
