from django.contrib import admin
from .models import Waiter, Order, OrderItem, WaiterAssignment

@admin.register(Waiter)
class WaiterAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'code', 'restaurant', 'mobileNumber', 'isActive']
    list_filter = ['restaurant', 'isActive']
    search_fields = ['fullname', 'code', 'mobileNumber']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'restaurant', 'waiter', 'status', 'final_price', 'createdAt']
    list_filter = ['status', 'restaurant', 'createdAt']
    search_fields = ['session_key', 'table_number']

admin.site.register(OrderItem)
admin.site.register(WaiterAssignment)