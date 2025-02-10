from django.urls import path, include
from main import views

# namespace 지정
app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('kiosk/', include('kiosk.urls')),  # kiosk 앱의 urls.py를 포함
    path('brand/', include('brand.urls')),  # brand 앱의 urls.py를 포함
    path('event/', include('event.urls')),  # event 앱의 urls.py를 포함
    path('member/', include('member.urls')),  # member 앱의 urls.py를 포함
    path('menu/', include('menu.urls')),  # menu 앱의 urls.py를 포함
    path('notice/', include('notice.urls')),  # notice 앱의 urls.py를 포함
    path('pay/', include('pay.urls')),  # pay 앱의 urls.py를 포함
    path('qna/', include('qna.urls')),  # qna 앱의 urls.py를 포함
    path('sales/', include('sales.urls')),  # sales 앱의 urls.py를 포함
    path('stock/', include('stock.urls')),  # stock 앱의 urls.py를 포함
    path('store/', include('store.urls')),  # store 앱의 urls.py를 포함
    path('store_info/', include('store_info.urls')),  # store_info 앱의 urls.py를 포함

]
