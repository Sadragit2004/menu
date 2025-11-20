# table/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import WorkingDay, WorkingTime, Table, Reservation, ReservationSettings, Customer

# ----------------------------
# Customer Admin
# ----------------------------

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای مشتریان
    """
    list_display = [
        'national_code',
        'full_name',
        'phone_number',
        'is_vip',
        'total_reservations',
        'success_rate_display',
        'created_jalali'
    ]

    list_filter = [
        'is_vip',
        'is_active',
        'created_jalali'
    ]

    list_editable = ['is_vip']

    search_fields = [
        'national_code',
        'full_name',
        'phone_number'
    ]

    readonly_fields = [
        'total_reservations',
        'successful_reservations',
        'cancellation_count',
        'created_jalali',
        'updated_at'
    ]

    ordering = ['-created_jalali']

    fieldsets = (
        ('اطلاعات هویتی', {
            'fields': (
                'national_code',
                'full_name',
                'phone_number',
                'email'
            )
        }),
        ('اطلاعات اضافی', {
            'fields': (
                'birth_date',
                'is_vip',
                'special_notes'
            )
        }),
        ('آمار رزرو', {
            'fields': (
                'total_reservations',
                'successful_reservations',
                'cancellation_count',
            )
        }),
        ('وضعیت', {
            'fields': (
                'is_active',
                'created_jalali',
                'updated_at'
            )
        }),
    )

    def success_rate_display(self, obj):
        rate = obj.get_success_rate()
        color = 'green' if rate >= 80 else 'orange' if rate >= 60 else 'red'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}%</span>',
            color,
            rate
        )
    success_rate_display.short_description = 'نرخ موفقیت'

# ----------------------------
# Working Day Admin
# ----------------------------

@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای روزهای کاری
    """
    list_display = ['name_display', 'display_order', 'is_weekend', 'is_active', 'is_used']
    list_editable = ['display_order', 'is_active']
    ordering = ['display_order']
    search_fields = ['name']

    def name_display(self, obj):
        return obj.get_name_display()
    name_display.short_description = 'روز هفته'

    def is_used(self, obj):
        return obj.workingtime_set.exists()
    is_used.short_description = 'استفاده شده'
    is_used.boolean = True

# ----------------------------
# Working Time Admin
# ----------------------------

@admin.register(WorkingTime)
class WorkingTimeAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای ساعات کاری
    """
    list_display = ['restaurant_name', 'day_name', 'start_time_display', 'end_time_display', 'is_active', 'duration']
    list_filter = ['restaurant', 'day', 'is_active']
    list_editable = ['is_active']
    search_fields = ['restaurant__title', 'day__name']
    ordering = ['restaurant', 'day__display_order']

    def restaurant_name(self, obj):
        return obj.restaurant.title
    restaurant_name.short_description = 'رستوران'

    def day_name(self, obj):
        return obj.day.get_name_display()
    day_name.short_description = 'روز'

    def start_time_display(self, obj):
        return obj.start_time.strftime('%H:%M') if obj.start_time else '-'
    start_time_display.short_description = 'ساعت شروع'

    def end_time_display(self, obj):
        return obj.end_time.strftime('%H:%M') if obj.end_time else '-'
    end_time_display.short_description = 'ساعت پایان'

    def duration(self, obj):
        if obj.start_time and obj.end_time:
            from datetime import datetime
            start = datetime.combine(datetime.today(), obj.start_time)
            end = datetime.combine(datetime.today(), obj.end_time)
            duration = end - start
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60
            return f"{hours} ساعت و {minutes} دقیقه"
        return "-"
    duration.short_description = 'مدت زمان'

# ----------------------------
# Table Admin
# ----------------------------

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای میزها
    """
    list_display = [
        'table_number',
        'restaurant_name',
        'table_type_display',
        'capacity',
        'is_active',
        'reservation_count',
        'created_jalali'
    ]

    list_filter = [
        'restaurant',
        'table_type',
        'is_active',
        'created_jalali'
    ]

    list_editable = ['is_active', 'capacity']

    search_fields = [
        'table_number',
        'restaurant__title',
        'description'
    ]

    readonly_fields = ['created_jalali', 'updated_at']

    ordering = ['restaurant', 'table_number']

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': (
                'restaurant',
                'table_number',
                'table_type',
                'capacity',
                'description'
            )
        }),
        ('مدت زمان رزرو', {
            'fields': (
                'min_reservation_duration',
                'max_reservation_duration'
            )
        }),
        ('ویژگی‌های میز', {
            'fields': (
                'has_view',
                'is_smoking',
                'is_vip',
                'floor',
                'section'
            )
        }),
        ('وضعیت', {
            'fields': (
                'is_active',
                'created_jalali',
                'updated_at'
            )
        }),
    )

    def restaurant_name(self, obj):
        return obj.restaurant.title
    restaurant_name.short_description = 'رستوران'

    def table_type_display(self, obj):
        return obj.get_table_type_display()
    table_type_display.short_description = 'نوع میز'

    def reservation_count(self, obj):
        count = obj.reservations.count()
        url = f"/admin/table/reservation/?table__id__exact={obj.id}"
        return format_html('<a href="{}">{} رزرو</a>', url, count)
    reservation_count.short_description = 'تعداد رزروها'

