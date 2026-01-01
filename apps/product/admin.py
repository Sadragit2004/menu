# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Sum, F

from .models import (
    Product, ProductFeature, ProductGallery,
    ProductOrder, ProductOrderDetail, OrderDetailInfo
)

# ==================== INLINE CLASSES ====================

class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1
    fields = ['key', 'value', 'slug']

class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    fields = ['image', 'alt_text', 'is_active', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = "پیش‌نمایش"

class ProductOrderDetailInline(admin.TabularInline):
    model = ProductOrderDetail
    extra = 0
    fields = ['product', 'price', 'quantity', 'item_total_price']
    readonly_fields = ['item_total_price']

    def item_total_price(self, obj):
        return f"{obj.total_price:,} تومان"
    item_total_price.short_description = "قیمت کل آیتم"

# ==================== FILTERS ====================

class ProductOrderStatusFilter(admin.SimpleListFilter):
    title = 'وضعیت سفارش'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return ProductOrder.STATUS_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset

# ==================== ADMIN CLASSES ====================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_display', 'is_active', 'publish_date_jalali']
    list_filter = ['is_active', 'publish_date']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at_display']
    inlines = [ProductFeatureInline, ProductGalleryInline]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'price', 'description', 'is_active')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at_display',),
            'classes': ('collapse',)
        }),
    )

    def price_display(self, obj):
        return f"{obj.price:,} تومان"
    price_display.short_description = "قیمت"

    def publish_date_jalali(self, obj):
        return obj.publish_date.strftime("%Y/%m/%d")
    publish_date_jalali.short_description = "تاریخ انتشار"

    def created_at_display(self, obj):
        return obj.publish_date.strftime("%Y-%m-%d %H:%M:%S")
    created_at_display.short_description = "تاریخ ایجاد"

@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value', 'slug']
    list_filter = ['product']
    search_fields = ['key', 'value', 'product__name']
    list_select_related = ['product']

@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'alt_text', 'is_active']
    list_filter = ['is_active', 'product']
    list_editable = ['is_active']
    search_fields = ['product__name', 'alt_text']
    readonly_fields = ['image_preview_large']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "-"
    image_preview.short_description = "پیش‌نمایش"

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" />', obj.image.url)
        return "-"
    image_preview_large.short_description = "پیش‌نمایش بزرگ"

