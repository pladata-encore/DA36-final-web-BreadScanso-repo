from django.urls import path
from . import views  # views.py에서 함수 가져오기

app_name = 'qna'

urlpatterns = [
    path('', views.qna_main, name='qna_main'),  # /qna/
    path('detail/<int:qna_id>/', views.qna_detail, name='qna_detail'),
    path('create/', views.qna_create, name='qna_create'),
    path('modify/<int:qna_id>/', views.qna_modify, name='qna_modify'),
    path('delete/<int:qna_id>/', views.qna_delete, name='qna_delete'),

    # question관련 view - ajax
    path('qna_search/', views.qna_search, name='qna_search'),
    # path('community_qna/question/vote/<int:question_id>/', views.question_vote, name='question_vote'),

    # answer관련 view
    path('answer_create/<int:qna_id>/',views.answer_create, name='answer_create'),
    path('answer_delete/<int:answer_id>/', views.answer_delete, name='answer_delete'),
    path('answer_modify/<int:answer_id>/', views.answer_modify, name='answer_modify'),

    # answer관련 view - ajax
    # path('community_qna/answer/vote/<int:answer_id>/', views.answer_vote, name='answer_vote'),

]