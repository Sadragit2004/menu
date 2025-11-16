# apps/peyment/urls.py
from django.urls import path
from .views import *

app_name = 'peyment'

urlpatterns = [
    # URLهای پرداخت یکپارچه
    path('request/<str:payment_type>/<int:order_id>/', unified_send_request, name='unified_request'),
    path('verify/', UnifiedVerifyView.as_view(), name='verify'),

    # URLهای قدیمی برای backward compatibility
    path('request/<int:order_id>/', send_request, name='request'),
    path('verify-old/', Zarin_pal_view_verfiy.as_view(), name='verify_old'),

    # URLهای نمایش پیام
    path('success/<str:message>/', show_success, name='show_success'),
    path('failed/<str:message>/', show_failed, name='show_failed'),

    # URLهای قدیمی برای backward compatibility
    path('show_sucess/<str:message>/', show_verfiy_message, name='show_sucess'),
    path('show_verfiy_unmessage/<str:message>/', show_verfiy_unmessage, name='show_verfiy_unmessage'),
]