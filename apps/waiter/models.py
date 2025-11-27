from django.db import models
from django.utils import timezone
from decimal import Decimal
import uuid
from apps.user.validators.mobile_validator import validate_iranian_mobile
from apps.menu.models.menufreemodels.models import Restaurant,Food,FoodRestaurant
# ----------------------------
# Waiter Model
# ----------------------------
class Waiter(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='waiters',
        verbose_name="رستوران"
    )
    fullname = models.CharField(max_length=255, verbose_name="نام کامل")
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="کد گارسون"
    )
    mobileNumber = models.CharField(
        max_length=11,
        validators=[validate_iranian_mobile],
        verbose_name="شماره موبایل"
    )
    age = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="سن"
    )
    description = models.TextField(
        null=True,
        blank=True,
        verbose_name="توضیحات"
    )
    isActive = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )
    createdAt = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updatedAt = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )

    class Meta:
        verbose_name = 'گارسون'
        verbose_name_plural = 'گارسون‌ها'
        ordering = ['-createdAt']
        unique_together = ['restaurant', 'code']

    def __str__(self):
        return f"{self.fullname} - {self.code} - {self.restaurant.title}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        """تولید کد منحصر به فرد برای گارسون"""
        base_code = f"W{self.restaurant.id:03d}"
        counter = 1
        code = f"{base_code}{counter:03d}"

        while Waiter.objects.filter(code=code).exclude(id=self.id).exists():
            counter += 1
            code = f"{base_code}{counter:03d}"

        return code

    @property
    def active_orders_count(self):
        """تعداد سفارش‌های فعال گارسون"""
        return self.orders.filter(status__in=['pending', 'preparing', 'ready']).count()

    @property
    def today_orders_count(self):
        """تعداد سفارش‌های امروز گارسون"""
        today = timezone.now().date()
        return self.orders.filter(createdAt__date=today).count()

    def can_accept_new_order(self):
        """بررسی می‌کند که آیا گارسون می‌تواند سفارش جدید بپذیرد"""
        max_orders = getattr(settings, 'MAX_ORDERS_PER_WAITER', 10)
        return self.active_orders_count < max_orders

# ----------------------------
# Order Item Model (برای آیتم‌های سفارش)
# ----------------------------
class OrderItem(models.Model):
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        verbose_name="غذا"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="تعداد"
    )
    custom_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="قیمت کاستوم"
    )
    notes = models.TextField(
        null=True,
        blank=True,
        verbose_name="یادداشت‌ها"
    )

    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'

    def __str__(self):
        return f"{self.food.title} x {self.quantity}"

    @property
    def final_price(self):
        """قیمت نهایی آیتم"""
        if self.custom_price:
            return self.custom_price
        return self.food.price

    @property
    def total_price(self):
        """قیمت کل آیتم (قیمت × تعداد)"""
        return self.final_price * self.quantity

    def get_final_food_data(self, restaurant):
        """دریافت اطلاعات نهایی غذا با در نظر گرفتن شخصی‌سازی‌ها"""
        return FoodRestaurant.get_final_food_data(restaurant, self.food)

# ----------------------------
# Order Model
# ----------------------------
class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'در انتظار تایید'),
        ('confirmed', 'تایید شده'),
        ('preparing', 'در حال آماده‌سازی'),
        ('ready', 'آماده'),
        ('served', 'سرو شده'),
        ('cancelled', 'لغو شده'),
        ('paid', 'پرداخت شده'),
    ]

    # اطلاعات پایه
    session_key = models.CharField(
        max_length=255,
        verbose_name="کلید سشن",
        help_text="برای شناسایی مشتری بدون نیاز به لاگین"
    )
    restaurant = models.ForeignKey(
       Restaurant,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="رستوران"
    )
    waiter = models.ForeignKey(
        'Waiter',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders',
        verbose_name="گارسون"
    )

    # آیتم‌های سفارش
    items = models.ManyToManyField(
        OrderItem,
        related_name='orders',
        verbose_name="آیتم‌های سفارش"
    )

    # وضعیت سفارش
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending',
        verbose_name="وضعیت"
    )

    # اطلاعات مالی
    total_price = models.PositiveIntegerField(
        default=0,
        verbose_name="قیمت کل"
    )
    tax_amount = models.PositiveIntegerField(
        default=0,
        verbose_name="مبلغ مالیات"
    )
    final_price = models.PositiveIntegerField(
        default=0,
        verbose_name="قیمت نهایی"
    )

    # اطلاعات سفارش
    table_number = models.CharField(
        max_length=10,
        null=True,
        blank=True,
        verbose_name="شماره میز"
    )
    customer_notes = models.TextField(
        null=True,
        blank=True,
        verbose_name="یادداشت مشتری"
    )

    # زمان‌ها
    createdAt = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاریخ ایجاد"
    )
    updatedAt = models.DateTimeField(
        auto_now=True,
        verbose_name="تاریخ بروزرسانی"
    )
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان تایید"
    )
    prepared_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان آماده‌سازی"
    )
    served_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="زمان سرو"
    )

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
        ordering = ['-createdAt']
        indexes = [
            models.Index(fields=['session_key', 'restaurant']),
            models.Index(fields=['status', 'createdAt']),
            models.Index(fields=['waiter', 'status']),
        ]

    def __str__(self):
        return f"Order #{self.id} - {self.restaurant.title} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        """محاسبه خودکار قیمت‌ها قبل از ذخیره"""
        if not self.pk or kwargs.get('update_prices', True):
            self.calculate_prices()
        super().save(*args, **kwargs)

    def calculate_prices(self):
        """محاسبه قیمت‌های سفارش"""
        items_total = sum(item.total_price for item in self.items.all())
        self.total_price = items_total
        self.tax_amount = int(items_total * (self.restaurant.taxRate / 100))
        self.final_price = self.total_price + self.tax_amount

    def add_item(self, food, quantity=1, custom_price=None, notes=None):
        """افزودن آیتم به سفارش"""
        order_item = OrderItem.objects.create(
            food=food,
            quantity=quantity,
            custom_price=custom_price,
            notes=notes
        )
        self.items.add(order_item)
        self.calculate_prices()
        self.save(update_prices=False)

    def update_status(self, new_status, commit=True):
        """بروزرسانی وضعیت سفارش"""
        old_status = self.status
        self.status = new_status

        # ثبت زمان‌های مربوط به وضعیت
        now = timezone.now()
        if new_status == 'confirmed' and old_status != 'confirmed':
            self.confirmed_at = now
        elif new_status == 'preparing' and old_status != 'preparing':
            self.prepared_at = now
        elif new_status == 'served' and old_status != 'served':
            self.served_at = now

        if commit:
            self.save(update_prices=False)

    @property
    def preparation_time(self):
        """مدت زمان آماده‌سازی سفارش"""
        if self.prepared_at and self.confirmed_at:
            return self.prepared_at - self.confirmed_at
        return None

    @property
    def serving_time(self):
        """مدت زمان سرو سفارش"""
        if self.served_at and self.prepared_at:
            return self.served_at - self.prepared_at
        return None

    @property
    def total_preparation_time(self):
        """زمان کل آماده‌سازی غذاها"""
        return max(item.food.preparationTime for item in self.items.all()) if self.items.exists() else 0

    @classmethod
    def get_cart_for_session(cls, session_key, restaurant):
        """دریافت سبد خرید برای سشن و رستوران مشخص"""
        cart, created = cls.objects.get_or_create(
            session_key=session_key,
            restaurant=restaurant,
            status='pending',
            defaults={'total_price': 0, 'tax_amount': 0, 'final_price': 0}
        )
        return cart

    @classmethod
    def get_active_orders_for_restaurant(cls, restaurant):
        """دریافت سفارش‌های فعال رستوران"""
        return cls.objects.filter(
            restaurant=restaurant,
            status__in=['pending', 'confirmed', 'preparing', 'ready']
        ).select_related('waiter').prefetch_related('items__food')

    @classmethod
    def get_today_orders_for_restaurant(cls, restaurant):
        """دریافت سفارش‌های امروز رستوران"""
        today = timezone.now().date()
        return cls.objects.filter(
            restaurant=restaurant,
            createdAt__date=today
        )

# ----------------------------
# Waiter Assignment Model (برای مدیریت انتساب گارسون‌ها)
# ----------------------------
class WaiterAssignment(models.Model):
    waiter = models.ForeignKey(
        Waiter,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="گارسون"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name="سفارش"
    )
    assigned_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="زمان انتساب"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    class Meta:
        verbose_name = 'انتساب گارسون'
        verbose_name_plural = 'انتساب‌های گارسون'
        ordering = ['-assigned_at']
        unique_together = ['waiter', 'order']

    def __str__(self):
        return f"{self.waiter.fullname} - Order #{self.order.id}"

# ----------------------------
# توابع و utility functions
# ----------------------------
def assign_waiter_to_order(order, waiter=None):
    """
    انتساب گارسون به سفارش
    اگر گارسون مشخص نشده باشد، به صورت خودکار انتخاب می‌شود
    """
    if not waiter:
        # انتخاب گارسون با کمترین سفارش فعال
        waiters = Waiter.objects.filter(
            restaurant=order.restaurant,
            isActive=True
        ).annotate(
            active_orders_count=models.Count(
                'orders',
                filter=models.Q(orders__status__in=['pending', 'confirmed', 'preparing', 'ready'])
            )
        ).order_by('active_orders_count')

        if waiters.exists():
            waiter = waiters.first()
        else:
            return None, "هیچ گارسون فعالی در این رستوران وجود ندارد"

    if not waiter.can_accept_new_order():
        return None, "گارسون انتخابی نمی‌تواند سفارش جدید بپذیرد"

    if waiter.restaurant != order.restaurant:
        return None, "گارسون متعلق به این رستوران نیست"

    order.waiter = waiter
    order.save()

    # ایجاد رکورد انتساب
    WaiterAssignment.objects.create(waiter=waiter, order=order)

    return waiter, "گارسون با موفقیت به سفارش انتساب یافت"

def get_restaurant_waiters_status(restaurant):
    """
    دریافت وضعیت گارسون‌های یک رستوران
    """
    waiters = Waiter.objects.filter(
        restaurant=restaurant,
        isActive=True
    ).annotate(
        active_orders_count=models.Count(
            'orders',
            filter=models.Q(orders__status__in=['pending', 'confirmed', 'preparing', 'ready'])
        ),
        today_orders_count=models.Count(
            'orders',
            filter=models.Q(orders__createdAt__date=timezone.now().date())
        )
    ).order_by('active_orders_count')

    return waiters

def create_order_from_cart(session_key, restaurant, table_number=None, customer_notes=None):
    """
    ایجاد سفارش از سبد خرید
    """
    try:
        cart = Order.get_cart_for_session(session_key, restaurant)

        if not cart.items.exists():
            return None, "سبد خرید خالی است"

        # بروزرسانی اطلاعات سفارش
        cart.table_number = table_number
        cart.customer_notes = customer_notes
        cart.update_status('confirmed')

        # انتساب خودکار گارسون
        waiter, message = assign_waiter_to_order(cart)

        return cart, f"سفارش با موفقیت ایجاد شد. {message}"

    except Exception as e:
        return None, f"خطا در ایجاد سفارش: {str(e)}"

# ----------------------------
# سیگنال‌ها (اختیاری - برای عملکردهای پیشرفته)
# ----------------------------
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Order)
def order_status_changed(sender, instance, **kwargs):
    """
    ارسال نوتیفیکیشن هنگام تغییر وضعیت سفارش
    (برای پیاده‌سازی سوکت)
    """
    # اینجا می‌توانید کد ارسال نوتیفیکیشن از طریق WebSocket را اضافه کنید
    pass