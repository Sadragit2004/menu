from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime
import random
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.menu.models.menufreemodels.models import Restaurant

# ----------------------------
# Working Time & Days
# ----------------------------

class WorkingDay(models.Model):
    """
    مدل روزهای کاری هفته
    کاربرد: ذخیره روزهای هفته برای تنظیم برنامه کاری رستوران
    """
    DAYS_OF_WEEK = [
        ('saturday', 'شنبه'),
        ('sunday', 'یکشنبه'),
        ('monday', 'دوشنبه'),
        ('tuesday', 'سه شنبه'),
        ('wednesday', 'چهارشنبه'),
        ('thursday', 'پنجشنبه'),
        ('friday', 'جمعه'),
    ]

    name = models.CharField(max_length=20, choices=DAYS_OF_WEEK, unique=True, verbose_name="روز هفته")
    display_order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['display_order']
        verbose_name = 'روز کاری'
        verbose_name_plural = 'روزهای کاری'

    def __str__(self):
        return self.get_name_display()

class WorkingTime(models.Model):
    """
    مدل زمان کاری رستوران
    کاربرد: تنظیم ساعات کاری رستوران برای هر روز
    """
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='working_times', verbose_name="رستوران")
    day = models.ForeignKey(WorkingDay, on_delete=models.CASCADE, verbose_name="روز هفته")
    start_time = models.TimeField(verbose_name="ساعت شروع")
    end_time = models.TimeField(verbose_name="ساعت پایان")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        unique_together = ['restaurant', 'day']
        verbose_name = 'زمان کاری'
        verbose_name_plural = 'زمان‌های کاری'
        ordering = ['day__display_order', 'start_time']

    def __str__(self):
        return f"{self.restaurant.title} - {self.day.get_name_display()} - {self.start_time} تا {self.end_time}"

    def get_time_slots(self, slot_duration_minutes=120):
        """
        تولید اسلات‌های زمانی بر اساس مدت زمان مشخص
        کاربرد: ایجاد بازه‌های زمانی برای رزرو
        """
        slots = []
        current_time = datetime.combine(datetime.today(), self.start_time)
        end_time = datetime.combine(datetime.today(), self.end_time)

        while current_time + timedelta(minutes=slot_duration_minutes) <= end_time:
            slot_end = current_time + timedelta(minutes=slot_duration_minutes)
            slots.append({
                'start': current_time.time(),
                'end': slot_end.time()
            })
            current_time = slot_end

        return slots

# ----------------------------
# Table Model
# ----------------------------

