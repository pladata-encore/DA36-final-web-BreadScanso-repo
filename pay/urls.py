from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.pay_main, name='pay_main'),  # /pay/
]