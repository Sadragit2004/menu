from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime, time
import random
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.menu.models.menufreemodels.models import Restaurant
import jdatetime
from django.utils import timezone


# ----------------------------
# مدل مشتری - کاملاً مستقل از User
# ----------------------------

class Customer(models.Model):
    """
    مدل مشتری برای سیستم رزرو - کاملاً مستقل از User
    این مدل اطلاعات مشتریان رستوران را ذخیره می‌کند
    """

    # اطلاعات هویتی
    national_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="کد ملی",
        help_text="کد ملی به عنوان شناسه یکتا برای مشتری"
    )
    full_name = models.CharField(max_length=255, verbose_name="نام کامل")
    phone_number = models.CharField(max_length=15, verbose_name="شماره تماس")
    email = models.EmailField(null=True, blank=True, verbose_name="ایمیل")

    # اطلاعات اضافی
    birth_date = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="تاریخ تولد شمسی"
    )
    is_vip = models.BooleanField(default=False, verbose_name="مشتری ویژه")
    special_notes = models.TextField(null=True, blank=True, verbose_name="یادداشت‌های ویژه")

    # آمار و اطلاعات
    total_reservations = models.PositiveIntegerField(default=0, verbose_name="تعداد کل رزروها")
    successful_reservations = models.PositiveIntegerField(default=0, verbose_name="رزروهای موفق")
    cancellation_count = models.PositiveIntegerField(default=0, verbose_name="تعداد لغوها")

    # وضعیت
    is_active = models.BooleanField(default=True, verbose_name="فعال",blank=True,null=True)
    created_jalali = models.CharField(max_length=10, verbose_name="تاریخ ایجاد شمسی",blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی",blank=True,null=True)

    class Meta:
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتریان'
        ordering = ['-created_jalali']
        indexes = [
            models.Index(fields=['national_code']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['is_vip']),
        ]

    def save(self, *args, **kwargs):
        """ذخیره مشتری با تاریخ شمسی"""
        if not self.created_jalali:
            now_jalali = jdatetime.datetime.now()
            self.created_jalali = now_jalali.strftime('%Y/%m/%d')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.national_code}"

    def get_reservation_history(self):
        """دریافت تاریخچه رزروهای مشتری"""
        return self.reservations.all().order_by('-reservation_jalali_date')

    def get_success_rate(self):
        """محاسبه درصد موفقیت رزروها"""
        if self.total_reservations == 0:
            return 0
        return (self.successful_reservations / self.total_reservations) * 100


# ----------------------------
# مدل روزهای کاری - نسخه شمسی
# ----------------------------

