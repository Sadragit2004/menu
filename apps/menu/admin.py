from django.contrib import admin, messages
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Count
from .models.menufreemodels.models import Category, Restaurant, MenuCategory, Food, ExchangeRate, FoodRestaurant, MenuView
from .helper import update_all_food_prices


# ----------------------------
# Mixin for bilingual support
# ----------------------------
class BilingualAdminMixin:
    """میکسین برای پشتیبانی از نمایش دو زبانه در ادمین"""

    def get_title_display(self, obj):
        """نمایش عنوان دو زبانه"""
        title_fa = obj.title or '-'
        title_en = obj.title_en or '-'
        return format_html(
            '<div style="direction: rtl; text-align: right;">'
            '<strong>فارسی:</strong> {}<br>'
            '<strong>English:</strong> {}'
            '</div>',
            title_fa, title_en
        )
    get_title_display.short_description = _('Title')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin, BilingualAdminMixin):
    list_display = ['get_title_display', 'slug', 'isActive', 'displayOrder', 'createdAt', 'get_image_preview']
    list_filter = ['isActive', 'createdAt']
    search_fields = ['title', 'title_en', 'slug']
    readonly_fields = ['createdAt', 'updatedAt', 'get_image_preview', 'get_title_display']
    list_editable = ['isActive', 'displayOrder']
    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('get_title_display', 'title', 'title_en', 'slug', 'isActive', 'displayOrder')
        }),
        (_('Relations'), {
            'fields': ('parent',)
        }),
        (_('Media'), {
            'fields': ('image', 'get_image_preview')
        }),
        (_('Timestamps'), {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )

    def get_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return _("No Image")
    get_image_preview.short_description = _('Image Preview')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin, BilingualAdminMixin):
    list_display = [
        'get_title_display',
        'slug',
        'phone',
        'total_menu_views',
        'recent_menu_views',
        'isActive',
        'displayOrder',
        'expiry_status_display',
        'createdAt',
        'get_logo_preview'
    ]

    list_filter = [
        'isActive',
        'createdAt',
        'expireDate',
    ]

    search_fields = [
        'title',
        'title_en',
        'slug',
        'phone',
        'address',
        'address_en'
    ]

    readonly_fields = [
        'createdAt',
        'updatedAt',
        'get_logo_preview',
        'get_cover_preview',
        'get_title_display',
        'total_menu_views_display',
        'daily_menu_views_display',
        'weekly_menu_views_display',
        'expiry_status_display',
    ]

    list_editable = [
        'isActive',
        'displayOrder'
    ]

    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'owner', 'get_title_display', 'title', 'title_en', 'slug', 'text',
                'description', 'description_en', 'isSeo',
                'isActive', 'displayOrder',
            )
        }),
        (_('Menu View Statistics'), {
            'fields': (
                'total_menu_views_display',
                'daily_menu_views_display',
                'weekly_menu_views_display',
            ),
            'classes': ('collapse',)
        }),
        (_('Contact Information'), {
            'fields': ('phone', 'address', 'address_en')
        }),
        (_('Images'), {
            'fields': ('logo', 'get_logo_preview', 'coverImage', 'get_cover_preview')
        }),
        (_('Business Settings'), {
            'fields': ('openingTime', 'closingTime', 'minimumOrder', 'deliveryFee', 'taxRate')
        }),
        (_('Expiry Management'), {
            'fields': (
                'expireDate',
                'expiry_status_display',
            )
        }),
        (_('Timestamps'), {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )

    def get_logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.logo.url)
        return _("No Logo")
    get_logo_preview.short_description = _('Logo Preview')

    def get_cover_preview(self, obj):
        if obj.coverImage:
            return format_html('<img src="{}" width="80" height="40" style="border-radius: 3px;" />', obj.coverImage.url)
        return _("No Cover")
    get_cover_preview.short_description = _('Cover Preview')

    # آمار بازدید منو
    def total_menu_views(self, obj):
        return obj.menu_views.count()
    total_menu_views.short_description = _('Total Menu Views')
    total_menu_views.admin_order_field = 'menu_views_count'

    def recent_menu_views(self, obj):
        from datetime import timedelta
        since = timezone.now() - timedelta(days=7)
        return obj.menu_views.filter(created_at__gte=since).count()
    recent_menu_views.short_description = _('Recent Views (7d)')

    def total_menu_views_display(self, obj):
        count = self.total_menu_views(obj)
        return format_html('<strong style="color: #007bff;">{:,}</strong>', count)
    total_menu_views_display.short_description = _('Total Menu Views')

    def daily_menu_views_display(self, obj):
        from datetime import timedelta
        since = timezone.now() - timedelta(hours=24)
        count = obj.menu_views.filter(created_at__gte=since).count()
        color = "green" if count > 0 else "gray"
        return format_html('<strong style="color: {};">{:,}</strong>', color, count)
    daily_menu_views_display.short_description = _('Daily Menu Views')

    def weekly_menu_views_display(self, obj):
        from datetime import timedelta
        since = timezone.now() - timedelta(days=7)
        count = obj.menu_views.filter(created_at__gte=since).count()
        color = "orange" if count > 0 else "gray"
        return format_html('<strong style="color: {};">{:,}</strong>', color, count)
    weekly_menu_views_display.short_description = _('Weekly Menu Views')

    # مدیریت انقضا
    def expiry_status_display(self, obj):
        status = obj.expiry_status
        if "منقضی شده" in status:
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', status)
        elif "در آستانه انقضا" in status:
            return format_html('<span style="color: orange; font-weight: bold;">{}</span>', status)
        elif "فعال" in status:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', status)
        else:
            return format_html('<span style="color: gray;">{}</span>', status)
    expiry_status_display.short_description = _('Expiry Status')

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            menu_views_count=Count('menu_views')
        )

    # اکشن‌های سفارشی برای مدیریت انقضا
    actions = ['extend_expiry_30_days', 'extend_expiry_90_days', 'deactivate_expired']

    def extend_expiry_30_days(self, request, queryset):
        success_count = 0
        for restaurant in queryset:
            success, message = restaurant.extend_expiry(30)
            if success:
                success_count += 1

        if success_count > 0:
            self.message_user(
                request,
                f"تاریخ انقضا برای {success_count} رستوران با موفقیت 30 روز تمدید شد",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                "هیچ رستورانی تمدید نشد",
                messages.WARNING
            )
    extend_expiry_30_days.short_description = _("تمدید 30 روزه تاریخ انقضا برای رستوران‌های انتخاب شده")

    def extend_expiry_90_days(self, request, queryset):
        success_count = 0
        for restaurant in queryset:
            success, message = restaurant.extend_expiry(90)
            if success:
                success_count += 1

        if success_count > 0:
            self.message_user(
                request,
                f"تاریخ انقضا برای {success_count} رستوران با موفقیت 90 روز تمدید شد",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                "هیچ رستورانی تمدید نشد",
                messages.WARNING
            )
    extend_expiry_90_days.short_description = _("تمدید 90 روزه تاریخ انقضا برای رستوران‌های انتخاب شده")

    def deactivate_expired(self, request, queryset):
        expired_restaurants = queryset.filter(expireDate__lt=timezone.now())
        count = expired_restaurants.update(isActive=False)

        if count > 0:
            self.message_user(
                request,
                f"{count} رستوران منقضی شده غیرفعال شدند",
                messages.SUCCESS
            )
        else:
            self.message_user(
                request,
                "هیچ رستوران منقضی شده‌ای در بین موارد انتخاب شده وجود ندارد",
                messages.WARNING
            )
    deactivate_expired.short_description = _("غیرفعال کردن رستوران‌های منقضی شده")

    # نمایش وضعیت در لیست
    def get_list_display(self, request):
        list_display = super().get_list_display(request)
        if not request.user.has_perm('menu.view_menuview'):
            # اگر کاربر دسترسی به آمار بازدید ندارد، فیلدهای آمار را حذف کن
            list_display = [field for field in list_display if 'menu_views' not in field]
        return list_display

    # دسترسی شرطی به فیلدها
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if not request.user.has_perm('menu.view_menuview'):
            # اگر کاربر دسترسی به آمار بازدید ندارد، فیلدهای آمار را از readonly حذف کن
            readonly_fields = [field for field in readonly_fields if 'menu_views' not in field]
        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        fieldsets = super().get_fieldsets(request, obj)
        if not request.user.has_perm('menu.view_menuview'):
            # اگر کاربر دسترسی به آمار بازدید ندارد، بخش آمار را حذف کن
            fieldsets = [fieldset for fieldset in fieldsets if fieldset[0] != _('Menu View Statistics')]
        return fieldsets


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['restaurant', 'get_category_title', 'displayOrder', 'isActive', 'createdAt', 'get_image_preview']
    list_filter = ['isActive', 'restaurant', 'category', 'createdAt']
    search_fields = ['restaurant__title', 'restaurant__title_en', 'category__title', 'category__title_en', 'customTitle', 'customTitle_en']
    readonly_fields = ['createdAt', 'updatedAt', 'get_image_preview', 'get_title_display']
    list_editable = ['isActive', 'displayOrder']
    list_select_related = ['restaurant', 'category']

    def get_category_title(self, obj):
        if obj.customTitle or obj.customTitle_en:
            title_fa = obj.customTitle or '-'
            title_en = obj.customTitle_en or '-'
        else:
            title_fa = obj.category.title if obj.category else '-'
            title_en = obj.category.title_en if obj.category else '-'
        return format_html(
            '<div style="direction: rtl; text-align: right;">'
            '<strong>فارسی:</strong> {}<br>'
            '<strong>English:</strong> {}'
            '</div>',
            title_fa, title_en
        )
    get_category_title.short_description = _('Category Title')

    def get_title_display(self, obj):
        return self.get_category_title(obj)
    get_title_display.short_description = _('Title Display')

    def get_image_preview(self, obj):
        if obj.displayImage:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.displayImage.url)
        return _("No Image")
    get_image_preview.short_description = _('Image Preview')

    fieldsets = (
        (_('Basic Information'), {
            'fields': ('restaurant', 'category', 'isActive', 'displayOrder')
        }),
        (_('Custom Titles'), {
            'fields': ('get_title_display', 'customTitle', 'customTitle_en'),
            'description': _('If you want to show different titles than the main category, enter them here')
        }),
        (_('Custom Image'), {
            'fields': ('customImage', 'get_image_preview'),
            'description': _('If you want to show a different image than the main category, upload here')
        }),
        (_('Timestamps'), {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )


# ----------------------------
# FOOD ADMIN (ویرایش‌شده برای ManyToMany)
# ----------------------------
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin, BilingualAdminMixin):
    list_display = [
        'get_title_display', 'get_restaurants_list', 'menuCategory',
        'get_price_display', 'preparationTime', 'isActive', 'displayOrder', 'image_preview'
    ]
    list_filter = ['isActive', 'restaurants', 'menuCategory', 'createdAt']
    search_fields = [
        'title', 'title_en', 'description', 'description_en',
        'restaurants__title', 'restaurants__title_en'
    ]
    readonly_fields = [
        'createdAt', 'updatedAt', 'image_preview', 'sound_preview',
        'get_title_display', 'get_price_info'
    ]
    list_editable = ['preparationTime', 'isActive', 'displayOrder']
    prepopulated_fields = {"slug": ("title",)}
    list_select_related = ['menuCategory__category']

    # 🧩 نمایش لیست رستوران‌ها به صورت کاما جدا
    def get_restaurants_list(self, obj):
        return ", ".join([r.title for r in obj.restaurants.all()])
    get_restaurants_list.short_description = _('Restaurants')

    def get_price_display(self, obj):
        price_toman = f"{obj.price:,} تومان" if obj.price else _("Not set")
        price_usd = obj.formatted_price_usd or _("Not set")
        return format_html(
            '<div style="direction: rtl; text-align: right;">'
            '<strong>تومان:</strong> {}<br>'
            '<strong>USD:</strong> {}'
            '</div>',
            price_toman, price_usd
        )
    get_price_display.short_description = _('Price')

    def get_price_info(self, obj):
        exchange_rate = obj.current_exchange_rate
        return format_html(
            '<div style="direction: rtl; text-align: right; background: #f8f9fa; padding: 10px; border-radius: 5px;">'
            '<strong>نرخ ارز فعلی:</strong> {} تومان<br>'
            '<strong>قیمت تومان:</strong> {}<br>'
            '<strong>قیمت USD:</strong> {}<br>'
            '<strong>قیمت سنت:</strong> {}'
            '</div>',
            exchange_rate,
            f"{obj.price:,} تومان" if obj.price else _("Not set"),
            obj.formatted_price_usd or _("Not set"),
            f"{obj.price_usd_cents} cents" if obj.price_usd_cents else _("Not set")
        )
    get_price_info.short_description = _('Price Information')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image.url)
        return _("No Image")
    image_preview.short_description = _('Image Preview')

    def sound_preview(self, obj):
        if obj.sound:
            return format_html(
                '<audio controls style="height: 30px; width: 200px;">'
                '<source src="{}" type="audio/mpeg">'
                '{}'
                '</audio>',
                obj.sound.url, _("Your browser does not support audio")
            )
        return _("No Sound")
    sound_preview.short_description = _('Sound Preview')

    fieldsets = (
        (_('Basic Information'), {
            'fields': (
                'get_title_display', 'title', 'title_en', 'slug',
                'description', 'description_en',
                'restaurants', 'menuCategory'
            )
        }),
        (_('Pricing'), {
            'fields': ('price', 'get_price_info', 'price_usd_cents')
        }),
        (_('Time & Settings'), {
            'fields': ('preparationTime', 'isActive', 'displayOrder','created_by')
        }),
        (_('Media'), {
            'fields': ('image', 'image_preview', 'sound', 'sound_preview')
        }),
        (_('Timestamps'), {
            'fields': ('createdAt', 'updatedAt'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ['rate', 'is_active', 'created_at', 'get_food_count']
    list_editable = ['is_active']
    list_filter = ['is_active', 'created_at']

    def get_food_count(self, obj):
        count = Food.objects.filter(price__isnull=False).count()
        return f"{count} foods"
    get_food_count.short_description = _('Affected Foods')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.is_active:
            result = update_all_food_prices()
            messages.info(request, result)

    fieldsets = (
        (_('Exchange Rate Information'), {
            'fields': ('rate', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(FoodRestaurant)
class FoodRestaurantAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'restaurant_display',
        'food_display',
        'custom_price_display',
        'final_price_display',
        'custom_image_display',
        'is_active',
        'display_order',
        'created_at'
    ]

    list_filter = [
        'restaurant',
        'is_active',
        'created_at',
        'updated_at'
    ]

    search_fields = [
        'restaurant__title',
        'food__title',
        'food__description'
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
        'final_price_display',
        'final_image_display'
    ]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': (
                'restaurant',
                'food',
                'is_active',
                'display_order'
            )
        }),
        ('شخصی‌سازی', {
            'fields': (
                'custom_price',
                'custom_image',
                'final_price_display',
                'final_image_display'
            )
        }),
        ('تاریخ‌ها', {
            'fields': (
                'created_at',
                'updated_at'
            )
        }),
    )

    def restaurant_display(self, obj):
        return obj.restaurant.title
    restaurant_display.short_description = 'رستوران'

    def food_display(self, obj):
        return obj.food.title
    food_display.short_description = 'غذا'

    def custom_price_display(self, obj):
        if obj.custom_price:
            return f"{obj.custom_price:,} تومان"
        return "---"
    custom_price_display.short_description = 'قیمت کاستوم'

    def final_price_display(self, obj):
        return f"{obj.final_price:,} تومان"
    final_price_display.short_description = 'قیمت نهایی'

    def custom_image_display(self, obj):
        if obj.custom_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius: 5px;" />',
                obj.custom_image.url
            )
        return "---"
    custom_image_display.short_description = 'عکس کاستوم'

    def final_image_display(self, obj):
        if obj.final_image:
            return format_html(
                '<img src="{}" width="80" height="80" style="border-radius: 5px;" />',
                obj.final_image.url
            )
        return "---"
    final_image_display.short_description = 'عکس نهایی'

    def has_customizations_display(self, obj):
        return "✅" if obj.has_customizations() else "❌"
    has_customizations_display.short_description = 'کاستوم شده'

    actions = ['activate_selected', 'deactivate_selected', 'reset_customizations']

    def activate_selected(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, "موارد انتخاب شده فعال شدند")
    activate_selected.short_description = "فعال کردن موارد انتخاب شده"

    def deactivate_selected(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, "موارد انتخاب شده غیرفعال شدند")
    deactivate_selected.short_description = "غیرفعال کردن موارد انتخاب شده"

    def reset_customizations(self, request, queryset):
        updated_count = 0
        for obj in queryset:
            obj.custom_price = None
            obj.custom_image = None
            obj.save()
            updated_count += 1
        self.message_user(request, f"کاستومایزهای {updated_count} مورد بازنشانی شد")
    reset_customizations.short_description = "بازنشانی کاستومایزها"

    list_per_page = 25
    ordering = ['-created_at']


class SessionKeyFilter(admin.SimpleListFilter):
    title = 'نوع بازدیدکننده'
    parameter_name = 'session_type'

    def lookups(self, request, model_admin):
        return (
            ('with_session', 'با سشن'),
            ('without_session', 'بدون سشن'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'with_session':
            return queryset.exclude(session_key__isnull=True).exclude(session_key='')
        if self.value() == 'without_session':
            return queryset.filter(session_key__isnull=True) | queryset.filter(session_key='')


class IPAddressFilter(admin.SimpleListFilter):
    title = 'آدرس IP'
    parameter_name = 'ip_type'

    def lookups(self, request, model_admin):
        return (
            ('with_ip', 'با IP'),
            ('without_ip', 'بدون IP'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'with_ip':
            return queryset.exclude(ip_address__isnull=True).exclude(ip_address='')
        if self.value() == 'without_ip':
            return queryset.filter(ip_address__isnull=True) | queryset.filter(ip_address='')


@admin.register(MenuView)
class MenuViewAdmin(admin.ModelAdmin):
    list_display = [
        'restaurant_name',
        'session_short',
        'ip_short',
        'user_agent_short',
        'created_at_formatted',
        'is_recent'
    ]

    list_filter = [
        'restaurant',
        SessionKeyFilter,
        IPAddressFilter,
        'created_at',
    ]

    search_fields = [
        'restaurant__title',
        'restaurant__title_en',
        'session_key',
        'ip_address',
        'user_agent',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
        'view_duration',
        'restaurant_name',
    ]

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': (
                'restaurant_name',
                'session_key',
                'ip_address',
            )
        }),
        ('اطلاعات مرورگر', {
            'fields': (
                'user_agent',
            ),
            'classes': ('collapse',)
        }),
        ('تاریخ‌ها', {
            'fields': (
                'created_at',
                'updated_at',
                'view_duration',
            )
        }),
    )

    def restaurant_name(self, obj):
        return obj.restaurant.title
    restaurant_name.short_description = 'رستوران'
    restaurant_name.admin_order_field = 'restaurant__title'

    def session_short(self, obj):
        if obj.session_key:
            return obj.session_key[:15] + '...' if len(obj.session_key) > 15 else obj.session_key
        return 'بدون سشن'
    session_short.short_description = 'سشن'

    def ip_short(self, obj):
        return obj.ip_address or 'ندارد'
    ip_short.short_description = 'آدرس IP'

    def user_agent_short(self, obj):
        if obj.user_agent:
            return obj.user_agent[:30] + '...' if len(obj.user_agent) > 30 else obj.user_agent
        return 'ندارد'
    user_agent_short.short_description = 'مرورگر'

    def created_at_formatted(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    created_at_formatted.short_description = 'تاریخ ایجاد'
    created_at_formatted.admin_order_field = 'created_at'

    def is_recent(self, obj):
        now = timezone.now()
        if (now - obj.created_at).days < 1:
            return 'امروز'
        elif (now - obj.created_at).days < 7:
            return 'هفته جاری'
        return 'قدیمی'
    is_recent.short_description = 'وضعیت'
    is_recent.admin_order_field = 'created_at'

    def view_duration(self, obj):
        if obj.created_at and obj.updated_at:
            duration = obj.updated_at - obj.created_at
            seconds = duration.total_seconds()
            if seconds < 60:
                return f"{int(seconds)} ثانیه"
            elif seconds < 3600:
                return f"{int(seconds/60)} دقیقه"
            else:
                return f"{int(seconds/3600)} ساعت"
        return "نامشخص"
    view_duration.short_description = 'مدت بازدید'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('restaurant')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

from django.contrib import admin
from django.utils.html import format_html
from .models.menufreemodels.models import MenuPaperDesien

@admin.register(MenuPaperDesien)
class MenuPaperDesienAdmin(admin.ModelAdmin):
    # نمایش فیلدها در لیست
    list_display = ('display_image', 'title', 'is_active_display', 'createAt', 'actions_column')
    list_display_links = ('title',)  # فقط عنوان قابل کلیک باشد
    list_filter = ('isActive', 'createAt')  # فیلترهای سمت راست
    search_fields = ('title',)  # جستجو در عنوان
    list_per_page = 20  # تعداد آیتم در هر صفحه
    ordering = ('-createAt',)  # مرتب‌سازی بر اساس تاریخ (جدیدترین اول)

    # فیلدها در فرم ویرایش
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'image', 'isActive')
        }),
        ('اطلاعات زمانی', {
            'fields': ('createAt',),
            'classes': ('collapse',)  # قابل جمع شدن
        }),
    )

    # فیلدهای فقط خواندنی
    readonly_fields = ('createAt',)

    # نمایش تاریخ به صورت فارسی
    def get_readonly_fields(self, request, obj=None):
        if obj:  # در حالت ویرایش
            return self.readonly_fields + ('createAt',)
        return self.readonly_fields

    # نمایش وضعیت فعال/غیرفعال در لیست
    def is_active_display(self, obj):
        if obj.isActive:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ فعال</span>'
            )
        return format_html(
            '<span style="color: red; font-weight: bold;">✗ غیرفعال</span>'
        )
    is_active_display.short_description = 'وضعیت'

    # نمایش تصویر کوچک در لیست - از فیلد image استفاده می‌کند
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 50px; height: 50px; background: #f0f0f0; display: flex; align-items: center; justify-content: center; border-radius: 8px;">'
            '<span style="color: #999; font-size: 12px;">بدون تصویر</span>'
            '</div>'
        )
    display_image.short_description = 'تصویر'

    # ستون اقدامات سفارشی
    def actions_column(self, obj):
        return format_html(
            '<div style="display: flex; gap: 5px;">'
            '<a href="/admin/{}/{}/{}/change/" class="button" style="padding: 3px 8px; background: #417690; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">ویرایش</a>'
            '<a href="/admin/{}/{}/{}/delete/" class="button" style="padding: 3px 8px; background: #ba2121; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">حذف</a>'
            '</div>',
            obj._meta.app_label,
            obj._meta.model_name,
            obj.id,
            obj._meta.app_label,
            obj._meta.model_name,
            obj.id
        )
    actions_column.short_description = 'اقدامات'
    actions_column.allow_tags = True

    # سفارشی‌سازی ظاهر فرم
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['title'].widget.attrs.update({'style': 'width: 70%;'})
        form.base_fields['isActive'].widget.attrs.update({'style': 'width: 20px; height: 20px;'})
        # اضافه کردن preview برای تصویر در فرم
        form.base_fields['image'].widget.template_name = 'admin/widgets/clearable_file_input.html'
        return form

    # نمایش پیش‌نمایش تصویر در فرم ویرایش
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 300px; max-height: 300px; border-radius: 8px; border: 1px solid #ddd;" />',
                obj.image.url
            )
        return "تصویری موجود نیست"
    image_preview.short_description = 'پیش‌نمایش تصویر'

    # اگر می‌خواهید در فرم ویرایش، پیش‌نمایش تصویر را ببینید
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if obj and obj.image:
            # اضافه کردن فیلد پیش‌نمایش
            fields = list(fields)
            if 'image_preview' not in fields:
                fields.insert(fields.index('image') + 1, 'image_preview')
        return fields

    # افزودن اکشن‌های سفارشی
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        updated = queryset.update(isActive=True)
        self.message_user(request, f'{updated} طرح فعال شدند.')
    make_active.short_description = 'فعال کردن طرح‌های انتخاب شده'

    def make_inactive(self, request, queryset):
        updated = queryset.update(isActive=False)
        self.message_user(request, f'{updated} طرح غیرفعال شدند.')
    make_inactive.short_description = 'غیرفعال کردن طرح‌های انتخاب شده'

    # نمایش بهتر تاریخ در لیست
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs

    # متن راهنما در بالای صفحه
    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'مدیریت طرح‌های منو کاغذی'
        extra_context['description'] = 'در این بخش می‌توانید طرح‌های منو کاغذی را مدیریت کنید.'
        return super().changelist_view(request, extra_context=extra_context)

    # تغییرات مربوط به save برای مدیریت تصویر
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)