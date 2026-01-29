import os
from uuid import uuid4
from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from apps.user.model.user import CustomUser
from django.utils.translation import gettext as _
from django.conf import settings
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
import utils

# ----------------------------
# Upload helpers
# ----------------------------
def upload_to_category(instance, filename):
    name, ext = os.path.splitext(filename)
    return f'categories/images/{uuid4()}{ext}'


def upload_to_restaurant_logo(instance, filename):
    name, ext = os.path.splitext(filename)
    return f'restaurants/logos/{uuid4()}{ext}'


def upload_to_restaurant_cover(instance, filename):
    name, ext = os.path.splitext(filename)
    return f'restaurants/covers/{uuid4()}{ext}'


def upload_to_menu_category(instance, filename):
    name, ext = os.path.splitext(filename)
    return f'restaurants/menu-categories/images/{uuid4()}{ext}'


def upload_to_food_image(instance, filename):
    name, ext = os.path.splitext(filename)
    return f'foods/images/{uuid4()}{ext}'


def upload_to_food_sound(instance, filename):
    name, ext = os.path.splitext(filename)
    return f'sound/menu/{uuid4()}{ext}'


def upload_to_food_restaurant_image(instance, filename):
    name, ext = os.path.splitext(filename)
    return f'restaurants/foods/images/{uuid4()}{ext}'


