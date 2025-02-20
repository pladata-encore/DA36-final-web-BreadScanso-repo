from django.urls import path
from . import views  # views.py에서 함수 가져오기


urlpatterns = [
    path('', views.member_main, name='member_main'),  # /member/
    path('store/', views.member_store, name='member_store'), # 점주 회원관리
    path('member_page/', views.member_page, name='member_page'), # 회원 마이페이지
    path('member_edit/', views.member_edit, name='member_edit'), # 회원정보수정 페이지
    path('member_pw/', views.member_pw, name='member_pw'), # 비밀번호변경 페이지
    path('member_delete/', views.member_delete, name='member_delete'), # 회원탈퇴 페이지
    path('member_delete_detail/', views.member_delete_detail, name='member_delete_detail'), # 회원탈퇴 사유입력 페이지
]












# from django.urls import path
# from . import views  # views.py에서 함수 가져오기
#
#
# urlpatterns = [
#     path('', views.member_main, name='member_main'),  # /member/
#     path('store/', views.member_store, name='member_store'), # 점주 회원관리
#     path('member_page/', views.member_page, name='member_page'), # 회원 마이페이지
#     path('member_edit/', views.member_edit, name='member_edit'), # 회원정보수정 페이지
#     path('member_pw/', views.member_pw, name='member_pw'), # 비밀번호변경 페이지
#     path('member_delete/', views.member_delete, name='member_delete'), # 회원탈퇴 페이지
#     path('member_delete_detail/', views.member_delete_detail, name='member_delete_detail'), # 회원탈퇴 사유입력 페이지
# ]