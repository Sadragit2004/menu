# models.py
from django.db import models
from django.utils import timezone
from apps.plan.models import Plan

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    price = models.PositiveIntegerField(default=0,verbose_name="قیمت محصول")
    description = models.TextField(verbose_name="توضیحات محصول")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت فعال")
    publish_date = models.DateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name

class ProductFeature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features', verbose_name="محصول")
    key = models.CharField(max_length=100, verbose_name="کلید")
    value = models.CharField(max_length=200, verbose_name="مقدار")
    slug = models.SlugField(max_length=100, verbose_name="اسلاگ")

    class Meta:
        verbose_name = "ویژگی محصول"
        verbose_name_plural = "ویژگی‌های محصول"

    def __str__(self):
        return f"{self.key}: {self.value}"

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='gallery', verbose_name="محصول")
    image = models.ImageField(upload_to='products/gallery/', verbose_name="عکس")
    alt_text = models.CharField(max_length=200, verbose_name="متن جایگزین")
    is_active = models.BooleanField(default=True, verbose_name="وضعیت")

    class Meta:
        verbose_name = "عکس گالری"
        verbose_name_plural = "گالری محصولات"

    def __str__(self):
        return f"گالری {self.product.name}"





# models.py - به‌روزرسانی مدل‌ها
from django.db import models
from django.utils import timezone
from django.db.models import Sum, F
from apps.plan.models import Plan
from apps.user.model.user import CustomUser

class ProductOrder(models.Model):
    """سفارش اصلی که شامل پلن و کاربر است"""
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name='product_orders',
        verbose_name="پلن"
    )
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='product_orders',
        verbose_name="کاربر"
    )
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    STATUS_CHOICES = [
        ('draft', 'پیش‌نویس'),
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('failed', 'ناموفق'),
        ('canceled', 'لغو شده'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name="وضعیت سفارش"
    )

    # اطلاعات مالی
    total_price = models.PositiveIntegerField(default=0, verbose_name="قیمت کل (بدون مالیات)")
    tax_amount = models.PositiveIntegerField(default=0, verbose_name="مبلغ مالیات ۹٪")  # جدید
    final_price = models.PositiveIntegerField(default=0, verbose_name="قیمت نهایی (با مالیات)")

    # اطلاعات پرداخت
    isPaid = models.BooleanField(default=False, verbose_name="پرداخت شده")
    paidAt = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ پرداخت")
    trackingCode = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="کد رهگیری"
    )

    expiryDate = models.DateTimeField(blank=True, null=True, verbose_name="تاریخ انقضا")

    class Meta:
        verbose_name = "سفارش محصول"
        verbose_name_plural = "سفارشات محصول"
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.user} - {self.plan.name} - {self.final_price}"

    def calculate_prices(self):
        """محاسبه قیمت کل، مالیات و قیمت نهایی"""
        # قیمت محصولات

        # قیمت محصولات (به تومان)
        items_total = self.items.aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total'] or 0

        self.total_price = items_total  # به تومان

        # محاسبه مالیات ۹ درصد روی مبلغ تومان
        self.tax_amount = int(self.total_price * 0.09)  # 9% مالیات به تومان

        # قیمت نهایی با احتساب مالیات (به تومان)
        self.final_price = self.total_price + self.tax_amount + self.plan.price

    def save(self, *args, **kwargs):
        # محاسبه خودکار قیمت‌ها
        self.calculate_prices()

        # تنظیم تاریخ انقضا
        if not self.expiryDate and self.plan and self.isPaid:
            self.expiryDate = timezone.now() + timezone.timedelta(days=self.plan.expiryDays)

        super().save(*args, **kwargs)

    @property
    def items_count(self):
        """تعداد کل آیتم‌های محصول در سبد"""
        return self.items.aggregate(total=Sum('quantity'))['total'] or 0

    @property
    def total_price_without_tax(self):
        """قیمت کل بدون مالیات"""
        return self.total_price

    @property
    def total_price_with_tax(self):
        """قیمت کل با مالیات"""
        return self.final_price

    def add_product(self, product, quantity=1):
        """افزودن محصول به سبد خرید"""
        item, created = ProductOrderDetail.objects.get_or_create(
            product_order=self,
            product=product,
            defaults={
                'price': product.price,
                'quantity': quantity,
                'product_name': product.name,
                'product_description': product.description
            }
        )

        if not created:
            item.quantity += quantity
            item.save()

        # بروزرسانی قیمت
        self.calculate_prices()
        self.save()

    def remove_product(self, product):
        """حذف محصول از سبد خرید"""
        try:
            item = self.items.get(product=product)
            item.delete()
            self.calculate_prices()
            self.save()
            return True
        except ProductOrderDetail.DoesNotExist:
            return False

    def update_quantity(self, product, quantity):
        """بروزرسانی تعداد محصول"""
        if quantity <= 0:
            return self.remove_product(product)

        try:
            item = self.items.get(product=product)
            item.quantity = quantity
            item.save()
            self.calculate_prices()
            self.save()
            return True
        except ProductOrderDetail.DoesNotExist:
            return False

