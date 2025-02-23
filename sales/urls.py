from django.urls import path

from member.urls import app_name
from . import views

app_name= "sales"

urlpatterns = [
    path('', views.sales_main, name='sales_main'),
]