# ----------------------------
# Base abstract model
# ----------------------------
class BaseModel(models.Model):

    title = models.CharField(max_length=255, null=True, blank=True, verbose_name="عنوان فارسی")
    title_en = models.CharField(max_length=255, null=True, blank=True, verbose_name="عنوان انگلیسی")
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    isActive = models.BooleanField(default=True, null=True, blank=True)
    displayOrder = models.IntegerField(default=0, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['displayOrder']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_title = self.title_en or self.title or "item"
            base_slug = slugify(base_title)
            slug = base_slug
            counter = 1
            while self.__class__.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.title_en or ''

    def get_title(self, lang):
        if lang == 'en':
            return self.title_en or self.title or ''
        return self.title or self.title_en or ''

    def get_description(self, lang='fa'):
        if hasattr(self, 'description') and hasattr(self, 'description_en'):
            if lang == 'en':
                return self.description_en or self.description or ''
            return self.description or self.description_en or ''
        return ''


# ----------------------------
# Category
# ----------------------------
class Category(BaseModel):

    image = models.ImageField(upload_to=upload_to_category, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta(BaseModel.Meta):
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    @property
    def is_parent(self):
        return self.children.exists()

    @property
    def active_subcategories(self):
        return self.children.filter(isActive=True)

    def get_all_subcategories(self):
        subcategories = []
        for child in self.children.filter(isActive=True):
            subcategories.append(child)
            subcategories.extend(child.get_all_subcategories())
        return subcategories



class MenuPaperDesien(models.Model):

    title = models.CharField(verbose_name='عنوان طرخ',max_length=200)
    imageFile = utils.FileUpload('images','paperMenu')
    image = models.ImageField(upload_to=imageFile.upload_to,verbose_name='عکس',null=True,blank=True)
    isActive = models.BooleanField(default=True,verbose_name='وضعیت فعال')
    createAt = models.DateTimeField(default=timezone.now,verbose_name='تاریخ ثبت')


    def __str__(self):
        return f'{self.title}\t{self.createAt}'





# ----------------------------
# Restaurant
# ----------------------------
from django.utils import timezone
from datetime import timedelta

class Restaurant(BaseModel):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='restaurants', null=True, blank=True)
    english_name = models.CharField(max_length=255, unique=True, null=True, blank=True, help_text="نام انگلیسی برای تولید اسلاگ")
    description = models.TextField(null=True, blank=True, verbose_name="توضیح فارسی")
    description_en = models.TextField(null=True, blank=True, verbose_name="توضیح انگلیسی")
    logo = models.ImageField(upload_to=upload_to_restaurant_logo, null=True, blank=True)
    coverImage = models.ImageField(upload_to=upload_to_restaurant_cover, null=True, blank=True)
    text = RichTextUploadingField(verbose_name=('متن'),default='خالی')
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    address_en = models.TextField(null=True, blank=True, verbose_name="آدرس انگلیسی")
    openingTime = models.TimeField(null=True, blank=True)
    closingTime = models.TimeField(null=True, blank=True)
    minimumOrder = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    deliveryFee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    taxRate = models.DecimalField(max_digits=5, decimal_places=2, default=9.0, null=True, blank=True)
    freeSmoke = models.BooleanField(default=False,verbose_name='ازادی سیگار')
    isSeo = models.BooleanField(default=False,verbose_name='ایا سئو شده',blank=True,null=True)
    expireDate = models.DateTimeField(null=True, blank=True, verbose_name="تاریخ انقضا")

    # Toggle Settings
    show_usd_price = models.BooleanField(default=False, verbose_name="نمایش قیمت دلار")
    show_preparation_time = models.BooleanField(default=True, verbose_name="نمایش زمان آماده‌سازی")
    menu_active = models.BooleanField(default=True, verbose_name="منو فعال")

    def save(self, *args, **kwargs):
        if self.openingTime == "":
            self.openingTime = None
        if self.closingTime == "":
            self.closingTime = None


        if not self.slug and self.english_name:
            base_slug = slugify(self.english_name)
            slug = base_slug
            counter = 1
            while Restaurant.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or self.title_en or self.english_name or "Restaurant"

    def get_address(self, lang='fa'):
        if lang == 'en':
            return self.address_en or self.address or ''
        return self.address or self.address_en or ''

    @property
    def is_expired(self):
        if not self.expireDate:
            return False
        return timezone.now() > self.expireDate

    @property
    def days_until_expiry(self):
        if not self.expireDate:
            return None
        now = timezone.now()
        if now > self.expireDate:
            return 0
        return (self.expireDate - now).days

    @property
    def expiry_status(self):
        if not self.expireDate:
            return "بدون تاریخ انقضا"
        if self.is_expired:
            return "منقضی شده"
        days_left = self.days_until_expiry
        if days_left <= 7:
            return f"در آستانه انقضا ({days_left} روز باقی مانده)"
        return f"فعال ({days_left} روز باقی مانده)"

    def extend_expiry(self, days):
        try:
            days = int(days)
            if days <= 0:
                return False, "تعداد روز باید بیشتر از صفر باشد"

            now = timezone.now()

            if not self.expireDate or self.is_expired:
                new_expire_date = now + timedelta(days=days)
            else:
                new_expire_date = self.expireDate + timedelta(days=days)

            self.expireDate = new_expire_date
            self.save()
            return True, f"تاریخ انقضا با موفقیت {days} روز تمدید شد"

        except ValueError:
            return False, "تعداد روز باید یک عدد معتبر باشد"
        except Exception as e:
            return False, f"خطا در تمدید: {str(e)}"

    def set_expiry_from_today(self, days):
        try:
            days = int(days)
            if days <= 0:
                return False, "تعداد روز باید بیشتر از صفر باشد"

            self.expireDate = timezone.now() + timedelta(days=days)
            self.save()
            return True, f"تاریخ انقضا با موفقیت برای {days} روز دیگر تنظیم شد"

        except ValueError:
            return False, "تعداد روز باید یک عدد معتبر باشد"
        except Exception as e:
            return False, f"خطا در تنظیم تاریخ انقضا: {str(e)}"

    def get_expiry_display(self, lang='fa'):
        if not self.expireDate:
            return "بدون تاریخ انقضا" if lang == 'fa' else "No expiry date"

        from django.utils.formats import date_format
        expire_date_local = timezone.localtime(self.expireDate)

        if lang == 'en':
            return f"Expires on: {date_format(expire_date_local, 'DATETIME_FORMAT')}"
        else:
            return f"تاریخ انقضا: {date_format(expire_date_local, 'DATETIME_FORMAT')}"

    @classmethod
    def get_expired_restaurants(cls):
        return cls.objects.filter(expireDate__lt=timezone.now())

    @classmethod
    def get_active_restaurants(cls):
        return cls.objects.filter(
            models.Q(expireDate__isnull=True) |
            models.Q(expireDate__gte=timezone.now())
        )

    @classmethod
    def get_expiring_soon_restaurants(cls, days=7):
        threshold = timezone.now() + timedelta(days=days)
        return cls.objects.filter(
            expireDate__gte=timezone.now(),
            expireDate__lte=threshold
        )




class RequestToCreatePaperMenu(models.Model):

    # وضعیت‌های ممکن
    STATUS_CHOICES = [
        ('pending', 'در انتظار'),
        ('confirmed', 'تایید شده'),
        ('delivered', 'تحویل شده'),
        ('rejected', 'رد شده'),
    ]

    paper = models.ForeignKey(
        'MenuPaperDesien',
        verbose_name='طرح منو',
        on_delete=models.CASCADE
    )

    restaurant = models.ForeignKey(
        'Restaurant',
        verbose_name='رستوران',
        on_delete=models.CASCADE
    )

    text_content = models.TextField(
        verbose_name='متن محتوا',
        blank=True,
        null=True
    )

    # فیلد وضعیت
    status = models.CharField(
        verbose_name='وضعیت درخواست',
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    # فیلد عکس بک‌گراند
    background_image = models.ImageField(
        verbose_name='عکس بک‌گراند',
        upload_to='paper_menu_backgrounds/',
        blank=True,
        null=True,
        help_text='تصویر زمینه منو را آپلود کنید'
    )

    # فیلدهای تاریخ برای ردیابی
    created_at = models.DateTimeField(
        verbose_name='تاریخ ایجاد',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name='تاریخ بروزرسانی',
        auto_now=True
    )

    class Meta:
        verbose_name = 'درخواست ایجاد منو کاغذی'
        verbose_name_plural = 'درخواست‌های ایجاد منو کاغذی'

    def __str__(self):
        return f'درخواست منو {self.paper} برای {self.restaurant}'





# ----------------------------
# Menu Category
# ----------------------------
class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menuCategories', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    customTitle = models.CharField(max_length=255, null=True, blank=True, verbose_name="عنوان سفارشی فارسی")
    customTitle_en = models.CharField(max_length=255, null=True, blank=True, verbose_name="عنوان سفارشی انگلیسی")
    customImage = models.ImageField(upload_to=upload_to_menu_category, null=True, blank=True)
    displayOrder = models.IntegerField(default=0, null=True, blank=True)
    isActive = models.BooleanField(default=True, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updatedAt = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['displayOrder']
        unique_together = ['restaurant', 'category']
        verbose_name = 'Menu Category'
        verbose_name_plural = 'Menu Categories'

    def __str__(self):
        title = self.customTitle or (self.category.title if self.category else "")
        return f"{self.restaurant.title if self.restaurant else 'No Restaurant'} - {title}"

    @property
    def displayImage(self):
        return self.customImage if self.customImage else (self.category.image if self.category else None)

    def get_title(self, lang='fa'):
        title_fa = self.customTitle or (self.category.title if self.category else None)
        title_en = self.customTitle_en or (self.category.title_en if self.category else None)
        if lang == 'en':
            return title_en or title_fa or ""
        return title_fa or title_en or ""


# ----------------------------
# Food
# ----------------------------
class Food(BaseModel):
    restaurants = models.ManyToManyField(
        'Restaurant',
        related_name='foods',
        blank=True,
        verbose_name='رستوران‌ها'
    )
    menuCategory = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='foods', null=True, blank=True)
    description = models.TextField(null=True, blank=True, verbose_name="توضیح فارسی")
    description_en = models.TextField(null=True, blank=True, verbose_name="توضیح انگلیسی")
    image = models.ImageField(upload_to=upload_to_food_image, null=True, blank=True)
    sound = models.FileField(upload_to=upload_to_food_sound, null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True, verbose_name="قیمت (تومان)")
    price_usd_cents = models.PositiveIntegerField(null=True, blank=True, verbose_name="قیمت (سنت)")
    preparationTime = models.IntegerField(help_text="زمان آماده‌سازی (دقیقه)", null=True, blank=True)
    created_by = models.CharField(
        max_length=20,
        choices=[('company', 'شرکت'), ('restaurant', 'رستوران')],
        default='restaurant',
        verbose_name="ایجاد شده توسط"
    )

    class Meta:
        ordering = ['displayOrder']

    def save(self, *args, **kwargs):
        if self.price is not None and self.price_usd_cents is None:
            self.update_usd_price()

        if not self.slug and (self.title or self.title_en):
            base_slug = slugify(self.title_en or self.title)
            slug = base_slug
            counter = 1
            while Food.objects.filter(slug=slug).exclude(id=self.id).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)

    def is_selected_by_restaurant(self, restaurant):
        return self.restaurants.filter(id=restaurant.id).exists()

    def toggle_for_restaurant(self, restaurant):
        if self.restaurants.filter(id=restaurant.id).exists():
            self.restaurants.remove(restaurant)
            return False
        else:
            self.restaurants.add(restaurant)
            return True

    def update_usd_price(self, exchange_rate=None):
        if self.price is not None:
            if exchange_rate is None:
                exchange_rate = get_current_exchange_rate()
            if exchange_rate and exchange_rate > 0:
                usd_amount = Decimal(self.price) / Decimal(exchange_rate)
                self.price_usd_cents = int(usd_amount * 100)
            else:
                self.price_usd_cents = 0
        else:
            self.price_usd_cents = None

    @property
    def price_usd(self):
        if self.price_usd_cents is not None:
            return Decimal(self.price_usd_cents) / Decimal(100)
        return None

    @property
    def formatted_price_usd(self):
        if self.price_usd is not None:
            return f"${self.price_usd:.2f}"
        return None

    @property
    def current_exchange_rate(self):
        return get_current_exchange_rate()

    @property
    def is_customizable(self):
        """آیا این غذا قابل کاستومایز توسط رستوران‌ها است؟"""
        return self.created_by == 'company'

    def get_price_display(self, lang='fa'):
        if lang == 'en':
            if self.price_usd_cents:
                usd_amount = Decimal(self.price_usd_cents) / Decimal(100)
                return f"${usd_amount:.2f}"
            elif self.price:
                exchange_rate = get_current_exchange_rate()
                if exchange_rate:
                    usd_amount = Decimal(self.price) / Decimal(exchange_rate)
                    return f"${usd_amount:.2f}"
            return "$0.00"
        else:
            from django.contrib.humanize.templatags.humanize import intcomma
            return f"{intcomma(self.price or 0)} تومان"

    def __str__(self):
        return self.title or self.title_en or "Food"




class FoodRestaurant(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='custom_foods',
        verbose_name="رستوران"
    )
    food = models.ForeignKey(
        Food,
        on_delete=models.CASCADE,
        related_name='custom_restaurants',
        verbose_name="غذا"
    )

    # فیلدهای کاستومایز
    custom_price = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="قیمت کاستوم (تومان)"
    )
    custom_image = models.ImageField(
        upload_to=upload_to_food_restaurant_image,
        null=True,
        blank=True,
        verbose_name="عکس کاستوم"
    )

    # فیلدهای مدیریتی
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    display_order = models.IntegerField(default=0, verbose_name="ترتیب نمایش")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'restaurant_food_restaurant'
        verbose_name = 'غذای کاستوم رستوران'
        verbose_name_plural = 'غذاهای کاستوم رستوران'
        ordering = ['display_order', 'created_at']
        unique_together = ['restaurant', 'food']

    def __str__(self):
        return f"{self.restaurant.title} - {self.food.title}"

    def save(self, *args, **kwargs):
        """ولیدیشن: فقط غذاهای ایجاد شده توسط شرکت قابل کاستومایز هستند"""
        if self.food.created_by != 'company':
            raise ValueError("فقط غذاهای ایجاد شده توسط شرکت قابل کاستومایز هستند")
        super().save(*args, **kwargs)

    # property های اصلی
    @property
    def final_price(self):
        """قیمت نهایی - اولویت با قیمت کاستوم است"""
        return self.custom_price if self.custom_price is not None else self.food.price

    @property
    def final_image(self):
        """عکس نهایی - اولویت با عکس کاستوم است"""
        return self.custom_image if self.custom_image else self.food.image

    def get_final_price_display(self, lang='fa'):
        """نمایش قیمت نهایی"""
        if lang == 'en':
            if self.final_price:
                exchange_rate = get_current_exchange_rate()
                if exchange_rate:
                    usd_amount = Decimal(self.final_price) / Decimal(exchange_rate)
                    return f"${usd_amount:.2f}"
            return "$0.00"
        else:
            from django.contrib.humanize.templatags.humanize import intcomma
            return f"{intcomma(self.final_price or 0)} تومان"

    def has_customizations(self):
        """بررسی می‌کند که آیا این غذا کاستومایز شده است"""
        return self.custom_price is not None or self.custom_image is not None

    def reset_customizations(self):
        """بازنشانی تمام کاستومایزها به مقادیر پیش‌فرض"""
        self.custom_price = None
        self.custom_image = None
        self.save()

    @classmethod
    def get_customizable_foods_for_restaurant(cls, restaurant):
        """لیست غذاهای قابل کاستومایز برای یک رستوران"""
        return Food.objects.filter(
            created_by='company',
            isActive=True
        ).exclude(
            custom_restaurants__restaurant=restaurant
        )

    @classmethod
    def create_custom_food(cls, restaurant, food, custom_price=None, custom_image=None):
        """ایجاد غذای کاستوم برای رستوران"""
        if food.created_by != 'company':
            raise ValueError("فقط غذاهای ایجاد شده توسط شرکت قابل کاستومایز هستند")

        return cls.objects.create(
            restaurant=restaurant,
            food=food,
            custom_price=custom_price,
            custom_image=custom_image
        )

    @classmethod
    def get_final_food_data(cls, restaurant, food):
        """
        دریافت اطلاعات نهایی غذا با در نظر گرفتن شخصی‌سازی‌ها
        """
        try:
            custom_food = cls.objects.get(restaurant=restaurant, food=food)
            return {
                'id': food.id,
                'title': food.title,
                'title_en': food.title_en,
                'description': food.description,
                'description_en': food.description_en,
                'price': custom_food.final_price,
                'image': custom_food.final_image,
                'preparationTime': food.preparationTime,
                'isActive': custom_food.is_active and food.isActive,
                'menuCategory': food.menuCategory,
                'slug': food.slug,
                'displayOrder': custom_food.display_order,
                'is_customized': custom_food.has_customizations(),
                'custom_food_id': custom_food.id
            }
        except cls.DoesNotExist:
            return {
                'id': food.id,
                'title': food.title,
                'title_en': food.title_en,
                'description': food.description,
                'description_en': food.description_en,
                'price': food.price,
                'image': food.image,
                'preparationTime': food.preparationTime,
                'isActive': food.isActive,
                'menuCategory': food.menuCategory,
                'slug': food.slug,
                'displayOrder': food.displayOrder,
                'is_customized': False,
                'custom_food_id': None
            }

