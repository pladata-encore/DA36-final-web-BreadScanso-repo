from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.member_main, name='member_main'),  # /member/
    path('store/', views.member_store, name='member_store'), # 점주 회원관리
    path('page/', views.member_page, name='member_page'), # 회원 마이페이지
    path('member_edit/', views.member_edit, name='member_edit'), # 회원정보수정
    path('member_delect/', views.member_delect, name='member_delect'), # 회원탈퇴
]