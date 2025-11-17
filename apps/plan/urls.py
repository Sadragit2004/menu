from django.urls import path
from . import views

app_name = 'plan'

urlpatterns = [

    path('planList/', views.plan_list, name='plan_list'),
    path('cart/', views.shop_cart, name='shop_cart'),
    path('assign-restaurant/', views.assign_restaurant_to_plan, name='assign_restaurant'),
    path('purchase/<slug:plan_slug>/', views.purchase_plan, name='purchase_plan'),
]