from django.urls import path
from ..views.freemenuviews.views import digital_menu, get_foods_by_category, search_foods, change_language,RecordMenuView,MenuViewStats
from ..views.freemenuviews import menuview



app_name = 'menu'
urlpatterns = [
    path('<slug:restaurant_slug>/', digital_menu, name='digital_menu'),
    path('<slug:restaurant_slug>/category/<str:category_id>/', get_foods_by_category, name='foods_by_category'),
    path('<slug:restaurant_slug>/search/', search_foods, name='search_foods'),
    path('<slug:restaurant_slug>/change-language/', change_language, name='change_language'),
    path('api/restaurant/<slug:restaurant_slug>/menu/view/', RecordMenuView.as_view(), name='record_menu_view'),
    path('api/restaurant/<slug:restaurant_slug>/menu/stats/', MenuViewStats.as_view(), name='menu_view_stats'),


    # ================================

      path('d/dashboard/', menuview.analytics_dashboard, name='analytics_dashboard'),

    # API endpoints برای آمار بازدید
    path('api/daily-views/', menuview.api_daily_views, name='api_daily_views'),
    path('api/weekly-views/', menuview.api_weekly_views, name='api_weekly_views'),
    path('api/monthly-views/', menuview.api_monthly_views, name='api_monthly_views'),

    # API endpoints برای آمار غذاها
    path('api/top-foods/', menuview.api_top_foods, name='api_top_foods'),
    path('api/low-performing-foods/', menuview.api_low_performing_foods, name='api_low_performing_foods'),

    # API endpoints برای آمار سفارش‌ها
    path('api/order-analytics/', menuview.api_order_analytics, name='api_order_analytics'),
    path('api/revenue-analytics/', menuview.api_revenue_analytics, name='api_revenue_analytics'),
    path('api/food-preparation-analytics/', menuview.api_food_preparation_analytics, name='api_food_preparation_analytics'),

    # API endpoints برای آمار مشتریان
    path('api/customer-notes/', menuview.api_customer_notes_analysis, name='api_customer_notes'),
    path('api/customer-behavior/', menuview.api_customer_behavior, name='api_customer_behavior'),

    # API endpoints برای آمار گارسون‌ها
    path('api/waiter-performance/', menuview.api_waiter_performance, name='api_waiter_performance'),

    # API endpoints برای آمار دسته‌بندی‌ها
    path('api/category-analytics/', menuview.api_category_analytics, name='api_category_analytics'),

    # API endpoints برای آمار لحظه‌ای
    path('api/real-time-stats/', menuview.api_real_time_stats, name='api_real_time_stats'),
    path('api/peak-hours/', menuview.api_peak_hours, name='api_peak_hours'),

    # API endpoints برای مقایسه رستوران‌ها
    path('api/restaurant-comparison/', menuview.api_restaurant_comparison, name='api_restaurant_comparison'),
]