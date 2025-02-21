from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.notice_main, name='notice_main'),  # /notice/
    path('notice/<int:notice_id>/', views.notice_detail, name='notice_detail'),
    path('notice/new/', views.notice_create, name='notice_create'),
    path('notice/delete/<int:notice_id>/', views.notice_delete, name='notice_delete'),
]