from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales_main, name='sales_main'),
]