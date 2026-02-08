from django.shortcuts import render, get_object_or_404,redirect
from django.core.cache import cache
from django.db import models
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.views import View
import hashlib
import json

# اصلاح import‌ها - بر اساس ساختار پروژه شما
try:
    # اگر models در همان اپ است
    from ...models.menufreemodels.models import Restaurant, MenuCategory, Food, FoodRestaurant, get_current_exchange_rate
except ImportError:
    try:
        # اگر ساختار متفاوت است
        from apps.menu.models.menufreemodels.models import Restaurant, MenuCategory, Food, FoodRestaurant, get_current_exchange_rate
    except ImportError:
        # از relative import استفاده کن
        from ...models.menufreemodels.models import Restaurant, MenuCategory, Food, FoodRestaurant, get_current_exchange_rate


def digital_menu(request, restaurant_slug):
    """بهینه‌ترین نسخه منوی دیجیتال با کش و حداقل query"""

    # 1. ساخت کلید کش یکتا
    lang = request.GET.get('lang', 'fa')
    cache_key = f"digital_menu_{restaurant_slug}_{lang}"

    # 2. تلاش برای دریافت از کش
    cached_response = cache.get(cache_key)
    if cached_response:
        return cached_response

    # 3. دریافت رستوران با یک query
    restaurant = get_object_or_404(
        Restaurant.objects.select_related('owner'),
        slug=restaurant_slug,
        isActive=True
    )

    # 4. بررسی انقضا
    if restaurant.is_expired:
        context = {
            'restaurant': restaurant,
            'current_language': lang,
            'lang': lang,
            'expired': True
        }
        template = 'menu_app/free/restaurant_expired_en.html' if lang == 'en' else 'menu_app/free/restaurant_expired.html'
        response = render(request, template, context)
        cache.set(cache_key, response, 300)  # 5 دقیقه برای صفحات منقضی
        return response

    # 5. فقط دو query اصلی برای همه داده‌ها
    # Query اول: همه دسته‌بندی‌ها
    menu_categories = MenuCategory.objects.filter(
        restaurant=restaurant,
        isActive=True
    ).select_related('category').order_by('displayOrder')

    # Query دوم: همه شخصی‌سازی‌های غذاها
    custom_foods = FoodRestaurant.objects.filter(
        restaurant=restaurant,
        is_active=True
    ).select_related('food').only(
        'food_id', 'custom_price', 'custom_image', 'display_order'
    )

    # 6. ساخت map برای دسترسی سریع
    custom_map = {cf.food_id: cf for cf in custom_foods}

    # 7. دریافت ID دسته‌بندی‌ها
    category_ids = list(menu_categories.values_list('id', flat=True))

    # 8. دریافت غذاهای مرتبط
    if category_ids:
        foods_by_category = Food.objects.filter(
            menuCategory_id__in=category_ids,
            isActive=True,
            restaurants=restaurant
        ).select_related('menuCategory__category')
    else:
        foods_by_category = Food.objects.none()

    # 9. پردازش داده‌ها
    foods_dict = {}
    all_foods_list = []

    for food in foods_by_category:
        cat_id = food.menuCategory_id
        if cat_id not in foods_dict:
            foods_dict[cat_id] = []

        # اعمال شخصی‌سازی‌ها
        cf = custom_map.get(food.id)
        if cf:
            food.final_price = cf.custom_price if cf.custom_price else food.price
            food.final_image = cf.custom_image if cf.custom_image else food.image
            food.is_customized = True
            food.display_order = cf.display_order if cf.display_order else food.displayOrder
        else:
            food.final_price = food.price
            food.final_image = food.image
            food.is_customized = False
            food.display_order = food.displayOrder

        foods_dict[cat_id].append(food)
        all_foods_list.append(food)

    # 10. مرتب‌سازی و ساخت دسته‌بندی نهایی
    processed_categories = []
    for category in menu_categories:
        cat_foods = foods_dict.get(category.id, [])
        # مرتب‌سازی غذاها
        cat_foods.sort(key=lambda x: x.display_order)
        category.foods_list = cat_foods
        processed_categories.append(category)

    # 11. نرخ ارز
    exchange_rate = get_current_exchange_rate()

    # 12. ساخت context
    context = {
        'restaurant': restaurant,
        'menu_categories': processed_categories,
        'foods': all_foods_list,
        'current_language': lang,
        'exchange_rate': exchange_rate,
        'lang': lang,
        'expired': False
    }

    # 13. رندر و ذخیره در کش
    template = 'menu_app/free/restaurant_en.html' if lang == 'en' else 'menu_app/free/restaurant.html'
    response = render(request, template, context)

    # کش کردن
    if restaurant.menu_active:
        cache.set(cache_key, response, 1800)  # 30 دقیقه

    return response



