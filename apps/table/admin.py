# table/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import WorkingDay, WorkingTime, Table, Reservation, ReservationSettings

# ----------------------------
# Admin Customizations
# ----------------------------

class WorkingTimeInline(admin.TabularInline):
    """
    اینلاین برای نمایش ساعات کاری در پنل رستوران
    """
    model = WorkingTime
    extra = 0
    fields = ['day', 'start_time', 'end_time', 'is_active']
    ordering = ['day__display_order']

class TableInline(admin.TabularInline):
    """
    اینلاین برای نمایش میزها در پنل رستوران
    """
    model = Table
    extra = 0
    fields = ['table_number', 'table_type', 'capacity', 'is_active']
    ordering = ['table_number']

# ----------------------------
# Working Day Admin
# ----------------------------

@admin.register(WorkingDay)
class WorkingDayAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای روزهای کاری
    """
    list_display = ['name_display', 'display_order', 'is_used']
    list_editable = ['display_order']
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
    list_display = ['restaurant', 'day_display', 'start_time', 'end_time', 'is_active', 'duration']
    list_filter = ['restaurant', 'day', 'is_active']
    list_editable = ['is_active']
    search_fields = ['restaurant__title', 'day__name']
    ordering = ['restaurant', 'day__display_order']

    def day_display(self, obj):
        return obj.day.get_name_display()
    day_display.short_description = 'روز'

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
        'restaurant',
        'table_type_display',
        'capacity',
        'is_active',
        'reservation_count',
        'created_at'
    ]
    list_filter = [
        'restaurant',
        'table_type',
        'is_active',
        'created_at'
    ]
    list_editable = ['is_active', 'capacity']
    search_fields = [
        'table_number',
        'restaurant__title',
        'description'
    ]
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['restaurant', 'table_number']

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': (
                'restaurant',
                'table_number',
                'table_type',
                'capacity',
                'min_reservation_duration'
            )
        }),
        ('توضیحات و وضعیت', {
            'fields': (
                'description',
                'is_active'
            )
        }),
        ('تاریخ‌ها', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

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
        'created_at'
    ]

    list_filter = [
        ReservationStatusFilter,
        'reservation_date',
        'is_confirmed',
        'customer_arrived',
        'table__restaurant',
        'created_at'
    ]

    list_editable = ['is_confirmed']

    search_fields = [
        'reservation_code',
        'customer_full_name',
        'customer_phone',
        'table__table_number',
        'table__restaurant__title'
    ]

    readonly_fields = [
        'reservation_code',
        'confirmation_code',
        'duration_minutes',
        'created_at',
        'updated_at',
        'arrival_time'
    ]

    ordering = ['-created_at']

    fieldsets = (
        ('اطلاعات رزرو', {
            'fields': (
                'reservation_code',
                'table',
                'reservation_date',
                'start_time',
                'end_time',
                'duration_minutes',
                'guest_count'
            )
        }),
        ('اطلاعات مشتری', {
            'fields': (
                'customer_full_name',
                'customer_phone',
                'special_requests'
            )
        }),
        ('وضعیت و تأیید', {
            'fields': (
                'reservation_status',
                'is_confirmed',
                'confirmation_code',
                'is_verified',
                'customer_arrived',
                'arrival_time'
            )
        }),
        ('تاریخ‌ها', {
            'fields': (
                'created_at',
                'updated_at'
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
            '<strong>{}</strong><br><small>{}</small>',
            obj.customer_full_name,
            obj.customer_phone
        )
    customer_info.short_description = 'مشتری'

    def table_info(self, obj):
        return format_html(
            'میز {}<br><small>{}</small>',
            obj.table.table_number,
            obj.table.restaurant.title
        )
    table_info.short_description = 'میز'

    def date_time_info(self, obj):
        return format_html(
            '{}<br><small>{} - {}</small>',
            obj.reservation_date,
            obj.start_time,
            obj.end_time
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
            obj.get_reservation_status_display()
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
        updated = queryset.filter(reservation_status='confirmed').update(
            reservation_status='seated',
            customer_arrived=True,
            arrival_time=timezone.now()
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
        return super().get_queryset(request).select_related('table', 'table__restaurant')

# ----------------------------
# Reservation Settings Admin
# ----------------------------

@admin.register(ReservationSettings)
class ReservationSettingsAdmin(admin.ModelAdmin):
    """
    پنل ادمین برای تنظیمات رزرو
    """
    list_display = [
        'restaurant',
        'max_advance_days',
        'min_advance_hours',
        'max_guests_per_reservation',
        'auto_confirm_reservations',
        'updated_at'
    ]

    list_filter = [
        'auto_confirm_reservations',
        'require_phone_verification',
        'allow_same_day_reservations'
    ]

    search_fields = ['restaurant__title']

    readonly_fields = ['created_at', 'updated_at']

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
        ('تاریخ‌ها', {
            'fields': (
                'created_at',
                'updated_at'
            ),
            'classes': ('collapse',)
        }),
    )

# ----------------------------
# Admin Site Customization
# ----------------------------


# گروه‌بندی مدل‌ها در پنل ادمین
from django.contrib.admin import AdminSite

class TableAdminSite(AdminSite):
    site_header = 'مدیریت سیستم رزرو'
    site_title = 'پنل مدیریت رزرو'
    index_title = 'مدیریت رزرو میزهای رستوران'

# اگر می‌خواهید پنل جداگانه داشته باشید:
# table_admin_site = TableAdminSite(name='table_admin')
# table_admin_site.register(WorkingDay, WorkingDayAdmin)
# table_admin_site.register(WorkingTime, WorkingTimeAdmin)
# table_admin_site.register(Table, TableAdmin)
# table_admin_site.register(Reservation, ReservationAdmin)
# table_admin_site.register(ReservationSettings, ReservationSettingsAdmin)