class ProductOrderDetail(models.Model):
    """جزئیات محصولات موجود در سفارش"""
    product_order = models.ForeignKey(
        ProductOrder,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name="سفارش محصول"
    )
    product = models.ForeignKey(
        'Product',
        on_delete=models.CASCADE,
        verbose_name="محصول"
    )
    price = models.PositiveIntegerField(
        default=0,
        verbose_name="قیمت واحد"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")

    # برای مواردی که ممکن است محصول حذف شود ولی سابقه باقی بماند
    product_name = models.CharField(max_length=200, blank=True, verbose_name="نام محصول")
    product_description = models.TextField(blank=True, verbose_name="توضیحات محصول")

    class Meta:
        verbose_name = "جزئیات سفارش محصول"
        verbose_name_plural = "جزئیات سفارشات محصول"
        unique_together = ['product_order', 'product']

    def __str__(self):
        return f"{self.product.name} - {self.quantity} عدد"

    def save(self, *args, **kwargs):
        # ذخیره اطلاعات محصول برای حفظ سابقه
        if not self.product_name:
            self.product_name = self.product.name
        if not self.product_description:
            self.product_description = self.product.description
        if not self.price:
            self.price = self.product.price

        super().save(*args, **kwargs)

    @property
    def total_price(self):
        """قیمت کل این آیتم (بدون مالیات)"""
        return self.price * self.quantity

    @property
    def total_price_with_tax(self):
        """قیمت کل این آیتم با مالیات ۹٪"""
        return int((self.price * self.quantity) * 1.09)  # 9% مالیات

# models.py
class OrderDetailInfo(models.Model):
    """اطلاعات تکمیلی و ارسال سفارش"""
    product_order = models.OneToOneField(
        ProductOrder,
        on_delete=models.CASCADE,
        related_name='order_info',
        verbose_name="سفارش محصول"
    )

    # اطلاعات شخصی
    full_name = models.CharField(max_length=255, verbose_name="نام کامل")
    phone_number = models.CharField(max_length=15, verbose_name="تلفن تماس")
    email = models.EmailField(blank=True, null=True, verbose_name="ایمیل")

    # اطلاعات آدرس
    address = models.TextField(verbose_name="آدرس کامل")
    city = models.CharField(max_length=100, verbose_name="شهر")
    province = models.CharField(max_length=100, verbose_name="استان")
    codePost = models.CharField(max_length=10, verbose_name="کد پستی")

    # اطلاعات اضافی
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات اضافی")

    # اطلاعات تخفیف
    discount_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="کد تخفیف")
    discount_amount = models.PositiveIntegerField(default=0, verbose_name="مقدار تخفیف")

    created_at = models.DateTimeField(verbose_name="تاریخ ایجاد",default=timezone.now)

    class Meta:
        verbose_name = "اطلاعات تکمیلی سفارش"
        verbose_name_plural = "اطلاعات تکمیلی سفارشات"

    def __str__(self):
        return f"اطلاعات سفارش {self.product_order.id}"