def get_foods_by_category(request, restaurant_slug, category_id):
    """دریافت غذاها بر اساس دسته‌بندی با پشتیبانی از شخصی‌سازی"""
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug, isActive=True)
    lang = request.GET.get('lang', 'fa')

    # دریافت غذاها
    if category_id == 'all':
        foods = Food.objects.filter(restaurants=restaurant, isActive=True)
    else:
        menu_category = get_object_or_404(MenuCategory, id=category_id, restaurant=restaurant, isActive=True)
        foods = Food.objects.filter(menuCategory=menu_category, restaurants=restaurant, isActive=True)

    # دریافت اطلاعات شخصی‌سازی شده
    customized_foods = FoodRestaurant.objects.filter(
        restaurant=restaurant,
        food__in=foods,
        is_active=True
    ).select_related('food')

    foods_data = []
    for food in foods.distinct():
        # پیدا کردن شخصی‌سازی برای این غذا
        custom_food = None
        for cf in customized_foods:
            if cf.food.id == food.id:
                custom_food = cf
                break

        if custom_food and (custom_food.custom_price or custom_food.custom_image):
            # اگر شخصی‌سازی شده
            final_price = custom_food.custom_price if custom_food.custom_price else food.price
            final_image = custom_food.custom_image.url if custom_food.custom_image else (food.image.url if food.image else None)
        else:
            # اگر شخصی‌سازی نشده
            final_price = food.price
            final_image = food.image.url if food.image else None

        # نمایش قیمت
        if lang == 'en':
            price_display = f"{final_price:,.0f} Toman"
        else:
            price_display = f"{final_price:,.0f} تومان"

        foods_data.append({
            'id': food.id,
            'title': food.title_en if lang == 'en' and food.title_en else food.title,
            'description': food.description_en if lang == 'en' and food.description_en else food.description,
            'price': final_price,  # قیمت نهایی
            'price_display': price_display,
            'preparationTime': food.preparationTime,
            'image': final_image,  # تصویر نهایی
            'sound': food.sound.url if food.sound else None,
            'category_id': food.menuCategory.id if food.menuCategory else None,
            'is_customized': custom_food and (custom_food.custom_price or custom_food.custom_image)
        })

    return JsonResponse({'foods': foods_data})

