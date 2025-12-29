from django.urls import path
from ..views.freemenuviews.views import (
    digital_menu, get_foods_by_category, search_foods, change_language,
    RecordMenuView, MenuViewStats
,

)



app_name = 'menu'
urlpatterns = [
    # Paper menu URLs (must come first to avoid conflicts with restaurant slug patterns)


    # Restaurant menu URLs (generic patterns come last)
    path('<slug:restaurant_slug>/', digital_menu, name='digital_menu'),
    path('<slug:restaurant_slug>/category/<str:category_id>/', get_foods_by_category, name='foods_by_category'),
    path('<slug:restaurant_slug>/search/', search_foods, name='search_foods'),
    path('<slug:restaurant_slug>/change-language/', change_language, name='change_language'),
    path('api/restaurant/<slug:restaurant_slug>/menu/view/', RecordMenuView.as_view(), name='record_menu_view'),
    path('api/restaurant/<slug:restaurant_slug>/menu/stats/', MenuViewStats.as_view(), name='menu_view_stats'),


    # ================================


]