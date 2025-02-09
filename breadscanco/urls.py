from django.urls import path
from main import views

# namespace 지정
app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
]