def search_foods(request, restaurant_slug):
    """جستجوی غذاها با پشتیبانی از شخصی‌سازی"""
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug, isActive=True)
    query = request.GET.get('q', '').strip()
    lang = request.GET.get('lang', 'fa')

    base_qs = Food.objects.filter(restaurants=restaurant, isActive=True)

    if query:
        foods = base_qs.filter(
            Q(title__icontains=query) |
            Q(title_en__icontains=query) |
            Q(description__icontains=query) |
            Q(description_en__icontains=query)
        )
    else:
        foods = base_qs

    # دریافت اطلاعات شخصی‌سازی شده
    customized_foods = FoodRestaurant.objects.filter(
        restaurant=restaurant,
        food__in=foods,
        is_active=True
    ).select_related('food')

    foods_data = []
    for food in foods.distinct():
        # پیدا کردن شخصی‌سازی برای این غذا
        custom_food = None
        for cf in customized_foods:
            if cf.food.id == food.id:
                custom_food = cf
                break

        if custom_food and (custom_food.custom_price or custom_food.custom_image):
            # اگر شخصی‌سازی شده
            final_price = custom_food.custom_price if custom_food.custom_price else food.price
            final_image = custom_food.custom_image.url if custom_food.custom_image else (food.image.url if food.image else None)
        else:
            # اگر شخصی‌سازی نشده
            final_price = food.price
            final_image = food.image.url if food.image else None

        # نمایش قیمت
        if lang == 'en':
            price_display = f"{final_price:,.0f} Toman"
        else:
            price_display = f"{final_price:,.0f} تومان"

        foods_data.append({
            'id': food.id,
            'title': food.title_en if lang == 'en' and food.title_en else food.title,
            'description': food.description_en if lang == 'en' and food.description_en else food.description,
            'price': final_price,  # قیمت نهایی
            'price_display': price_display,
            'preparationTime': food.preparationTime,
            'image': final_image,  # تصویر نهایی
            'sound': food.sound.url if food.sound else None,
            'category_id': food.menuCategory.id if food.menuCategory else None,
            'is_customized': custom_food and (custom_food.custom_price or custom_food.custom_image)
        })

    return JsonResponse({'foods': foods_data})

def change_language(request, restaurant_slug):
    """تغییر زبان"""
    lang = request.GET.get('lang', 'fa')
    if lang not in ['fa', 'en']:
        lang = 'fa'

    url = reverse('menu:digital_menu', kwargs={'restaurant_slug': restaurant_slug})
    return redirect(f"{url}?lang={lang}")




# در فایل views.py این ویو را اضافه کنید

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from ...models.menufreemodels.models import Restaurant, MenuView
import json

@method_decorator(csrf_exempt, name='dispatch')
class RecordMenuView(View):
    """
    ویو برای ثبت بازدید یکتا از منوی رستوران
    """
    def post(self, request, restaurant_slug):
        try:
            # پیدا کردن رستوران
            restaurant = Restaurant.objects.get(slug=restaurant_slug, isActive=True)

            # گرفتن session_key از request
            session_key = request.session.session_key
            if not session_key:
                # اگر سشن وجود ندارد، یک سشن جدید ایجاد کن
                request.session.create()
                session_key = request.session.session_key

            # گرفتن اطلاعات درخواست
            ip_address = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', '')

            # ثبت بازدید
            menu_view = MenuView.record_view(
                restaurant=restaurant,
                session_key=session_key,
                ip_address=ip_address,
                user_agent=user_agent
            )

            # گرفتن آمار بازدید
            total_views = MenuView.get_views_count(restaurant)
            daily_views = MenuView.get_recent_views(restaurant, hours=24)

            return JsonResponse({
                'success': True,
                'message': 'بازدید با موفقیت ثبت شد',
                'is_new_view': menu_view is not None,
                'stats': {
                    'total_views': total_views,
                    'daily_views': daily_views
                }
            })

        except Restaurant.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'رستوران پیدا نشد'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در ثبت بازدید: {str(e)}'
            }, status=500)

    def get_client_ip(self, request):
        """دریافت IP واقعی کاربر"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class MenuViewStats(View):
    """
    ویو برای دریافت آمار بازدیدهای یک رستوران
    """
    def get(self, request, restaurant_slug):
        try:
            restaurant = Restaurant.objects.get(slug=restaurant_slug, isActive=True)

            total_views = MenuView.get_views_count(restaurant)
            daily_views = MenuView.get_recent_views(restaurant, hours=24)
            weekly_views = MenuView.get_recent_views(restaurant, hours=168)  # 7 روز

            return JsonResponse({
                'success': True,
                'restaurant': {
                    'title': restaurant.title,
                    'slug': restaurant.slug
                },
                'stats': {
                    'total_views': total_views,
                    'daily_views': daily_views,
                    'weekly_views': weekly_views
                }
            })

        except Restaurant.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'رستوران پیدا نشد'
            }, status=404)