class Table(models.Model):
    """
    مدل میز رستوران
    کاربرد: مدیریت میزهای رستوران و مشخصات آنها
    """
    TABLE_TYPES = [
        ('standard', 'استاندارد'),
        ('booth', 'بخ'),
        ('bar', 'بار'),
        ('outdoor', 'فضای باز'),
        ('private', 'اتاق خصوصی'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='tables', verbose_name="رستوران")
    table_number = models.CharField(max_length=50, verbose_name="شماره میز")
    table_type = models.CharField(max_length=20, choices=TABLE_TYPES, default='standard', verbose_name="نوع میز")
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        verbose_name="ظرفیت (تعداد نفر)"
    )
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    min_reservation_duration = models.PositiveIntegerField(
        default=60,
        help_text="حداقل زمان رزرو به دقیقه",
        verbose_name="حداقل زمان رزرو"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['restaurant', 'table_number']
        ordering = ['table_number']
        verbose_name = 'میز'
        verbose_name_plural = 'میزها'

    def __str__(self):
        return f"{self.restaurant.title} - میز {self.table_number}"

    def is_available(self, start_time, end_time, exclude_reservation_id=None):
        """
        بررسی می‌کند که آیا میز در بازه زمانی مشخص آزاد است
        کاربرد: اعتبارسنجی قبل از رزرو
        """
        conflicting_reservations = self.reservations.filter(
            models.Q(reservation_status__in=['confirmed', 'pending']) &
            (
                (models.Q(start_time__lt=end_time) & models.Q(end_time__gt=start_time)) |
                (models.Q(start_time__gte=start_time) & models.Q(start_time__lt=end_time))
            )
        )

        if exclude_reservation_id:
            conflicting_reservations = conflicting_reservations.exclude(id=exclude_reservation_id)

        return not conflicting_reservations.exists()

    def get_availability_for_date(self, date):
        """
        دریافت وضعیت دسترسی میز برای یک تاریخ خاص
        کاربرد: نمایش زمان‌های آزاد در تقویم
        """
        # پیدا کردن روز هفته مربوطه
        weekday_map = {
            5: 'saturday',    # شنبه
            6: 'sunday',      # یکشنبه
            0: 'monday',      # دوشنبه
            1: 'tuesday',     # سه شنبه
            2: 'wednesday',   # چهارشنبه
            3: 'thursday',    # پنجشنبه
            4: 'friday',      # جمعه
        }

        day_name = weekday_map[date.weekday()]
        working_time = self.restaurant.working_times.filter(
            day__name=day_name,
            is_active=True
        ).first()

        if not working_time:
            return {'available': False, 'slots': [], 'reason': 'رستوران در این روز تعطیل است'}

        # دریافت رزروهای موجود برای این تاریخ
        reservations = self.reservations.filter(
            reservation_date=date,
            reservation_status__in=['confirmed', 'pending']
        )

        # تولید اسلات‌های زمانی
        time_slots = working_time.get_time_slots(self.min_reservation_duration)
        available_slots = []

        for slot in time_slots:
            slot_start = datetime.combine(date, slot['start'])
            slot_end = datetime.combine(date, slot['end'])

            # بررسی تداخل با رزروهای موجود
            is_occupied = reservations.filter(
                models.Q(start_time__lt=slot_end.time()) &
                models.Q(end_time__gt=slot_start.time())
            ).exists()

            if not is_occupied:
                available_slots.append({
                    'start': slot['start'],
                    'end': slot['end'],
                    'display': f"{slot['start'].strftime('%H:%M')} - {slot['end'].strftime('%H:%M')}"
                })

        return {
            'available': len(available_slots) > 0,
            'slots': available_slots,
            'working_hours': {
                'start': working_time.start_time,
                'end': working_time.end_time
            }
        }

# ----------------------------
# Reservation Models
# ----------------------------

class Reservation(models.Model):
    """
    مدل اصلی رزرو میز
    کاربرد: ذخیره اطلاعات کامل رزرو
    """
    RESERVATION_STATUS = [
        ('pending', 'در انتظار تایید'),
        ('confirmed', 'تایید شده'),
        ('seated', 'مشتری حاضر شد'),
        ('completed', 'اتمام یافته'),
        ('cancelled', 'لغو شده'),
        ('no_show', 'عدم حضور'),
    ]

    # اطلاعات رزرو
    reservation_code = models.CharField(max_length=10, unique=True, verbose_name="کد رزرو")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations', verbose_name="میز")

    # اطلاعات زمانی
    reservation_date = models.DateField(verbose_name="تاریخ رزرو")
    start_time = models.TimeField(verbose_name="ساعت شروع")
    end_time = models.TimeField(verbose_name="ساعت پایان")
    duration_minutes = models.PositiveIntegerField(verbose_name="مدت زمان (دقیقه)")

    # اطلاعات مشتری
    customer_full_name = models.CharField(max_length=255, verbose_name="نام کامل مشتری")
    customer_phone = models.CharField(max_length=15, verbose_name="شماره تماس مشتری")
    special_requests = models.TextField(null=True, blank=True, verbose_name="درخواست‌های ویژه")
    guest_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="تعداد مهمان"
    )

    # وضعیت رزرو
    reservation_status = models.CharField(
        max_length=20,
        choices=RESERVATION_STATUS,
        default='pending',
        verbose_name="وضعیت رزرو"
    )

    # تأیید و حضور
    is_confirmed = models.BooleanField(default=False, verbose_name="تایید شده")
    confirmation_code = models.CharField(max_length=6, verbose_name="کد تأیید")
    is_verified = models.BooleanField(default=False, verbose_name="تأیید شده با کد")
    customer_arrived = models.BooleanField(default=False, verbose_name="مشتری حاضر شد")
    arrival_time = models.DateTimeField(null=True, blank=True, verbose_name="زمان حضور")

    # اطلاعات سیستمی
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'رزرو'
        verbose_name_plural = 'رزروها'
        indexes = [
            models.Index(fields=['reservation_code']),
            models.Index(fields=['customer_phone']),
            models.Index(fields=['reservation_date', 'start_time']),
        ]

    def save(self, *args, **kwargs):
        """
        ذخیره رزرو با تولید خودکار کدها
        کاربرد: تولید کد رزرو و کد تأیید قبل از ذخیره
        """
        if not self.reservation_code:
            self.reservation_code = self.generate_reservation_code()

        if not self.confirmation_code:
            self.confirmation_code = self.generate_confirmation_code()

        # محاسبه مدت زمان
        if self.start_time and self.end_time:
            start_dt = datetime.combine(self.reservation_date, self.start_time)
            end_dt = datetime.combine(self.reservation_date, self.end_time)
            self.duration_minutes = int((end_dt - start_dt).total_seconds() / 60)

        super().save(*args, **kwargs)

    def generate_reservation_code(self):
        """
        تولید کد رزرو 10 رقمی
        کاربرد: ایجاد شناسه یکتا برای رزرو
        """
        while True:
            code = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))
            if not Reservation.objects.filter(reservation_code=code).exists():
                return code

    def generate_confirmation_code(self):
        """
        تولید کد تأیید 6 رقمی
        کاربرد: ارسال برای تأیید شماره تماس
        """
        return ''.join(random.choices('0123456789', k=6))

    def verify_confirmation_code(self, code):
        """
        تأیید کد ارسال شده
        کاربرد: اعتبارسنجی کد تأیید مشتری
        """
        if self.confirmation_code == code:
            self.is_verified = True
            self.save()
            return True
        return False

    def confirm_reservation(self):
        """
        تأیید نهایی رزرو
        کاربرد: تغییر وضعیت رزرو به تأیید شده
        """
        if self.is_verified:
            self.is_confirmed = True
            self.reservation_status = 'confirmed'
            self.save()
            return True
        return False

    def mark_customer_arrived(self):
        """
        علامت‌گذاری حضور مشتری
        کاربرد: زمانی که مشتری در رستوران حاضر می‌شود
        """
        self.customer_arrived = True
        self.arrival_time = timezone.now()
        self.reservation_status = 'seated'
        self.save()

    def mark_no_show(self):
        """
        علامت‌گذاری عدم حضور مشتری
        کاربرد: زمانی که مشتری در زمان مقرر حاضر نمی‌شود
        """
        self.reservation_status = 'no_show'
        self.save()

    def cancel_reservation(self):
        """
        لغو رزرو
        کاربرد: آزاد کردن میز برای رزروهای دیگر
        """
        self.reservation_status = 'cancelled'
        self.save()

    def complete_reservation(self):
        """
        تکمیل رزرو
        کاربرد: پس از اتمام زمان رزرو
        """
        self.reservation_status = 'completed'
        self.save()

    @property
    def is_active(self):
        """
        بررسی فعال بودن رزرو
        کاربرد: تشخیص رزروهای جاری و آینده
        """
        return self.reservation_status in ['pending', 'confirmed', 'seated']

    @property
    def can_cancel(self):
        """
        بررسی امکان لغو رزرو
        کاربرد: نمایش دکمه لغو در رابط کاربری
        """
        return self.reservation_status in ['pending', 'confirmed']

    @property
    def time_until_reservation(self):
        """
        محاسبه زمان تا رزرو
        کاربرد: نمایش زمان باقی‌مانده
        """
        now = timezone.now()
        reservation_dt = timezone.make_aware(
            datetime.combine(self.reservation_date, self.start_time)
        )
        return reservation_dt - now if reservation_dt > now else timedelta(0)

    def __str__(self):
        return f"رزرو {self.reservation_code} - {self.customer_full_name}"

