from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Product, ProductFeature, ProductGallery, ProductOrder, ProductOrderDetail

# Inline برای ویژگی‌های محصول
class ProductFeatureInline(admin.TabularInline):
    model = ProductFeature
    extra = 1
    fields = ['key', 'value', 'slug']
    verbose_name = "ویژگی محصول"
    verbose_name_plural = "ویژگی‌های محصول"

# Inline برای گالری محصول
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1
    fields = ['image', 'alt_text', 'is_active', 'image_preview']
    readonly_fields = ['image_preview']
    verbose_name = "عکس گالری"
    verbose_name_plural = "گالری محصولات"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = "پیش‌نمایش"

# Inline برای جزئیات سفارش - اصلاح شده
class ProductOrderDetailInline(admin.TabularInline):
    model = ProductOrderDetail
    extra = 0
    fields = ['product', 'price', 'quantity', 'total_price_display']
    readonly_fields = ['total_price_display']
    verbose_name = "جزئیات سفارش"
    verbose_name_plural = "جزئیات سفارشات"

    def total_price_display(self, obj):
        try:
            return f"{obj.total_price:,} تومان"
        except (TypeError, ValueError):
            return "0 تومان"
    total_price_display.short_description = "قیمت کل"

# فیلترهای سفارشی
class ProductStatusFilter(admin.SimpleListFilter):
    title = 'وضعیت فعال'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('active', 'فعال'),
            ('inactive', 'غیرفعال'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)

class ProductOrderStatusFilter(admin.SimpleListFilter):
    title = 'وضعیت سفارش'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return ProductOrder.STATUS_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())

# مدل ادمین برای محصول
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price_display', 'is_active', 'publish_date', 'features_count', 'gallery_count']
    list_filter = [ProductStatusFilter, 'publish_date']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    readonly_fields = ['publish_date', 'created_at_display']
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('name', 'price', 'description', 'is_active')
        }),
        ('تاریخ‌ها', {
            'fields': ('publish_date', 'created_at_display'),
            'classes': ('collapse',)
        }),
    )
    inlines = [ProductFeatureInline, ProductGalleryInline]

    def price_display(self, obj):
        try:
            return f"{obj.price:,} تومان"
        except (TypeError, ValueError):
            return "0 تومان"
    price_display.short_description = "قیمت"

    def features_count(self, obj):
        return obj.features.count()
    features_count.short_description = "تعداد ویژگی‌ها"

    def gallery_count(self, obj):
        return obj.gallery.count()
    gallery_count.short_description = "تعداد عکس‌ها"

    def created_at_display(self, obj):
        return obj.publish_date.strftime("%Y-%m-%d %H:%M")
    created_at_display.short_description = "تاریخ ایجاد"

# مدل ادمین برای ویژگی محصول
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ['product', 'key', 'value', 'slug']
    list_filter = ['product']
    search_fields = ['key', 'value', 'product__name']
    list_select_related = ['product']

