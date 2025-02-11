from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.menu_main, name='menu_main'),  # 소비자 메뉴정보 페이지
    path('store/', views.menu_store, name='menu_store'),  # 점주 메뉴관리 페이지
]
#TODO 이후 점주와 소비자 로그인 다르기 때문에 url 경로 재설정 필요