# ----------------------------
# Reservation Settings
# ----------------------------

class ReservationSettings(models.Model):
    """
    مدل تنظیمات رزرو برای هر رستوران
    کاربرد: مدیریت قوانین و محدودیت‌های رزرو
    """
    restaurant = models.OneToOneField(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='reservation_settings',
        verbose_name="رستوران"
    )

    # تنظیمات عمومی
    max_advance_days = models.PositiveIntegerField(
        default=30,
        verbose_name="حداکثر روزهای پیش‌رو برای رزرو"
    )
    min_advance_hours = models.PositiveIntegerField(
        default=2,
        verbose_name="حداقل ساعت‌های پیش‌رو برای رزرو"
    )
    max_guests_per_reservation = models.PositiveIntegerField(
        default=20,
        verbose_name="حداکثر تعداد مهمان در هر رزرو"
    )

    # تنظیمات زمان
    default_reservation_duration = models.PositiveIntegerField(
        default=120,
        verbose_name="مدت زمان پیش‌فرض رزرو (دقیقه)"
    )
    slot_duration = models.PositiveIntegerField(
        default=30,
        verbose_name="مدت زمان هر اسلات (دقیقه)"
    )

    # تنظیمات تأیید
    auto_confirm_reservations = models.BooleanField(
        default=False,
        verbose_name="تأیید خودکار رزروها"
    )
    require_phone_verification = models.BooleanField(
        default=True,
        verbose_name="نیاز به تأیید شماره تماس"
    )

    # محدودیت‌ها
    max_reservations_per_time_slot = models.PositiveIntegerField(
        default=1,
        verbose_name="حداکثر رزرو همزمان در هر اسلات"
    )
    allow_same_day_reservations = models.BooleanField(
        default=True,
        verbose_name="اجازه رزرو در همان روز"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'تنظیمات رزرو'
        verbose_name_plural = 'تنظیمات رزروها'

    def __str__(self):
        return f"تنظیمات رزرو - {self.restaurant.title}"

# ----------------------------
# Helper Functions
# ----------------------------

def get_available_tables(restaurant, date, start_time, end_time, guest_count):
    """
    دریافت لیست میزهای آزاد
    کاربرد: جستجوی میزهای قابل رزرو بر اساس معیارها
    """
    available_tables = Table.objects.filter(
        restaurant=restaurant,
        is_active=True,
        capacity__gte=guest_count
    ).exclude(
        reservations__in=Reservation.objects.filter(
            reservation_date=date,
            reservation_status__in=['confirmed', 'pending', 'seated'],
            start_time__lt=end_time,
            end_time__gt=start_time
        )
    )

    return available_tables

def create_reservation(restaurant, table, customer_data, date, start_time, end_time):
    """
    ایجاد رزرو جدید
    کاربرد: ایجاد رزرو با اعتبارسنجی کامل
    """
    # اعتبارسنجی اولیه
    if not table.is_available(date, start_time, end_time):
        return None, "میز در این بازه زمانی آزاد نیست"

    if table.capacity < customer_data['guest_count']:
        return None, "ظرفیت میز کمتر از تعداد مهمان است"

    # ایجاد رزرو
    reservation = Reservation(
        table=table,
        reservation_date=date,
        start_time=start_time,
        end_time=end_time,
        customer_full_name=customer_data['full_name'],
        customer_phone=customer_data['phone'],
        guest_count=customer_data['guest_count'],
        special_requests=customer_data.get('special_requests', '')
    )

    reservation.save()
    return reservation, "رزرو با موفقیت ایجاد شد"