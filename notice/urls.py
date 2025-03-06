from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.notice_main, name='notice_main'),  # /notice/
    path('<int:notice_id>/', views.notice_detail, name='notice_detail'), # 공지사항 상세 페이지
    path('store/notice', views.notice_store, name='notice_store'), # 점주용 공지사항 페이지
    path('store/notice_write/', views.notice_write, name='notice_write'), # 공지사항 작성 페이지
    path('store/notice_save/', views.notice_save, name='notice_save'), # 공지사항 저장 api
    path('store/notice_delete/', views.notice_delete, name='notice_delete'), # 공지사항 삭제 api
    path('store/notice_info/<int:notice_id>/', views.notice_info, name='notice_info'),  # 관리자 페이지 공지사항 상세 페이지
    path('store/notice_edit/<int:notice_id>/', views.notice_edit, name='notice_edit'),  # 관리자 페이지 공지사항 수정 페이지
]