# ----------------------------
# Exchange Rate
# ----------------------------
class ExchangeRate(models.Model):
    rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="نرخ برابری (تومان)")
    is_active = models.BooleanField(default=True, verbose_name="نرخ فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'نرخ ارز'
        verbose_name_plural = 'نرخ‌های ارز'

    def save(self, *args, **kwargs):
        if self.is_active:
            ExchangeRate.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)
        if self.is_active:
            self.update_all_food_prices()

    def update_all_food_prices(self):
        try:
            foods = Food.objects.filter(price__isnull=False)
            updated_count = 0
            for food in foods:
                food.update_usd_price(self.rate)
                food.save(update_fields=['price_usd_cents'])
                updated_count += 1
            return f"تعداد {updated_count} غذا با نرخ {self.rate} به‌روزرسانی شد"
        except Exception as e:
            return f"خطا در به‌روزرسانی قیمت‌ها: {str(e)}"

    def __str__(self):
        return f"1 USD = {self.rate} Toman"


def update_all_food_prices():
    try:
        current_rate = ExchangeRate.objects.filter(is_active=True).first()
        if current_rate:
            return current_rate.update_all_food_prices()
        return "No active exchange rate found"
    except Exception as e:
        return f"Error updating prices: {str(e)}"


def get_current_exchange_rate():
    try:
        current_rate = ExchangeRate.objects.filter(is_active=True).first()
        if current_rate:
            return current_rate.rate
    except:
        pass
    return getattr(settings, 'EXCHANGE_RATE', Decimal('60000.00'))



