from django.urls import path
from . import views
from . import chat_views

app_name= "sales"

urlpatterns = [
    path('', views.sales_main, name='sales_main'),
    path("chatbot/", chat_views.sales_chatbot, name="sales_chatbot"),
]