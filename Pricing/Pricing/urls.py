from django.contrib import admin
from django.urls import re_path
from . import views #從當前目錄import views模組（檔案）
from goods_pricing.views import table


urlpatterns = [
    re_path('admin/', admin.site.urls),
    re_path(r'^hello/$', views.hello), #指定網址http://127.0.0.1:8000/hello/
    re_path('sofy/',table),

]