# مدل ادمین برای گالری محصول
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'alt_text', 'is_active']
    list_filter = ['is_active', 'product']
    list_editable = ['is_active']
    search_fields = ['product__name', 'alt_text']
    readonly_fields = ['image_preview_large']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview.short_description = "پیش‌نمایش"

    def image_preview_large(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" height="200" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_preview_large.short_description = "پیش‌نمایش بزرگ"

# مدل ادمین برای سفارش محصول
class ProductOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'plan', 'status_display', 'final_price_display', 'items_count', 'created_at_display', 'is_paid_display']
    list_filter = [ProductOrderStatusFilter, 'isPaid', 'createdAt', 'plan']
    search_fields = ['user__username', 'user__email', 'plan__name', 'trackingCode']
    readonly_fields = ['createdAt', 'total_price', 'final_price', 'items_count_display', 'order_details']
    list_select_related = ['user', 'plan']
    inlines = [ProductOrderDetailInline]
    fieldsets = (
        ('اطلاعات سفارش', {
            'fields': ('user', 'plan', 'status', 'isPaid', 'trackingCode')
        }),
        ('اطلاعات مالی', {
            'fields': ('total_price', 'final_price', 'items_count_display')
        }),
        ('تاریخ‌ها', {
            'fields': ('createdAt', 'paidAt', 'expiryDate'),
            'classes': ('collapse',)
        }),
    )

    def status_display(self, obj):
        status_colors = {
            'draft': 'gray',
            'pending': 'orange',
            'paid': 'green',
            'failed': 'red',
            'canceled': 'darkred'
        }
        color = status_colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_display.short_description = "وضعیت"

    def final_price_display(self, obj):
        try:
            return f"{obj.final_price:,} تومان"
        except (TypeError, ValueError):
            return "0 تومان"
    final_price_display.short_description = "قیمت نهایی"

    def created_at_display(self, obj):
        return obj.createdAt.strftime("%Y-%m-%d %H:%M")
    created_at_display.short_description = "تاریخ ایجاد"

    def is_paid_display(self, obj):
        if obj.isPaid:
            return format_html('<span style="color: green;">✓</span>')
        return format_html('<span style="color: red;">✗</span>')
    is_paid_display.short_description = "پرداخت شده"

    def items_count_display(self, obj):
        return f"{obj.items_count} عدد"
    items_count_display.short_description = "تعداد آیتم‌ها"

    def order_details(self, obj):
        items = obj.items.all()
        if items:
            details = []
            for item in items:
                try:
                    details.append(f"{item.product_name} - {item.quantity} عدد - {item.total_price:,} تومان")
                except (TypeError, ValueError):
                    details.append(f"{item.product_name} - {item.quantity} عدد - 0 تومان")
            return format_html("<br>".join(details))
        return "هیچ آیتمی وجود ندارد"
    order_details.short_description = "جزئیات سفارش"

# مدل ادمین برای جزئیات سفارش
class ProductOrderDetailAdmin(admin.ModelAdmin):
    list_display = ['product_order', 'product_name', 'price_display', 'quantity', 'total_price_display']
    list_filter = ['product_order__status', 'product_order__plan']
    search_fields = ['product_name', 'product_order__user__username', 'product_order__trackingCode']
    readonly_fields = ['product_name', 'product_description', 'price', 'total_price_display']
    list_select_related = ['product_order', 'product']

    def price_display(self, obj):
        try:
            return f"{obj.price:,} تومان"
        except (TypeError, ValueError):
            return "0 تومان"
    price_display.short_description = "قیمت واحد"

    def total_price_display(self, obj):
        try:
            return f"{obj.total_price:,} تومان"
        except (TypeError, ValueError):
            return "0 تومان"
    total_price_display.short_description = "قیمت کل"

# Actions سفارشی برای ادمین
def make_published(modeladmin, request, queryset):
    queryset.update(is_active=True)
make_published.short_description = "فعال کردن محصولات انتخاب شده"

def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_active=False)
make_unpublished.short_description = "غیرفعال کردن محصولات انتخاب شده"

def mark_as_paid(modeladmin, request, queryset):
    queryset.update(isPaid=True, status='paid', paidAt=timezone.now())
mark_as_paid.short_description = "علامت‌گذاری به عنوان پرداخت شده"

def mark_as_pending(modeladmin, request, queryset):
    queryset.update(isPaid=False, status='pending', paidAt=None)
mark_as_pending.short_description = "علامت‌گذاری به عنوان در انتظار پرداخت"

# اضافه کردن actions به مدل‌ها
ProductAdmin.actions = [make_published, make_unpublished]
ProductOrderAdmin.actions = [mark_as_paid, mark_as_pending]

# ثبت مدل‌ها
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductFeature, ProductFeatureAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(ProductOrderDetail, ProductOrderDetailAdmin)



# در فایل admin.py
from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from .models import OrderDetailInfo

