from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.store_info_main, name='store_info_main'),  # /store_info/
]