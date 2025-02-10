from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.kiosk_main, name='kiosk_main'),  # /kiosk/ kiosk 메인 페이지
    path('products/', views.products, name='products'),  # 상품 안내 페이지 추가
]