class MenuView(models.Model):
    """
    مدل برای ثبت بازدید یکتا از منوی هر رستوران
    """
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menu_views',
        verbose_name="رستوران"
    )
    session_key = models.CharField(
        max_length=40,
        db_index=True,
        verbose_name="کلید سشن"
    )
    ip_address = models.GenericIPAddressField(
        verbose_name="آدرس IP",
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        verbose_name="User Agent",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = 'بازدید منو'
        verbose_name_plural = 'بازدیدهای منو'
        unique_together = ['restaurant', 'session_key']
        indexes = [
            models.Index(fields=['restaurant', 'created_at']),
            models.Index(fields=['session_key', 'restaurant']),
            models.Index(fields=['ip_address', 'restaurant']),
        ]

    def __str__(self):
        return f"{self.restaurant.title} - {self.session_key} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @classmethod
    def is_viewed(cls, restaurant, session_key):
        """بررسی می‌کند که آیا این سشن قبلاً از این منو بازدید کرده است"""
        return cls.objects.filter(
            restaurant=restaurant,
            session_key=session_key
        ).exists()

    @classmethod
    def record_view(cls, restaurant, session_key, ip_address=None, user_agent=None):
        """ثبت بازدید جدید اگر قبلاً ثبت نشده باشد"""
        if not cls.is_viewed(restaurant, session_key):
            return cls.objects.create(
                restaurant=restaurant,
                session_key=session_key,
                ip_address=ip_address,
                user_agent=user_agent
            )
        return None

    @classmethod
    def get_views_count(cls, restaurant):
        """تعداد بازدیدهای یکتا برای یک رستوران"""
        return cls.objects.filter(restaurant=restaurant).count()

    @classmethod
    def get_recent_views(cls, restaurant, hours=24):
        """تعداد بازدیدهای اخیر (مثلاً در 24 ساعت گذشته)"""
        from django.utils import timezone
        from datetime import timedelta

        since = timezone.now() - timedelta(hours=hours)
        return cls.objects.filter(
            restaurant=restaurant,
            created_at__gte=since
        ).count()