# ----------------------------
# Reservation Admin
# ----------------------------

class ReservationStatusFilter(admin.SimpleListFilter):
    """
    فیلتر وضعیت رزرو
    """
    title = 'وضعیت رزرو'
    parameter_name = 'reservation_status'

    def lookups(self, request, model_admin):
        return Reservation.RESERVATION_STATUS

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(reservation_status=self.value())
        return queryset

class JalaliDateFilter(admin.SimpleListFilter):
    """
    فیلتر تاریخ شمسی
    """
    title = 'تاریخ رزرو شمسی'
    parameter_name = 'reservation_jalali_date'

    def lookups(self, request, model_admin):
        # لیست تاریخ‌های منحصربه‌فرد برای فیلتر
        dates = Reservation.objects.values_list('reservation_jalali_date', flat=True).distinct().order_by('-reservation_jalali_date')[:10]
        return [(date, date) for date in dates]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(reservation_jalali_date=self.value())
        return queryset

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای رزروها
    """
    list_display = [
        'reservation_code',
        'customer_info',
        'table_info',
        'date_time_info',
        'guest_count',
        'status_display',
        'is_confirmed',
        'customer_arrived',
        'created_jalali'
    ]

    list_filter = [
        ReservationStatusFilter,
        JalaliDateFilter,
        'is_confirmed',
        'customer_arrived',
        'table__restaurant',
        'created_jalali'
    ]

    list_editable = ['is_confirmed']

    search_fields = [
        'reservation_code',
        'customer__full_name',
        'customer__phone_number',
        'table__table_number',
        'table__restaurant__title'
    ]

    readonly_fields = [
        'reservation_code',
        'confirmation_code',
        'duration_minutes',
        'created_jalali',
        'created_jalali_time',
        'updated_jalali',
        'arrival_jalali_time'
    ]

    ordering = ['-created_jalali', '-start_time']

    fieldsets = (
        ('اطلاعات رزرو', {
            'fields': (
                'reservation_code',
                'table',
                'reservation_jalali_date',
                'start_time',
                'end_time',
                'duration_minutes',
                'guest_count',
                'special_requests'
            )
        }),
        ('اطلاعات مشتری', {
            'fields': (
                'customer',
            )
        }),
        ('وضعیت و تأیید', {
            'fields': (
                'reservation_status',
                'is_confirmed',
                'confirmation_code',
                'is_verified',
                'customer_arrived',
                'arrival_jalali_time'
            )
        }),
        ('تاریخ‌های شمسی', {
            'fields': (
                'created_jalali',
                'created_jalali_time',
                'updated_jalali'
            ),
            'classes': ('collapse',)
        }),
    )

    actions = [
        'confirm_selected_reservations',
        'cancel_selected_reservations',
        'mark_as_seated',
        'mark_as_completed'
    ]

    def customer_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>{}</small><br><small>کدملی: {}</small>',
            obj.customer.full_name,
            obj.customer.phone_number,
            obj.customer.national_code
        )
    customer_info.short_description = 'مشتری'

    def table_info(self, obj):
        return format_html(
            'میز {}<br><small>{}</small><br><small>ظرفیت: {}</small>',
            obj.table.table_number,
            obj.table.restaurant.title,
            obj.table.capacity
        )
    table_info.short_description = 'میز'

    def date_time_info(self, obj):
        return format_html(
            '{}<br><small>{} - {}</small><br><small>مدت: {} دقیقه</small>',
            obj.reservation_jalali_date,
            obj.start_time.strftime('%H:%M'),
            obj.end_time.strftime('%H:%M'),
            obj.duration_minutes
        )
    date_time_info.short_description = 'تاریخ و زمان'

    def status_display(self, obj):
        status_colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'seated': 'green',
            'completed': 'gray',
            'cancelled': 'red',
            'no_show': 'purple'
        }
        color = status_colors.get(obj.reservation_status, 'gray')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_persian_status()
        )
    status_display.short_description = 'وضعیت'

    # اکشن‌های سفارشی
    def confirm_selected_reservations(self, request, queryset):
        updated = queryset.filter(reservation_status='pending').update(
            reservation_status='confirmed',
            is_confirmed=True
        )
        self.message_user(request, f'{updated} رزرو تأیید شد.')
    confirm_selected_reservations.short_description = 'تأیید رزروهای انتخاب شده'

    def cancel_selected_reservations(self, request, queryset):
        updated = queryset.filter(reservation_status__in=['pending', 'confirmed']).update(
            reservation_status='cancelled'
        )
        self.message_user(request, f'{updated} رزرو لغو شد.')
    cancel_selected_reservations.short_description = 'لغو رزروهای انتخاب شده'

    def mark_as_seated(self, request, queryset):
        from django.utils import timezone
        import jdatetime

        now_jalali = jdatetime.datetime.now().strftime('%Y/%m/%d %H:%M')
        updated = queryset.filter(reservation_status='confirmed').update(
            reservation_status='seated',
            customer_arrived=True,
            arrival_jalali_time=now_jalali
        )
        self.message_user(request, f'{updated} رزرو به وضعیت حاضر تغییر یافت.')
    mark_as_seated.short_description = 'علامت‌گذاری به عنوان حاضر'

    def mark_as_completed(self, request, queryset):
        updated = queryset.filter(reservation_status__in=['confirmed', 'seated']).update(
            reservation_status='completed'
        )
        self.message_user(request, f'{updated} رزرو تکمیل شد.')
    mark_as_completed.short_description = 'علامت‌گذاری به عنوان تکمیل شده'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'table',
            'table__restaurant',
            'customer'
        )

# ----------------------------
# Reservation Settings Admin
# ----------------------------

@admin.register(ReservationSettings)
class ReservationSettingsAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای تنظیمات رزرو
    """
    list_display = [
        'restaurant_name',
        'max_advance_days',
        'min_advance_hours',
        'max_guests_per_reservation',
        'auto_confirm_reservations',
        'updated_jalali'
    ]

    list_filter = [
        'auto_confirm_reservations',
        'require_phone_verification',
        'allow_same_day_reservations',
        'friday_off'
    ]

    search_fields = ['restaurant__title']

    readonly_fields = ['created_jalali', 'updated_jalali']

    fieldsets = (
        ('تنظیمات عمومی', {
            'fields': (
                'restaurant',
                'max_advance_days',
                'min_advance_hours',
                'max_guests_per_reservation'
            )
        }),
        ('تنظیمات زمانی', {
            'fields': (
                'default_reservation_duration',
                'slot_duration'
            )
        }),
        ('تنظیمات تأیید', {
            'fields': (
                'auto_confirm_reservations',
                'require_phone_verification'
            )
        }),
        ('محدودیت‌ها', {
            'fields': (
                'max_reservations_per_time_slot',
                'allow_same_day_reservations'
            )
        }),
        ('تعطیلی‌ها', {
            'fields': (
                'friday_off',
                'thursday_evening_off',
                'special_holidays'
            )
        }),
        ('تاریخ‌های شمسی', {
            'fields': (
                'created_jalali',
                'updated_jalali'
            ),
            'classes': ('collapse',)
        }),
    )

    def restaurant_name(self, obj):
        return obj.restaurant.title
    restaurant_name.short_description = 'رستوران'