# apps/peyment/models.py
from django.db import models
from apps.user.models import CustomUser
from django.utils import timezone
from apps.order.models import Ordermenu
import utils
import jdatetime



class Peyment(models.Model):
    PAYMENT_TYPES = [
        ('menu', 'منو'),
        ('plan', 'پلن'),
        ('product', 'محصول'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'در انتظار پرداخت'),
        ('success', 'پرداخت موفق'),
        ('failed', 'پرداخت ناموفق'),
        ('canceled', 'لغو شده'),
    ]

    # فیلدهای اصلی
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='peyment_customer', verbose_name='مشتری')
    createAt = models.DateTimeField(default=timezone.now, verbose_name="تاریخ ساخته شده")
    updateAt = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    amount = models.IntegerField(verbose_name='مبلغ پرداخت')
    description = models.TextField(verbose_name='توضیحات پرداخت')
    isFinaly = models.BooleanField(default=False, verbose_name='وضعیت پرداخت')
    statusCode = models.IntegerField(verbose_name='کد وضعیت پرداخت', null=True, blank=True)
    refId = models.CharField(max_length=50, verbose_name='کد پیگیری پرداخت', null=True, blank=True)

    # فیلدهای جدید برای یکپارچه‌سازی
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default='menu', verbose_name="نوع پرداخت")
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending', verbose_name="وضعیت پرداخت")

    # فیلدهای مرتبط با هر نوع سفارش
    order = models.ForeignKey(Ordermenu, on_delete=models.CASCADE, related_name='peyment_order', verbose_name='سفارش منو', null=True, blank=True)
    plan_order_id = models.IntegerField(null=True, blank=True, verbose_name='شناسه سفارش پلن')
    product_order_id = models.IntegerField(null=True, blank=True, verbose_name='شناسه سفارش محصول')

    def get_jalali_register_date(self):
        return jdatetime.datetime.fromgregorian(datetime=self.createAt).strftime('%Y/%m/%d')

    def get_related_order_info(self):
        """اطلاعات سفارش مرتبط"""
        if self.payment_type == 'menu' and self.order:
            return f"منو: {self.order.restaurant.name}"
        elif self.payment_type == 'plan' and self.plan_order_id:
            return f"پلن: #{self.plan_order_id}"
        elif self.payment_type == 'product' and self.product_order_id:
            return f"محصول: #{self.product_order_id}"
        return "نامشخص"

    def __str__(self) -> str:
        return f'{self.get_payment_type_display()} - {self.customer} - {self.amount:,} تومان'

    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت ها'