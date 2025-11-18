
from django.urls import path
from . import views

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

    # Reservations
    path('reservations/', views.reservation_list, name='reservation_list'),
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
    path('ajax/table/<int:table_id>/reservations/', views.get_table_reservations_ajax, name='ajax_table_reservations'),
    path('ajax/calendar/daily/', views.get_daily_calendar_ajax, name='ajax_daily_calendar'),
]
