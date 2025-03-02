from django.urls import path
from . import views

app_name= "sales"

urlpatterns = [
    path('', views.sales_main, name='sales_main'),
]