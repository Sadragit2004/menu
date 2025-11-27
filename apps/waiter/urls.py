# apps/restaurant/urls.py
from django.urls import path
from .views import *

app_name = 'waiter'

urlpatterns = [
    # مدیریت گارسون‌ها
    path('waiters/', waiter_dashboard, name='waiter_dashboard'),
    path('waiters/list/', waiter_list, name='waiter_list'),
    path('waiters/create/', waiter_create, name='waiter_create'),
    path('waiters/<int:pk>/', waiter_detail, name='waiter_detail'),
    path('waiters/<int:pk>/edit/', waiter_edit, name='waiter_edit'),
    path('waiters/<int:pk>/toggle-active/', waiter_toggle_active, name='waiter_toggle_active'),
    path('waiters/<int:pk>/delete/', waiter_delete, name='waiter_delete'),
    path('waiters/analytics/', waiter_analytics, name='waiter_analytics'),
    path('waiters/export/', waiter_export, name='waiter_export'),
    path('<int:pk>/panel/', waiter_panel, name='waiter_panel'),

]