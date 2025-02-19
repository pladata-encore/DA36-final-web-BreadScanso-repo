from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.store_main, name='store_main'),  # /store/
    path('store_home_edit', views.store_home_edit, name='store_home_edit'),  # 홈 화면 수정
    path('about_breadscanso_edit', views.about_breadscanso_edit, name='about_breadscanso_edit'),  # 브랜드 소개
    path('store_map', views.store_map, name='store_map'),  # 매장 안내
    path('store_map/edit', views.store_map_edit, name='store_map_edit'),  # 매장 안내 수정
    path('store_event', views.store_event, name='store_event'),  # 이벤트
    path('store_event/edit', views.store_event_edit, name='store_event_edit'),  # 이벤트
    path('community_notice', views.community_notice, name='community_notice'),  # 커뮤니티/공지사항
    path('community_notice/write', views.community_notice_write, name='community_notice_write'),  # 커뮤니티/공지사항 글쓰기
    path('community_notice/modify/<int:notice_id>', views.community_notice_modify, name='community_notice_modify'),  # 커뮤니티/공지사항 수정
    path('community_qna', views.community_qna, name='community_qna'),  # 커뮤니티/Q&A
    path('community_qna', views.community_qna, name='community_qna'),  # 커뮤니티/Q&A
    path('store_account', views.store_account, name='store_account'),  # 매장정보
]

