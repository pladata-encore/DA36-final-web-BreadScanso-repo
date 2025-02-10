from django.urls import path, include
from main import views

# namespace 지정
app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('kiosk/', include('kiosk.urls')),  # kiosk 앱의 urls.py를 포함
]
