from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
   path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/details/', views.get_cart_details, name='get_cart_details'),
     path('checkout/create/', views.create_checkout_session, name='create_checkout'),

    # صفحات checkout با ID سفارش
    path('checkout/<int:order_id>/', views.checkout_view, name='checkout'),
    path('checkout/<int:order_id>/apply-discount/', views.apply_discount, name='apply_diQscount'),
    path('checkout/<int:order_id>/complete-order/', views.complete_order, name='complete_order'),
]