class WorkingDay(models.Model):
    """
    مدل روزهای کاری هفته - کاملاً شمسی
    مدیریت روزهای کاری رستوران بر اساس تقویم شمسی
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

    name = models.CharField(
        max_length=20,
        choices=DAYS_OF_WEEK,
        unique=True,
        verbose_name="روز هفته"
    )
    display_order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    is_weekend = models.BooleanField(default=False, verbose_name="تعطیل آخر هفته")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        ordering = ['display_order']
        verbose_name = 'روز کاری'
        verbose_name_plural = 'روزهای کاری'

    def __str__(self):
        return self.get_name_display()

    def save(self, *args, **kwargs):
        """تنظیم خودکار تعطیلی جمعه"""
        if self.name == 'friday':
            self.is_weekend = True
        super().save(*args, **kwargs)


# ----------------------------
# مدل زمان کاری - نسخه شمسی
# ----------------------------

class WorkingTime(models.Model):
    """
    مدل زمان کاری رستوران - کاملاً شمسی
    مدیریت ساعات کاری رستوران برای هر روز
    """

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='working_times',
        verbose_name="رستوران"
    )
    day = models.ForeignKey(
        WorkingDay,
        on_delete=models.CASCADE,
        verbose_name="روز هفته"
    )
    start_time = models.TimeField(
        verbose_name="ساعت شروع کار",
        default=time(9, 0)
    )
    end_time = models.TimeField(
        verbose_name="ساعت پایان کار",
        default=time(23, 0)
    )
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    # زمان‌های استراحت
    break_start = models.TimeField(
        null=True,
        blank=True,
        verbose_name="شروع زمان استراحت"
    )
    break_end = models.TimeField(
        null=True,
        blank=True,
        verbose_name="پایان زمان استراحت"
    )

    class Meta:
        unique_together = ['restaurant', 'day']
        verbose_name = 'زمان کاری'
        verbose_name_plural = 'زمان‌های کاری'
        ordering = ['day__display_order']

    def __str__(self):
        return f"{self.restaurant.title} - {self.day.get_name_display()} - {self.start_time.strftime('%H:%M')} تا {self.end_time.strftime('%H:%M')}"

    def is_working_hour(self, check_time):
        """بررسی اینکه ساعت مورد نظر در زمان کاری است"""
        return self.start_time <= check_time <= self.end_time

    def is_break_time(self, check_time):
        """بررسی اینکه ساعت مورد نظر در زمان استراحت است"""
        if self.break_start and self.break_end:
            return self.break_start <= check_time <= self.break_end
        return False

    def get_available_time_slots(self, slot_duration_minutes=60, jalali_date=None):
        """
        تولید اسلات‌های زمانی قابل رزرو - کاملاً شمسی
        """
        slots = []

        if not jalali_date:
            jalali_date = jdatetime.date.today().strftime('%Y/%m/%d')

        # استفاده از datetime.combine با date معتبر
        today = datetime.today().date()
        current_time = datetime.combine(today, self.start_time)
        end_time_dt = datetime.combine(today, self.end_time)

        print(f"🕒 تولید اسلات از {current_time.time()} تا {end_time_dt.time()}")

        # مدیریت زمان استراحت
        break_start_dt = None
        break_end_dt = None

        if self.break_start and self.break_end:
            break_start_dt = datetime.combine(today, self.break_start)
            break_end_dt = datetime.combine(today, self.break_end)
            print(f"⏸️ زمان استراحت: {self.break_start} تا {self.break_end}")

        slot_count = 0
        while current_time + timedelta(minutes=slot_duration_minutes) <= end_time_dt:
            slot_end = current_time + timedelta(minutes=slot_duration_minutes)

            # بررسی تداخل با زمان استراحت
            is_in_break = False
            if break_start_dt and break_end_dt:
                if (current_time < break_end_dt and slot_end > break_start_dt):
                    is_in_break = True
                    # اگر در زمان استراحت هستیم، به بعد از استراحت پرش کنیم
                    current_time = break_end_dt
                    continue

            if not is_in_break:
                slots.append({
                    'start': current_time.time(),
                    'end': slot_end.time(),
                    'display': f"{current_time.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}",
                    'jalali_date': jalali_date
                })
                slot_count += 1

            current_time = slot_end

        print(f"✅ تعداد اسلات‌های تولید شده: {slot_count}")
        return slots


# ----------------------------
# مدل میز - نسخه شمسی
# ----------------------------

class Table(models.Model):
    """
    مدل میز رستوران - کاملاً شمسی
    مدیریت اطلاعات میزهای رستوران و وضعیت آن‌ها
    """

    TABLE_TYPES = [
        ('standard', 'میز استاندارد'),
        ('booth', 'میز بوث'),
        ('bar', 'میز بار'),
        ('outdoor', 'میز فضای باز'),
        ('private', 'اتاق خصوصی'),
        ('family', 'میز فامیلی'),
        ('vip', 'میز وی‌آی‌پی'),
    ]

    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='tables',
        verbose_name="رستوران"
    )
    table_number = models.CharField(max_length=50, verbose_name="شماره میز")
    table_type = models.CharField(
        max_length=20,
        choices=TABLE_TYPES,
        default='standard',
        verbose_name="نوع میز"
    )
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        verbose_name="ظرفیت (تعداد نفر)"
    )
    description = models.TextField(null=True, blank=True, verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    # مدت زمان رزرو
    min_reservation_duration = models.PositiveIntegerField(
        default=60,
        verbose_name="حداقل زمان رزرو (دقیقه)"
    )
    max_reservation_duration = models.PositiveIntegerField(
        default=240,
        verbose_name="حداکثر زمان رزرو (دقیقه)"
    )

    # ویژگی‌های میز
    has_view = models.BooleanField(default=False, verbose_name="دارای ویو")
    is_smoking = models.BooleanField(default=False, verbose_name="مجوز سیگار")
    is_vip = models.BooleanField(default=False, verbose_name="میز وی‌آی‌پی")

    # موقعیت فیزیکی
    floor = models.PositiveIntegerField(default=1, verbose_name="طبقه")
    section = models.CharField(max_length=100, blank=True, verbose_name="بخش")

    created_jalali = models.CharField(max_length=10, verbose_name="تاریخ ایجاد شمسی",blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")

    class Meta:
        unique_together = ['restaurant', 'table_number']
        ordering = ['floor', 'table_number']
        verbose_name = 'میز'
        verbose_name_plural = 'میزها'

    def save(self, *args, **kwargs):
        """ذخیره میز با تاریخ شمسی"""
        if not self.created_jalali:
            now_jalali = jdatetime.datetime.now()
            self.created_jalali = now_jalali.strftime('%Y/%m/%d')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.restaurant.title} - میز {self.table_number} (ظرفیت: {self.capacity} نفر)"

    def is_available(self, jalali_date, start_time, end_time, exclude_reservation_id=None):
        """
        بررسی می‌کند که آیا میز در بازه زمانی مشخص آزاد است - کاملاً شمسی
        """
        # نرمال‌سازی فرمت زمان
        def normalize_time(time_obj):
            if isinstance(time_obj, str):
                # اگر زمان به صورت رشته است، تبدیل به time object
                if len(time_obj) == 5:  # فرمت HH:MM
                    time_obj += ':00'
                return datetime.strptime(time_obj, '%H:%M:%S').time()
            return time_obj

        start_time = normalize_time(start_time)
        end_time = normalize_time(end_time)

        conflicting_reservations = self.reservations.filter(
            models.Q(reservation_status__in=['confirmed', 'pending', 'seated']) &
            (models.Q(reservation_jalali_date=jalali_date)) &
            (
                (models.Q(start_time__lt=end_time) & models.Q(end_time__gt=start_time)) |
                (models.Q(start_time__gte=start_time) & models.Q(start_time__lt=end_time))
            )
        )

        if exclude_reservation_id:
            conflicting_reservations = conflicting_reservations.exclude(id=exclude_reservation_id)

        return not conflicting_reservations.exists()

    def get_jalali_availability(self, jalali_date):
        """
        بررسی دسترسی میز بر اساس تاریخ شمسی
        """
        try:
            # تبدیل تاریخ شمسی به میلادی
            y, m, d = map(int, jalali_date.split('/'))
            jalali_obj = jdatetime.date(y, m, d)
            gregorian_date = jalali_obj.togregorian()
        except Exception:
            return {'available': False, 'reason': 'تاریخ نامعتبر است'}

        # گرفتن نام روز هفته نسخه جدید jdatetime (بدون weekday_name)
        weekday_str = jalali_obj.strftime("%A").lower()

        # پیدا کردن ساعت کاری آن روز
        working_time = WorkingTime.objects.filter(
            restaurant=self.restaurant,
            day__name=weekday_str,
            is_active=True
        ).first()

        if not working_time:
            return {'available': False, 'reason': 'رستوران در این روز تعطیل است'}

        # گرفتن اسلات‌های زمانی
        slots = working_time.get_available_time_slots(jalali_date=jalali_date)

        final_slots = []

        for slot in slots:
            slot_start = slot['start']
            slot_end = slot['end']

            conflict = self.reservations.filter(
                reservation_jalali_date=jalali_date,
                start_time__lt=slot_end,
                end_time__gt=slot_start,
                reservation_status__in=['pending', 'confirmed', 'seated']
            ).exists()

            if not conflict:
                final_slots.append(slot)

        if not final_slots:
            return {'available': False, 'reason': 'بدون بازه زمانی آزاد'}

        return {
            'available': True,
            'slots': final_slots,
            'working_hours': f"{working_time.start_time}-{working_time.end_time}"
        }




# ----------------------------
# مدل رزرو - نسخه کاملاً شمسی
# ----------------------------

class Reservation(models.Model):
    """
    مدل اصلی رزرو میز - کاملاً شمسی
    مدیریت کامل فرآیند رزرو با تاریخ‌های شمسی
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
    reservation_code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="کد رزرو"
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="میز"
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name="مشتری"
        ,blank=True,null=True
    )

    # اطلاعات زمانی - کاملاً شمسی
    reservation_jalali_date = models.CharField(
        max_length=10,
        verbose_name="تاریخ رزرو شمسی"
        ,blank=True,null=True
    )
    start_time = models.TimeField(verbose_name="ساعت شروع")
    end_time = models.TimeField(verbose_name="ساعت پایان")
    duration_minutes = models.PositiveIntegerField(verbose_name="مدت زمان (دقیقه)")

    # اطلاعات مهمانان
    guest_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="تعداد مهمان"
    )
    special_requests = models.TextField(
        null=True,
        blank=True,
        verbose_name="درخواست‌های ویژه"
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
    arrival_jalali_time = models.CharField(
        max_length=16,
        null=True,
        blank=True,
        verbose_name="زمان حضور شمسی"
    )

    # اطلاعات سیستمی - شمسی
    created_jalali = models.CharField(max_length=10, verbose_name="تاریخ ایجاد شمسی",blank=True,null=True)
    created_jalali_time = models.CharField(max_length=8, verbose_name="ساعت ایجاد شمسی",blank=True,null=True)
    updated_jalali = models.CharField(max_length=16, verbose_name="آخرین بروزرسانی شمسی",blank=True,null=True)

    class Meta:
        ordering = ['-created_jalali', '-start_time']
        verbose_name = 'رزرو'
        verbose_name_plural = 'رزروها'
        indexes = [
            models.Index(fields=['reservation_code']),
            models.Index(fields=['reservation_jalali_date']),
            models.Index(fields=['customer']),
            models.Index(fields=['reservation_status']),
        ]

    def save(self, *args, **kwargs):
        """
        ذخیره رزرو با تولید خودکار کدها و تاریخ‌های شمسی
        """
        # تولید کد رزرو
        if not self.reservation_code:
            self.reservation_code = self.generate_reservation_code()

        # تولید کد تأیید
        if not self.confirmation_code:
            self.confirmation_code = self.generate_confirmation_code()

        # محاسبه مدت زمان
        if self.start_time and self.end_time:
            start_dt = datetime.combine(datetime.today(), self.start_time)
            end_dt = datetime.combine(datetime.today(), self.end_time)
            self.duration_minutes = int((end_dt - start_dt).total_seconds() / 60)

        # تاریخ‌های شمسی
        now_jalali = jdatetime.datetime.now()
        if not self.created_jalali:
            self.created_jalali = now_jalali.strftime('%Y/%m/%d')
            self.created_jalali_time = now_jalali.strftime('%H:%M:%S')

        self.updated_jalali = now_jalali.strftime('%Y/%m/%d %H:%M')

        super().save(*args, **kwargs)

    def generate_reservation_code(self):
        """تولید کد رزرو 10 رقمی"""
        while True:
            chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            code = ''.join(random.choices(chars, k=8))
            full_code = f"RZ{code}"
            if not Reservation.objects.filter(reservation_code=full_code).exists():
                return full_code

    def generate_confirmation_code(self):
        """تولید کد تأیید 6 رقمی"""
        return ''.join(random.choices('0123456789', k=6))

    def get_persian_status(self):
        """دریافت وضعیت فارسی"""
        status_map = {
            'pending': 'در انتظار تایید',
            'confirmed': 'تایید شده',
            'seated': 'مشتری حاضر شد',
            'completed': 'اتمام یافته',
            'cancelled': 'لغو شده',
            'no_show': 'عدم حضور',
        }
        return status_map.get(self.reservation_status, self.reservation_status)

    def verify_confirmation_code(self, code):
        """تأیید کد ارسال شده"""
        if self.confirmation_code == code:
            self.is_verified = True
            self.save()
            return True
        return False

    def confirm_reservation(self):
        """تأیید نهایی رزرو"""
        if self.is_verified:
            self.is_confirmed = True
            self.reservation_status = 'confirmed'
            self.save()

            # به‌روزرسانی آمار مشتری
            self.customer.total_reservations += 1
            self.customer.successful_reservations += 1
            self.customer.save()

            return True
        return False

    def mark_customer_arrived(self):
        """علامت‌گذاری حضور مشتری"""
        self.customer_arrived = True
        self.arrival_jalali_time = jdatetime.datetime.now().strftime('%Y/%m/%d %H:%M')
        self.reservation_status = 'seated'
        self.save()

    def cancel_reservation(self):
        """لغو رزرو"""
        old_status = self.reservation_status
        self.reservation_status = 'cancelled'
        self.save()

        # به‌روزرسانی آمار مشتری
        if old_status in ['confirmed', 'pending']:
            self.customer.cancellation_count += 1
            self.customer.save()

    def complete_reservation(self):
        """تکمیل رزرو"""
        self.reservation_status = 'completed'
        self.save()

    @property
    def is_active(self):
        """بررسی فعال بودن رزرو"""
        return self.reservation_status in ['pending', 'confirmed', 'seated']

    @property
    def can_cancel(self):
        """بررسی امکان لغو رزرو"""
        return self.reservation_status in ['pending', 'confirmed']

    def __str__(self):
        return f"رزرو {self.reservation_code} - {self.customer.full_name} - {self.reservation_jalali_date}"


# ----------------------------
# مدل تنظیمات رزرو - نسخه شمسی
# ----------------------------

class ReservationSettings(models.Model):
    """
    مدل تنظیمات رزرو برای هر رستوران - کاملاً شمسی
    مدیریت کلیه تنظیمات مربوط به سیستم رزرو
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

    # تنظیمات خاص ایران
    friday_off = models.BooleanField(default=True, verbose_name="تعطیلی جمعه")
    thursday_evening_off = models.BooleanField(default=False, verbose_name="تعطیلی پنجشنبه عصر")
    special_holidays = models.TextField(
        blank=True,
        help_text="تاریخ‌های تعطیل خاص (هر خط یک تاریخ شمسی - فرمت: YYYY/MM/DD)",
        verbose_name="تعطیلی‌های خاص"
    )

    created_jalali = models.CharField(max_length=10, verbose_name="تاریخ ایجاد شمسی",blank=True,null=True)
    updated_jalali = models.CharField(max_length=16, verbose_name="آخرین بروزرسانی شمسی",blank=True,null=True)

    class Meta:
        verbose_name = 'تنظیمات رزرو'
        verbose_name_plural = 'تنظیمات رزروها'

    def save(self, *args, **kwargs):
        """ذخیره تنظیمات با تاریخ شمسی"""
        now_jalali = jdatetime.datetime.now()
        if not self.created_jalali:
            self.created_jalali = now_jalali.strftime('%Y/%m/%d')
        self.updated_jalali = now_jalali.strftime('%Y/%m/%d %H:%M')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"تنظیمات رزرو - {self.restaurant.title}"

    def get_special_holidays_list(self):
        """دریافت لیست تعطیلی‌های خاص"""
        if self.special_holidays:
            return [date.strip() for date in self.special_holidays.split('\n') if date.strip()]
        return []

    def is_holiday(self, jalali_date):
        """بررسی اینکه تاریخ شمسی تعطیل است یا نه"""
        # بررسی جمعه
        if self.friday_off:
            try:
                year, month, day = map(int, jalali_date.split('/'))
                jalali_obj = jdatetime.JalaliDate(year, month, day)
                if jalali_obj.weekday() == 6:  # جمعه
                    return True
            except (ValueError, AttributeError):
                pass

        # بررسی تعطیلی‌های خاص
        if jalali_date in self.get_special_holidays_list():
            return True

        return False


# ----------------------------
# توابع کمکی - نسخه شمسی
# ----------------------------

def get_available_tables(restaurant, jalali_date, start_time, end_time, guest_count):
    """
    دریافت لیست میزهای آزاد بر اساس تاریخ شمسی
    """
    available_tables = Table.objects.filter(
        restaurant=restaurant,
        is_active=True,
        capacity__gte=guest_count
    ).exclude(
        reservations__in=Reservation.objects.filter(
            reservation_jalali_date=jalali_date,
            reservation_status__in=['confirmed', 'pending', 'seated'],
            start_time__lt=end_time,
            end_time__gt=start_time
        )
    )

    return available_tables

def create_jalali_reservation(restaurant, table, customer, jalali_date, start_time, end_time, guest_count, special_requests=''):
    """
    ایجاد رزرو جدید با تاریخ شمسی
    """
    # اعتبارسنجی اولیه
    if not table.is_available(jalali_date, start_time, end_time):
        return None, "میز در این بازه زمانی آزاد نیست"

    if table.capacity < guest_count:
        return None, "ظرفیت میز کمتر از تعداد مهمان است"

    # ایجاد رزرو
    reservation = Reservation(
        table=table,
        customer=customer,
        reservation_jalali_date=jalali_date,
        start_time=start_time,
        end_time=end_time,
        guest_count=guest_count,
        special_requests=special_requests
    )

    reservation.save()
    return reservation, "رزرو با موفقیت ایجاد شد"

def get_jalali_week_range():
    """
    دریافت محدوده هفته جاری شمسی
    """
    today = jdatetime.date.today()
    start_of_week = today - jdatetime.timedelta(days=today.weekday())
    end_of_week = start_of_week + jdatetime.timedelta(days=6)

    return {
        'start': start_of_week.strftime('%Y/%m/%d'),
        'end': end_of_week.strftime('%Y/%m/%d'),
        'today': today.strftime('%Y/%m/%d')
    }