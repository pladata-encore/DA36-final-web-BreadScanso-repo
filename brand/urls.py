from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.brand_main, name='brand_main'),  # /brand/
]