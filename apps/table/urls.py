from django.urls import path
from . import views
from . import viewres

app_name = 'table'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.reservation_dashboard, name='dashboard'),

    # Tables
    path('tables/', views.table_list, name='table_list'),
    path('tables/create/', views.table_create, name='table_create'),
    path('tables/<int:table_id>/', views.table_detail, name='table_detail'),
    path('tables/<int:table_id>/edit/', views.table_edit, name='table_edit'),
    path('tables/<int:table_id>/delete/', views.table_delete, name='table_delete'),

    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:customer_id>/', views.customer_detail, name='customer_detail'),

    # Reservations
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/create/', views.reservation_create, name='reservation_create'),
    path('reservations/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('reservations/<int:reservation_id>/confirm/', views.reservation_confirm, name='reservation_confirm'),
    path('reservations/<int:reservation_id>/cancel/', views.reservation_cancel, name='reservation_cancel'),
    path('reservations/<int:reservation_id>/seated/', views.reservation_mark_seated, name='reservation_mark_seated'),
    path('reservations/<int:reservation_id>/completed/', views.reservation_mark_completed, name='reservation_mark_completed'),
    path('reservations/<int:reservation_id>/no-show/', views.reservation_mark_no_show, name='reservation_mark_no_show'),

    # Working Time
    path('working-time/', views.working_time_management, name='working_time_management'),

    # Settings
    path('settings/', views.reservation_settings, name='reservation_settings'),

    # AJAX
    path('ajax/table/<int:table_id>/availability/', views.get_table_availability_ajax, name='ajax_table_availability'),
    path('ajax/calendar/daily/', views.get_daily_calendar_ajax, name='ajax_daily_calendar'),
    path('ajax/tables/available/', views.get_available_tables_ajax, name='ajax_available_tables'),
    path('ajax/table/<int:table_id>/reservations/', views.get_table_reservations_ajax, name='ajax_table_reservations'),


    #==========
   path('<slug:restaurant_slug>/check-availability/', viewres.check_availability_ajax, name='check_availability'),
    path('<slug:restaurant_slug>/create-reservation/', viewres.create_reservation_ajax, name='create_reservation'),
    path('verify/<str:reservation_code>/', viewres.verify_reservation_ajax, name='verify_reservation'),
    path('status/<str:reservation_code>/', viewres.reservation_status_ajax, name='reservation_status'),  # ✅ اصلاح شده
]