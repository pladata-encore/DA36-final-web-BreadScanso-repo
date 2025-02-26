from django.urls import path
from . import views  # views.py에서 함수 가져오기

app_name = 'store'
urlpatterns = [
    path('', views.store_main, name='store_main'),  # /store/
    path('member_store/', views.member_store, name='member_store'), # 매장페이지 - 회원관리
    path('update_member_store/', views.update_member_store, name='update_member_store'), # 매장페이지 - 회원관리 내 수정
    path('delete_member/', views.delete_member, name='delete_member'),  # 회원 삭제
    path('store_home_edit', views.store_home_edit, name='store_home_edit'),  # 홈 화면 수정
    path('about_breadscanso_edit', views.about_breadscanso_edit, name='about_breadscanso_edit'),  # 브랜드 소개
    path('store_map', views.store_map, name='store_map'),  # 매장 안내
    path('store_map/edit', views.store_map_edit, name='store_map_edit'),  # 매장 안내 수정
    path('store_event', views.store_event, name='store_event'),  # 이벤트
    path('store_event/edit', views.store_event_edit, name='store_event_edit'),  # 이벤트 수정 페이지
    path('community_notice', views.community_notice, name='community_notice'),  # 커뮤니티/공지사항
    path('community_notice/write', views.community_notice_write, name='community_notice_write'),  # 커뮤니티/공지사항 글쓰기
    path('community_notice/modify/<int:notice_id>', views.community_notice_modify, name='community_notice_modify'),  # 커뮤니티/공지사항 수정
    path('community_qna', views.community_qna, name='community_qna'),  # 커뮤니티/Q&A

    # question관련 view
    path('community_qna/question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('community_qna/question/create/', views.question_create, name='question_create'),
    path('community_qna/question/modify/<int:question_id>/', views.question_modify, name='question_modify'),
    path('community_qna/question/delete/<int:question_id>/', views.question_delete, name='question_delete'),

    # question관련 view - ajax
    path('community_qna/question/search/', views.question_search, name='question_search'),
    path('community_qna/question/vote/<int:question_id>/', views.question_vote, name='question_vote'),

    # answer관련 view
    path('community_qna/answer/create/<int:question_id>/',views.answer_create, name='answer_create'),
    path('community_qna/answer/delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    path('community_qna/answer/modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),

    # answer관련 view - ajax
    path('community_qna/answer/vote/<int:answer_id>/', views.answer_vote, name='answer_vote'),


    path('store_account', views.store_account, name='store_account'),  # 매장정보
]