@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'plan', 'status_display',
        'final_price_display', 'items_count_display',
        'created_at_display', 'is_paid_display'
    ]
    list_filter = [ProductOrderStatusFilter, 'isPaid', 'plan']
    search_fields = ['user__username', 'user__email', 'plan__name', 'trackingCode']
    list_select_related = ['user', 'plan']
    inlines = [ProductOrderDetailInline]

    # فیلدهای واقعی مدل
    fieldsets = (
        ('اطلاعات سفارش', {
            'fields': ('user', 'plan', 'status', 'isPaid', 'trackingCode')
        }),
        ('اطلاعات مالی', {
            'fields': ('total_price', 'tax_amount', 'final_price')
        }),
        ('تاریخ‌ها', {
            'fields': ('createdAt', 'paidAt', 'expiryDate'),
            'classes': ('collapse',)
        }),
    )

    # فقط فیلدهای real
    readonly_fields = [
        'total_price', 'tax_amount', 'final_price',
        'createdAt', 'items_count_display'
    ]

    def status_display(self, obj):
        colors = {
            'draft': '#6c757d',
            'pending': '#ffc107',
            'paid': '#28a745',
            'failed': '#dc3545',
            'canceled': '#343a40'
        }
        color = colors.get(obj.status, '#000')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = "وضعیت"

    def final_price_display(self, obj):
        return f"{obj.final_price:,} تومان"
    final_price_display.short_description = "قیمت نهایی"

    def created_at_display(self, obj):
        return obj.createdAt.strftime("%Y/%m/%d %H:%M")
    created_at_display.short_description = "تاریخ ایجاد"

    def is_paid_display(self, obj):
        if obj.isPaid:
            return format_html('<span style="color: green; font-weight: bold;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    is_paid_display.short_description = "پرداخت"

    def items_count_display(self, obj):
        return f"{obj.items_count} عدد"
    items_count_display.short_description = "تعداد آیتم‌ها"

    def show_order_details(self, obj):
        items = obj.items.all()
        if items:
            details = []
            for item in items:
                details.append(f"{item.product_name} - {item.quantity} عدد")
            return format_html("<br>".join(details))
        return "بدون آیتم"
    show_order_details.short_description = "جزئیات سفارش"

@admin.register(ProductOrderDetail)
class ProductOrderDetailAdmin(admin.ModelAdmin):
    list_display = [
        'product_order_link', 'product_name',
        'price_display', 'quantity', 'total_price_display'
    ]
    list_filter = ['product_order__status', 'product_order__plan']
    search_fields = ['product_name', 'product_order__user__username', 'product_order__trackingCode']
    readonly_fields = ['product_name', 'product_description', 'price', 'total_price_display']
    list_select_related = ['product_order', 'product']

    def product_order_link(self, obj):
        url = f"/admin/product/productorder/{obj.product_order.id}/change/"
        return format_html(
            '<a href="{}">سفارش #{}</a>',
            url, obj.product_order.id
        )
    product_order_link.short_description = "سفارش"

    def price_display(self, obj):
        return f"{obj.price:,} تومان"
    price_display.short_description = "قیمت واحد"

    def total_price_display(self, obj):
        return f"{obj.total_price:,} تومان"
    total_price_display.short_description = "قیمت کل"

@admin.register(OrderDetailInfo)
class OrderDetailInfoAdmin(admin.ModelAdmin):
    list_display = [
        'order_id_link', 'truncated_full_name', 'phone_number',
        'city_province', 'discount_info', 'created_at_display'
    ]
    list_filter = ['city', 'province', 'created_at']
    search_fields = [
        'full_name', 'phone_number', 'email',
        'product_order__id', 'discount_code'
    ]
    readonly_fields = ['order_link', 'created_at']

    fieldsets = (
        ('اطلاعات سفارش', {
            'fields': ('order_link', 'product_order', 'created_at')
        }),
        ('اطلاعات تماس', {
            'fields': (('full_name', 'phone_number'), 'email')
        }),
        ('آدرس تحویل', {
            'fields': ('address', ('city', 'province', 'codePost'))
        }),
        ('تخفیف', {
            'fields': (('discount_code', 'discount_amount'),),
            'classes': ('collapse',)
        }),
        ('توضیحات', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )

    def order_id_link(self, obj):
        if obj.product_order:
            url = f"/admin/product/productorder/{obj.product_order.id}/change/"
            return format_html(
                '<a href="{}">سفارش #{}</a>',
                url, obj.product_order.id
            )
        return "-"
    order_id_link.short_description = "شماره سفارش"

    def order_link(self, obj):
        return self.order_id_link(obj)
    order_link.short_description = "لینک سفارش"

    def truncated_full_name(self, obj):
        if len(obj.full_name) > 20:
            return obj.full_name[:20] + '...'
        return obj.full_name
    truncated_full_name.short_description = "نام کامل"

    def city_province(self, obj):
        return f"{obj.city} / {obj.province}"
    city_province.short_description = "شهر/استان"

    def discount_info(self, obj):
        if obj.discount_code and obj.discount_amount > 0:
            return format_html(
                '<span style="color: green;">{} - {:,} تومان</span>',
                obj.discount_code, obj.discount_amount
            )
        return "بدون تخفیف"
    discount_info.short_description = "تخفیف"

    def created_at_display(self, obj):
        return obj.created_at.strftime("%Y/%m/%d %H:%M")
    created_at_display.short_description = "تاریخ ثبت"

# ==================== ACTIONS ====================

def activate_products(modeladmin, request, queryset):
    queryset.update(is_active=True)
activate_products.short_description = "فعال کردن محصولات انتخاب شده"

def deactivate_products(modeladmin, request, queryset):
    queryset.update(is_active=False)
deactivate_products.short_description = "غیرفعال کردن محصولات انتخاب شده"

def mark_orders_as_paid(modeladmin, request, queryset):
    queryset.update(isPaid=True, status='paid', paidAt=timezone.now())
mark_orders_as_paid.short_description = "علامت‌گذاری به عنوان پرداخت شده"

def mark_orders_as_pending(modeladmin, request, queryset):
    queryset.update(isPaid=False, status='pending', paidAt=None)
mark_orders_as_pending.short_description = "علامت‌گذاری به عنوان در انتظار"

# اضافه کردن actions
ProductAdmin.actions = [activate_products, deactivate_products]
ProductOrderAdmin.actions = [mark_orders_as_paid, mark_orders_as_pending]