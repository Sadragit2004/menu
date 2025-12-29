from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.db.models import Q
from django.views import View
from ...models.menufreemodels.models import Restaurant, MenuCategory, Food, FoodRestaurant, get_current_exchange_rate

# صفحه اصلی منوی دیجیتال
def digital_menu(request, restaurant_slug):
    """صفحه اصلی منوی دیجیتال با پشتیبانی از شخصی‌سازی"""
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug, isActive=True)

    # بررسی انقضای رستوران
    if restaurant.is_expired:
        lang = request.GET.get('lang', 'fa')
        context = {
            'restaurant': restaurant,
            'current_language': lang,
            'lang': lang,
            'expired': True
        }

        if lang == 'en':
            return render(request, 'menu_app/free/restaurant_expired_en.html', context)
        else:
            return render(request, 'menu_app/free/restaurant_expired.html', context)

    lang = request.GET.get('lang', 'fa')

    # دریافت دسته‌بندی‌های فعال
    menu_categories = MenuCategory.objects.filter(
        restaurant=restaurant,
        isActive=True
    ).select_related('category').prefetch_related('foods')

    # دریافت غذاهای فعال رستوران
    foods = Food.objects.filter(
        restaurants=restaurant,
        isActive=True
    ).select_related('menuCategory__category').distinct()

    # دریافت اطلاعات شخصی‌سازی شده غذاها
    customized_foods = FoodRestaurant.objects.filter(
        restaurant=restaurant,
        food__in=foods,
        is_active=True
    ).select_related('food')

    # به هر غذا فیلدهای final_price و final_image رو اضافه کن
    for food in foods:
        # پیدا کردن شخصی‌سازی برای این غذا
        custom_food = None
        for cf in customized_foods:
            if cf.food.id == food.id:
                custom_food = cf
                break

        if custom_food and (custom_food.custom_price or custom_food.custom_image):
            # اگر شخصی‌سازی شده
            food.final_price = custom_food.custom_price if custom_food.custom_price else food.price
            food.final_image = custom_food.custom_image if custom_food.custom_image else food.image
        else:
            # اگر شخصی‌سازی نشده
            food.final_price = food.price
            food.final_image = food.image

    exchange_rate = get_current_exchange_rate()

    context = {
        'restaurant': restaurant,
        'menu_categories': menu_categories,
        'foods': foods,
        'current_language': lang,
        'exchange_rate': exchange_rate,
        'lang': lang,
        'expired': False
    }

    if lang == 'en':
        return render(request, 'menu_app/free/restaurant_en.html', context)
    else:
        return render(request, 'menu_app/free/restaurant.html', context)

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

