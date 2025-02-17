from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.store_main, name='store_main'),  # /store/
    path('store_home_edit', views.store_home_edit, name='store_home_edit'),  # 홈 화면 수정
    path('about_breadscanso_edit', views.about_breadscanso_edit, name='about_breadscanso_edit'),  # 브랜드 소개
    path('store_map', views.store_map, name='store_map'),  # 매장 안내
    path('event_edit', views.event_edit, name='event_edit'),  # 이벤트
    path('community_notice', views.community_notice, name='community_notice'),  # 커뮤니티/공지사항
    path('community_qna', views.community_qna, name='community_qna'),  # 커뮤니티/Q&A
    path('store_account', views.store_account, name='store_account'),  # 매장정보
]