@admin.register(OrderDetailInfo)
class OrderDetailInfoAdmin(admin.ModelAdmin):
    # لیست فیلدهایی که در صفحه لیست نمایش داده می‌شوند
    list_display = [
        'get_order_id',
        'truncated_full_name',
        'phone_number',
        'city_province',
        'get_discount_info',
        'created_at_shamsi',
        'quick_actions'
    ]

    # فیلترهای سمت راست
    list_filter = [
        'city',
        'province',
        'created_at',
        'discount_code'
    ]

    # جستجو در فیلدهای زیر
    search_fields = [
        'full_name',
        'phone_number',
        'email',
        'product_order__id',
        'discount_code',
        'city',
        'province'
    ]

    # فیلدهای فقط خواندنی
    readonly_fields = [
        'created_at',
        'get_order_link'
    ]

    # گروه‌بندی فیلدها در صفحه ویرایش
    fieldsets = (
        ('اطلاعات پایه سفارش', {
            'fields': ('get_order_link', 'product_order', 'created_at'),
            'classes': ('wide',)
        }),
        ('اطلاعات تماس', {
            'fields': (
                ('full_name', 'phone_number'),
                'email'
            )
        }),
        ('آدرس تحویل', {
            'fields': (
                'address',
                ('city', 'province', 'codePost')
            )
        }),
        ('تخفیف و مالی', {
            'fields': (
                ('discount_code', 'discount_amount'),
            ),
            'classes': ('collapse',)
        }),
        ('یادداشت‌ها', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )

    # نمایش سفارش مرتبط به صورت لینک
    def get_order_link(self, obj):
        if obj.product_order:
            url = f"/admin/product/productorder/{obj.product_order.id}/change/"
            return format_html(
                '<a href="{}" style="background: #4CAF50; color: white; padding: 5px 10px; border-radius: 4px; text-decoration: none;" target="_blank">🎯 مشاهده سفارش #{}</a>',
                url, obj.product_order.id
            )
        return format_html('<span style="color: #999;">بدون سفارش مرتبط</span>')
    get_order_link.short_description = "سفارش مرتبط"

    # نمایش شماره سفارش
    def get_order_id(self, obj):
        if obj.product_order:
            return f"#{obj.product_order.id}"
        return "-"
    get_order_id.short_description = "شماره سفارش"

    # نام کامل truncated
    def truncated_full_name(self, obj):
        if len(obj.full_name) > 20:
            return obj.full_name[:20] + '...'
        return obj.full_name
    truncated_full_name.short_description = "نام کامل"

    # شهر و استان با هم
    def city_province(self, obj):
        return f"{obj.city} - {obj.province}"
    city_province.short_description = "شهر / استان"

    # اطلاعات تخفیف
    def get_discount_info(self, obj):
        if obj.discount_code and obj.discount_amount > 0:
            return format_html(
                '<span style="color: #4CAF50;">{} - {}</span>',
                obj.discount_code,
                f"{obj.discount_amount:,} تومان"
            )
        return format_html('<span style="color: #999;">بدون تخفیف</span>')
    get_discount_info.short_description = "تخفیف"

    # تاریخ شمسی
    def created_at_shamsi(self, obj):
        return obj.created_at.strftime("%Y/%m/%d - %H:%M")
    created_at_shamsi.short_description = "تاریخ ثبت"

    # دکمه‌های سریع
    def quick_actions(self, obj):
        return format_html(
            '<div style="display: flex; gap: 5px;">'
            '<a href="/admin/product/orderdetailinfo/{}/change/" class="button" style="padding: 5px 10px; background: #2196F3; color: white; border-radius: 3px; text-decoration: none;">✏️</a>'
            '<a href="/admin/product/orderdetailinfo/{}/delete/" class="button" style="padding: 5px 10px; background: #f44336; color: white; border-radius: 3px; text-decoration: none;">🗑️</a>'
            '</div>',
            obj.id, obj.id
        )
    quick_actions.short_description = "عملیات"

    # بهینه‌سازی کوئری‌ها
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('product_order')

    # دسترسی‌ها
    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    # ذخیره خودکار تاریخ
    def save_model(self, request, obj, form, change):
        if not change:  # اگر رکورد جدید است
            obj.created_at = timezone.now()
        super().save_model(request, obj, form, change)

    # سفارشی‌سازی ظاهر
    class Media:
        css = {
            'all': ('admin/css/orderdetailinfo.css',)
        }

# فایل CSS سفارشی (اختیاری)
# در static/admin/css/orderdetailinfo.css
"""
.field-get_order_link {
    background: #f8f9fa;
    padding: 10px;
    border-radius: 5px;
    border-right: 4px solid #4CAF50;
}
"""