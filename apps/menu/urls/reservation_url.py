# urls.py
from django.urls import path
from apps.panel.views.reservation_view import *



app_name = 'menu'

urlpatterns = [
    # مدیریت تایم‌اسلات‌ها - کاملاً مستقل
    path('/time-slots/',  TimeSlotListView.as_view(), name='time_slot_list'),
    path('time-slots/create/',  TimeSlotCreateView.as_view(), name='time_slot_create'),
    path('time-slots/<int:pk>/edit/',  TimeSlotUpdateView.as_view(), name='time_slot_edit'),
    path('time-slots/<int:pk>/delete/',  TimeSlotDeleteView.as_view(), name='time_slot_delete'),
    path('time-slots/generate/',  TimeSlotGenerationView.as_view(), name='time_slot_generate'),
    path('time-slots/availability/',  TimeSlotAvailabilityView.as_view(), name='time_slot_availability'),

    # مدیریت رزروها - کاملاً مستقل
    path('reservations/',  ReservationListView.as_view(), name='reservation_list'),
    path('reservations/<int:pk>/',  ReservationDetailView.as_view(), name='reservation_detail'),

    # مدیریت ساعت کاری - کاملاً مستقل
    path('working-hours/',  WorkingHoursListView.as_view(), name='working_hours_list'),
    path('working-hours/<int:pk>/edit/',  WorkingHoursUpdateView.as_view(), name='working_hours_edit'),

    # API های AJAX - کاملاً مستقل
    path('api/time-slot-reservations/',  GetTimeSlotReservationsView.as_view(), name='api_time_slot_reservations'),
    path('api/available-tables/',  GetAvailableTablesView.as_view(), name='api_available_tables'),
]