from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
import json
from apps.menu.models.menufreemodels.models import Restaurant, Category, MenuCategory, Food,FoodRestaurant
from apps.order.models import Ordermenu, MenuImage
from apps.plan.models import PlanOrder
from apps.product.models import ProductOrder
from django.utils import timezone
from django.db.models import Count, Sum
from datetime import datetime, timedelta
try:
    import qrcode
    QRCODE_AVAILABLE = True
    print("✅ qrcode imported successfully")
except ImportError as e:
    print(f"❌ qrcode import failed: {e}")
    QRCODE_AVAILABLE = False
    qrcode = None


import base64
from io import BytesIO
from django.urls import reverse
from django.contrib import messages


# دکوراتور برای بررسی مالکیت رستوران
def restaurant_owner_required(view_func):
    def wrapper(request, slug, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('account:login')

        restaurant = get_object_or_404(Restaurant, slug=slug, isActive=True)

        # بررسی مالکیت
        if restaurant.owner != request.user:
            return HttpResponseForbidden("شما دسترسی به این رستوران را ندارید")

        request.restaurant = restaurant
        return view_func(request, slug, *args, **kwargs)
    return wrapper


@login_required
def panel(request):
    """پنل اصلی - نمایش تمام سفارشات کاربر"""

    # دریافت رستوران‌های کاربر
    user_restaurants = Restaurant.objects.filter(owner=request.user, isActive=True)

    # دریافت تمام سفارشات کاربر از انواع مختلف
    user_orders = Ordermenu.objects.filter(restaurant__owner=request.user).select_related('restaurant').prefetch_related('images')
    plan_orders = PlanOrder.objects.filter(user=request.user,isActive=True).select_related('plan')
    product_orders = ProductOrder.objects.filter(user=request.user).select_related('plan').prefetch_related('items')

    # محاسبه آمار کلی
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # آمار سفارشات منو
    menu_paid_orders = user_orders.filter(status=Ordermenu.STATUS_PAID)
    menu_confirmed_orders = user_orders.filter(status=Ordermenu.STATUS_CONFIRMED)
    menu_delivered_orders = user_orders.filter(status=Ordermenu.STATUS_DELIVERED)
    menu_unpaid_orders = user_orders.filter(status=Ordermenu.STATUS_UNPAID)

    # آمار سفارشات پلن
    plan_paid_orders = plan_orders.filter(isPaid=True)
    plan_unpaid_orders = plan_orders.filter(isPaid=False)

    # آمار سفارشات محصول
    product_paid_orders = product_orders.filter(isPaid=True)
    product_unpaid_orders = product_orders.filter(isPaid=False)

    # آمار کلی سفارشات امروز
    today_menu_orders = user_orders.filter(created_at__date=today).count()
    today_plan_orders = plan_orders.filter(createdAt__date=today).count()
    today_product_orders = product_orders.filter(createdAt__date=today).count()
    today_orders_count = today_menu_orders + today_plan_orders + today_product_orders

    # آمار کلی سفارشات این ماه
    monthly_menu_orders = user_orders.filter(created_at__date__gte=month_start).count()
    monthly_plan_orders = plan_orders.filter(createdAt__date__gte=month_start).count()
    monthly_product_orders = product_orders.filter(createdAt__date__gte=month_start).count()
    monthly_orders_count = monthly_menu_orders + monthly_plan_orders + monthly_product_orders

    # محاسبه درآمد واقعی (فقط سفارشات پرداخت شده)
    today_revenue = (
        sum(order.final_price for order in user_orders.filter(
            created_at__date=today,
            status__in=[Ordermenu.STATUS_PAID, Ordermenu.STATUS_CONFIRMED, Ordermenu.STATUS_DELIVERED]
        )) +
        sum(order.finalPrice for order in plan_orders.filter(
            createdAt__date=today,
            isPaid=True
        )) +
        sum(order.final_price for order in product_orders.filter(
            createdAt__date=today,
            isPaid=True
        ))
    ) // 10  # تبدیل به تومان

    monthly_revenue = (
        sum(order.final_price for order in user_orders.filter(
            created_at__date__gte=month_start,
            status__in=[Ordermenu.STATUS_PAID, Ordermenu.STATUS_CONFIRMED, Ordermenu.STATUS_DELIVERED]
        )) +
        sum(order.finalPrice for order in plan_orders.filter(
            createdAt__date__gte=month_start,
            isPaid=True
        )) +
        sum(order.final_price for order in product_orders.filter(
            createdAt__date__gte=month_start,
            isPaid=True
        ))
    ) // 10  # تبدیل به تومان

    # ترکیب تمام سفارشات برای نمایش
    all_orders = []

    # افزودن سفارشات منو
    for order in user_orders:
        all_orders.append({
            'type': 'menu',
            'object': order,
            'created_at': order.created_at,
            'status': order.status,
            'final_price': order.final_price,
            'is_paid': order.status in [Ordermenu.STATUS_PAID, Ordermenu.STATUS_CONFIRMED, Ordermenu.STATUS_DELIVERED]
        })

    # افزودن سفارشات پلن
    for order in plan_orders:
        all_orders.append({
            'type': 'plan',
            'object': order,
            'created_at': order.createdAt,
            'status': 'paid' if order.isPaid else 'unpaid',
            'final_price': order.finalPrice,
            'is_paid': order.isPaid
        })

    # افزودن سفارشات محصول
    for order in product_orders:
        all_orders.append({
            'type': 'product',
            'object': order,
            'created_at': order.createdAt,
            'status': order.status,
            'final_price': order.final_price,
            'is_paid': order.isPaid
        })

    # مرتب‌سازی بر اساس تاریخ (جدیدترین اول)
    all_orders.sort(key=lambda x: x['created_at'], reverse=True)

    context = {
        'restaurants': user_restaurants,
        'has_restaurant': user_restaurants.exists(),

        # سفارشات ترکیبی
        'all_orders': all_orders,

        # آمار سفارشات منو
        'user_orders': user_orders,
        'paid_orders': menu_paid_orders,
        'confirmed_orders': menu_confirmed_orders,
        'delivered_orders': menu_delivered_orders,
        'unpaid_orders': menu_unpaid_orders,

        # آمار سفارشات پلن
        'plan_orders': plan_orders,
        'plan_paid_orders': plan_paid_orders,
        'plan_unpaid_orders': plan_unpaid_orders,

        # آمار سفارشات محصول
        'product_orders': product_orders,
        'product_paid_orders': product_paid_orders,
        'product_unpaid_orders': product_unpaid_orders,

        # آمار کلی
        'today_orders': today_orders_count,
        'monthly_orders': monthly_orders_count,
        'today_revenue': today_revenue,
        'monthly_revenue': monthly_revenue,
        'purchased_menus': menu_paid_orders.count(),
    }

    return render(request, 'panel_app/free/panel.html', context)

# views.py - بخش order_detail
@login_required
def order_detail(request, order_id, order_type=None):
    """جزئیات سفارش بر اساس نوع"""

    # تشخیص نوع سفارش از URL
    if 'menu' in request.path:
        order_type = 'menu'
    elif 'plan' in request.path:
        order_type = 'plan'
    elif 'product' in request.path:
        order_type = 'product'
    else:
        # اگر از URL قدیمی استفاده شده، فرض می‌کنیم سفارش منو است
        order_type = 'menu'

    try:
        if order_type == 'menu':
            order = get_object_or_404(
                Ordermenu,
                id=order_id,
                restaurant__owner=request.user
            )
            menu_images = order.images.all()
            status_info = order.get_status_info()
            template = 'panel_app/free/order_detail.html'

        elif order_type == 'plan':
            from apps.plan.models import PlanOrder
            order = get_object_or_404(
                PlanOrder,
                id=order_id,
                user=request.user
            )
            menu_images = []
            status_info = {
                'code': 'paid' if order.isPaid else 'unpaid',
                'display': 'پرداخت شده' if order.isPaid else 'پرداخت نشده',
                'is_paid': order.isPaid,
                'is_completed': order.isPaid,
                'is_pending': not order.isPaid,
            }
            template = 'panel_app/free/order_detail.html'

        elif order_type == 'product':
            from apps.product.models import ProductOrder
            order = get_object_or_404(
                ProductOrder,
                id=order_id,
                user=request.user
            )
            menu_images = []
            status_info = {
                'code': order.status,
                'display': dict(ProductOrder.STATUS_CHOICES).get(order.status, order.status),
                'is_paid': order.isPaid,
                'is_completed': order.status == 'paid',
                'is_pending': order.status in ['draft', 'pending'],
            }
            template = 'panel_app/free/order_detail.html'

        else:
            messages.error(request, 'نوع سفارش نامعتبر است')
            return redirect('panel:panel')

        context = {
            'order': order,
            'order_type': order_type,
            'menu_images': menu_images,
            'status_info': status_info,
        }

        return render(request, template, context)

    except Exception as e:
        messages.error(request, f'خطا در دریافت اطلاعات سفارش: {str(e)}')
        return redirect('panel:panel')


@login_required
def update_order_status(request, order_id, order_type):
    """به‌روزرسانی وضعیت سفارش"""
    if request.method == 'POST':
        try:
            if order_type == 'menu':
                order = get_object_or_404(Ordermenu, id=order_id, restaurant__owner=request.user)
                new_status = int(request.POST.get('status'))
                valid_statuses = [status[0] for status in Ordermenu.STATUS_CHOICES]

            elif order_type == 'plan':
                order = get_object_or_404(PlanOrder, id=order_id, user=request.user)
                new_status = request.POST.get('status')
                valid_statuses = ['paid', 'unpaid']

            elif order_type == 'product':
                order = get_object_or_404(ProductOrder, id=order_id, user=request.user)
                new_status = request.POST.get('status')
                valid_statuses = [status[0] for status in ProductOrder.STATUS_CHOICES]

            else:
                return JsonResponse({
                    'success': False,
                    'message': 'نوع سفارش نامعتبر'
                })

            if new_status in valid_statuses:
                if order_type == 'menu':
                    order.status = new_status
                elif order_type == 'plan':
                    order.isPaid = (new_status == 'paid')
                    if order.isPaid and not order.paidAt:
                        order.paidAt = timezone.now()
                elif order_type == 'product':
                    order.status = new_status
                    if new_status == 'paid' and not order.paidAt:
                        order.isPaid = True
                        order.paidAt = timezone.now()

                order.save()

                return JsonResponse({
                    'success': True,
                    'message': 'وضعیت سفارش با موفقیت به‌روزرسانی شد',
                    'new_status': getattr(order, 'get_status_display', lambda: 'پرداخت شده' if getattr(order, 'isPaid', False) else 'پرداخت نشده')()
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'وضعیت نامعتبر'
                })

        except (ValueError, TypeError) as e:
            return JsonResponse({
                'success': False,
                'message': 'خطا در پردازش درخواست'
            })

    return JsonResponse({
        'success': False,
        'message': 'متد نامعتبر'
    })


@login_required
def cancel_order(request, order_id, order_type):
    """لغو سفارش"""
    if request.method == 'POST':
        try:
            if order_type == 'menu':
                order = get_object_or_404(Ordermenu, id=order_id, restaurant__owner=request.user)
                # فقط سفارشات پرداخت نشده قابل لغو هستند
                if order.status != Ordermenu.STATUS_UNPAID:
                    return JsonResponse({
                        'success': False,
                        'message': 'فقط سفارشات پرداخت نشده قابل لغو هستند'
                    })
                order.delete()

            elif order_type == 'plan':
                order = get_object_or_404(PlanOrder, id=order_id, user=request.user)
                # فقط سفارشات پرداخت نشده قابل لغو هستند
                if order.isPaid:
                    return JsonResponse({
                        'success': False,
                        'message': 'سفارشات پرداخت شده قابل لغو نیستند'
                    })
                order.delete()

            elif order_type == 'product':
                order = get_object_or_404(ProductOrder, id=order_id, user=request.user)
                # فقط سفارشات پرداخت نشده قابل لغو هستند
                if order.isPaid:
                    return JsonResponse({
                        'success': False,
                        'message': 'سفارشات پرداخت شده قابل لغو نیستند'
                    })
                order.delete()

            else:
                return JsonResponse({
                    'success': False,
                    'message': 'نوع سفارش نامعتبر'
                })

            return JsonResponse({
                'success': True,
                'message': 'سفارش با موفقیت لغو شد'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در لغو سفارش: {str(e)}'
            })

    return JsonResponse({
        'success': False,
        'message': 'متد نامعتبر'
    })


@login_required
def order_list(request):
    """لیست تمام سفارشات کاربر با فیلتر"""
    status_filter = request.GET.get('status', 'all')
    type_filter = request.GET.get('type', 'all')

    # دریافت تمام سفارشات
    user_orders = Ordermenu.objects.filter(restaurant__owner=request.user)
    plan_orders = PlanOrder.objects.filter(user=request.user)
    product_orders = ProductOrder.objects.filter(user=request.user)

    # فیلتر بر اساس نوع
    if type_filter == 'menu':
        orders_data = user_orders
    elif type_filter == 'plan':
        orders_data = plan_orders
    elif type_filter == 'product':
        orders_data = product_orders
    else:
        # ترکیب تمام سفارشات
        orders_data = list(user_orders) + list(plan_orders) + list(product_orders)

    # فیلتر بر اساس وضعیت
    filtered_orders = []
    for order in orders_data:
        if hasattr(order, 'status'):
            status = order.status
        elif hasattr(order, 'isPaid'):
            status = 'paid' if order.isPaid else 'unpaid'
        else:
            status = 'unknown'

        if (status_filter == 'all' or
            (status_filter == 'unpaid' and status in ['unpaid', 1]) or
            (status_filter == 'paid' and status in ['paid', 2, 3, 4]) or
            (status_filter == 'confirmed' and status == 3) or
            (status_filter == 'delivered' and status == 4)):
            filtered_orders.append(order)

    # مرتب‌سازی
    if type_filter == 'all':
        filtered_orders.sort(key=lambda x: getattr(x, 'created_at', getattr(x, 'createdAt', timezone.now())), reverse=True)
    else:
        if hasattr(filtered_orders, 'order_by'):
            filtered_orders = filtered_orders.order_by('-created_at' if hasattr(filtered_orders.first(), 'created_at') else '-createdAt')

    context = {
        'orders': filtered_orders,
        'current_filter': status_filter,
        'current_type': type_filter,
        'status_choices': Ordermenu.STATUS_CHOICES,
    }

    return render(request, 'panel_app/free/order_list.html', context)


@login_required
def create_restaurant(request):
    """ایجاد رستوران جدید"""
    if request.method == 'POST':
        try:
            data = request.POST
            files = request.FILES

            # بررسی نام انگلیسی تکراری
            english_name = data.get('english_name')
            if Restaurant.objects.filter(english_name=english_name).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'این نام انگلیسی قبلاً انتخاب شده است'
                })

            # ایجاد رستوران جدید
            restaurant = Restaurant(
                owner=request.user,
                title=data.get('title'),
                english_name=english_name,
                description=data.get('description', ''),
                phone=data.get('phone', ''),
                address=data.get('address', ''),
                openingTime=data.get('opening_time'),
                closingTime=data.get('closing_time'),
                minimumOrder=data.get('minimum_order', 0),
                deliveryFee=data.get('delivery_fee', 0),
                taxRate=data.get('tax_rate', 9.0),
                isActive=True
            )

            # ذخیره لوگو
            if 'logo' in files:
                restaurant.logo = files['logo']

            # ذخیره تصویر کاور
            if 'cover_image' in files:
                restaurant.coverImage = files['cover_image']

            restaurant.save()

            return JsonResponse({
                'success': True,
                'message': 'رستوران با موفقیت ایجاد شد',
                'restaurant_slug': restaurant.slug
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در ایجاد رستوران: {str(e)}'
            })

    return render(request, 'panel_app/free/create_restaurant.html')

from django.utils import timezone
from datetime import timedelta

@login_required
@restaurant_owner_required
def restaurant_admin(request, slug):
    """پنل مدیریت منوی رستوران"""
    restaurant = request.restaurant

    if restaurant.is_expired:
        messages.error(request, "❌ دسترسی به پنل مدیریت امکان‌پذیر نیست. رستوران شما منقضی شده است.")
        return redirect('/panel/')

    # دریافت دسته‌بندی‌های رستوران
    menu_categories = MenuCategory.objects.filter(
        restaurant=restaurant
    ).select_related('category').order_by('displayOrder')

    # دریافت همه دسته‌بندی‌های موجود برای افزودن به منو (فقط آنهایی که غذاهای شرکت دارند)
    all_categories = Category.objects.filter(isActive=True).exclude(
        id__in=menu_categories.values_list('category_id', flat=True)
    )

    # غذاهای رستوران (انتخاب شده توسط رستوران)
    selected_company_foods = Food.objects.filter(
        restaurants=restaurant,
        created_by='company'
    ).select_related('menuCategory__category').order_by('displayOrder')

    restaurant_own_foods = Food.objects.filter(
        restaurants=restaurant,
        created_by='restaurant'
    ).select_related('menuCategory__category').order_by('displayOrder')

    # دریافت تمام غذاهای شرکت برای نمایش در تب "همه غذاهای شرکت"
    # فقط غذاهایی که توسط این رستوران انتخاب نشده‌اند
    all_company_foods = Food.objects.filter(
        isActive=True,
        created_by='company'
    ).exclude(
        id__in=selected_company_foods.values_list('id', flat=True)
    ).select_related('menuCategory__category').order_by('displayOrder')

    # محاسبه آمار برای غذاهای شرکت
    foods_with_stats = []
    company_category_ids = set()  # برای ذخیره ID دسته‌بندی‌های شرکت

    # لیست ID غذاهای انتخاب شده توسط رستوران
    selected_food_ids = list(selected_company_foods.values_list('id', flat=True))
    selected_food_ids.extend(list(restaurant_own_foods.values_list('id', flat=True)))

    # غذاهای اصلی شرکت (غیر انتخابی)
    for food in all_company_foods:
        stats = calculate_food_stats(food)
        foods_with_stats.append(create_food_with_stats(food, stats))

        # جمع‌آوری ID دسته‌بندی‌های شرکت
        if food.menuCategory and food.menuCategory.category:
            company_category_ids.add(food.menuCategory.category.id)

    # دریافت دسته‌بندی‌های شرکت (فقط دسته‌بندی‌هایی که غذاهای غیر انتخابی دارند)
    company_categories = Category.objects.filter(
        id__in=company_category_ids,
        isActive=True
    ).order_by('title')

    # ساخت لیست غذاهای نهایی با شخصی‌سازی‌ها
    final_foods = []
    company_foods_for_customization = []  # لیست جدید برای غذاهای شرکت

    # غذاهای شرکت انتخاب شده
    for food in selected_company_foods:
        try:
            custom_food = FoodRestaurant.objects.get(restaurant=restaurant, food=food)
            food_data = {
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
                'custom_food_id': custom_food.id,
                'created_by': food.created_by
            }
            # اضافه کردن به لیست غذاهای شرکت برای شخصی‌سازی
            company_foods_for_customization.append(food_data)
        except FoodRestaurant.DoesNotExist:
            food_data = {
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
                'custom_food_id': None,
                'created_by': food.created_by
            }
            # اضافه کردن به لیست غذاهای شرکت برای شخصی‌سازی
            company_foods_for_customization.append(food_data)
        final_foods.append(food_data)

    # غذاهای خود رستوران
    for food in restaurant_own_foods:
        food_data = {
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
            'custom_food_id': None,
            'created_by': food.created_by
        }
        final_foods.append(food_data)

    # محاسبه اطلاعات انقضا
    expiry_info = {
        'is_expired': restaurant.is_expired,
        'days_until_expiry': restaurant.days_until_expiry,
        'expire_date': restaurant.expireDate,
        'expiry_status': restaurant.expiry_status,
    }

    context = {
        'restaurant': restaurant,
        'menu_categories': menu_categories,
        'all_categories': all_categories,
        'foods_data': final_foods,
        'company_foods_for_customization': company_foods_for_customization,
        'all_foods': foods_with_stats,
        'company_categories': company_categories,
        'selected_food_ids': selected_food_ids,
        'categories': Category.objects.filter(isActive=True),
        'expiry_info': expiry_info,
        'restaurant_own_foods_count': restaurant_own_foods.count(),
        'selected_company_foods_count': selected_company_foods.count(),
    }
    return render(request, 'panel_app/free/restaurant_admin.html', context)


def get_food_details(request, food_id):
    """دریافت اطلاعات یک غذا برای شخصی‌سازی"""
    try:
        food = Food.objects.get(id=food_id, isActive=True)
        restaurant = request.restaurant

        # بررسی اینکه آیا رستوران این غذا را انتخاب کرده است
        if not food.restaurants.filter(id=restaurant.id).exists():
            return JsonResponse({
                'success': False,
                'message': 'این غذا در منوی شما وجود ندارد'
            })

        # دریافت اطلاعات شخصی‌سازی شده
        try:
            custom_food = FoodRestaurant.objects.get(restaurant=restaurant, food=food)
            price = custom_food.final_price
            image_url = custom_food.final_image.url if custom_food.final_image else None
            is_customized = custom_food.has_customizations()
        except FoodRestaurant.DoesNotExist:
            price = food.price
            image_url = food.image.url if food.image else None
            is_customized = False

        return JsonResponse({
            'success': True,
            'food': {
                'id': food.id,
                'title': food.title,
                'title_en': food.title_en,
                'description': food.description,
                'price': price,
                'image_url': image_url,
                'preparationTime': food.preparationTime,
                'menuCategory': food.menuCategory.category.title if food.menuCategory and food.menuCategory.category else 'بدون دسته',
                'created_by': food.created_by,
                'is_customized': is_customized,
                'can_customize': food.created_by == 'company'
            }
        })

    except Food.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'غذا یافت نشد'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در دریافت اطلاعات: {str(e)}'
        })











def calculate_food_stats(food):
    """محاسبه آمار برای یک غذا"""
    # تعداد رستوران‌هایی که این غذا را انتخاب کرده‌اند
    restaurant_count = food.restaurants.count()

    # محاسبه آمار از FoodRestaurant
    custom_foods = FoodRestaurant.objects.filter(food=food)

    if custom_foods.exists():
        # محاسبه قیمت‌های نهایی
        final_prices = [cf.final_price for cf in custom_foods if cf.final_price is not None]

        if final_prices:
            avg_price = sum(final_prices) // len(final_prices)
            min_price = min(final_prices)
            max_price = max(final_prices)
        else:
            avg_price = food.price or 0
            min_price = food.price or 0
            max_price = food.price or 0

        # بررسی شخصی‌سازی
        has_customizations = any(
            cf.custom_price is not None or cf.custom_image for cf in custom_foods
        )
    else:
        avg_price = food.price or 0
        min_price = food.price or 0
        max_price = food.price or 0
        has_customizations = False

    return {
        'restaurant_count': restaurant_count,
        'avg_price': int(avg_price),
        'min_price': int(min_price),
        'max_price': int(max_price),
        'base_price': int(food.price or 0),
        'has_customizations': has_customizations
    }


def create_food_with_stats(food, stats):
    """ایجاد دیکشنری غذا با آمار"""
    return {
        'id': food.id,
        'title': food.title,
        'title_en': food.title_en,
        'description': food.description,
        'description_en': food.description_en,
        'price': food.price or 0,
        'image': food.image,
        'preparationTime': food.preparationTime or 0,
        'isActive': food.isActive,
        'menuCategory': food.menuCategory,
        'slug': food.slug,
        'displayOrder': food.displayOrder or 0,
        'created_by': food.created_by,
        'stats': stats
    }

@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["POST"])
def add_food(request, slug):
    """افزودن غذای جدید - اصلاح شده برای Many-to-Many"""
    restaurant = request.restaurant

    try:
        data = request.POST
        files = request.FILES

        # ایجاد غذای جدید
        food = Food(
            title=data.get('title'),
            description=data.get('description', ''),
            price=data.get('price', 0),
            preparationTime=data.get('preparation_time', 0),
            isActive=data.get('is_active', 'true').lower() == 'true'
        )

        # تنظیم دسته‌بندی منو
        menu_category_id = data.get('menu_category')
        if menu_category_id:
            menu_category = get_object_or_404(MenuCategory, id=menu_category_id, restaurant=restaurant)
            food.menuCategory = menu_category

        # ذخیره تصویر
        if 'image' in files:
            food.image = files['image']

        # ذخیره فایل صوتی
        if 'sound' in files:
            food.sound = files['sound']

        # ابتدا غذا را ذخیره کنید
        food.save()

        # سپس رستوران را به رابطه Many-to-Many اضافه کنید
        food.restaurants.add(restaurant)

        return JsonResponse({
            'success': True,
            'message': 'غذا با موفقیت اضافه شد',
            'food_id': food.id
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در افزودن غذا: {str(e)}'
        })

@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["POST"])
def update_food(request, slug, food_id):
    """ویرایش غذا - اصلاح شده برای Many-to-Many"""
    restaurant = request.restaurant
    food = get_object_or_404(Food, id=food_id, restaurants=restaurant)

    try:
        data = request.POST
        files = request.FILES

        # به‌روزرسانی فیلدها
        food.title = data.get('title', food.title)
        food.description = data.get('description', food.description)
        food.price = data.get('price', food.price)
        food.preparationTime = data.get('preparation_time', food.preparationTime)
        food.isActive = data.get('is_active', 'true').lower() == 'true'

        # به‌روزرسانی دسته‌بندی منو
        menu_category_id = data.get('menu_category')
        if menu_category_id:
            menu_category = get_object_or_404(MenuCategory, id=menu_category_id, restaurant=restaurant)
            food.menuCategory = menu_category
        else:
            food.menuCategory = None

        # به‌روزرسانی تصویر
        if 'image' in files:
            food.image = files['image']

        # به‌روزرسانی فایل صوتی
        if 'sound' in files:
            food.sound = files['sound']

        food.save()

        return JsonResponse({
            'success': True,
            'message': 'غذا با موفقیت ویرایش شد'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در ویرایش غذا: {str(e)}'
        })

@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_food(request, slug, food_id):
    """حذف غذا - اصلاح شده برای Many-to-Many"""
    restaurant = request.restaurant
    food = get_object_or_404(Food, id=food_id, restaurants=restaurant)

    try:
        # حذف رابطه با رستوران (نه خود غذا)
        food.restaurants.remove(restaurant)

        # اگر غذا دیگر به هیچ رستورانی مرتبط نیست، آن را حذف کن
        if not food.restaurants.exists():
            food.delete()

        return JsonResponse({
            'success': True,
            'message': 'غذا با موفقیت از رستوران حذف شد'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در حذف غذا: {str(e)}'
        })

@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["POST"])
def toggle_food_status(request, slug, food_id):
    """تغییر وضعیت فعال/غیرفعال غذا"""
    restaurant = request.restaurant
    food = get_object_or_404(Food, id=food_id, restaurants=restaurant)

    try:
        food.isActive = not food.isActive
        food.save()

        status = "فعال" if food.isActive else "غیرفعال"
        return JsonResponse({
            'success': True,
            'message': f'وضعیت غذا به {status} تغییر کرد',
            'is_active': food.isActive
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در تغییر وضعیت: {str(e)}'
        })

@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["POST"])
def add_menu_category(request, slug):
    """افزودن دسته‌بندی جدید به منوی رستوران"""
    restaurant = request.restaurant

    try:
        data = request.POST
        files = request.FILES

        category_id = data.get('category_id')
        if not category_id:
            return JsonResponse({
                'success': False,
                'message': 'لطفاً یک دسته‌بندی انتخاب کنید'
            })

        # بررسی وجود دسته‌بندی
        category = get_object_or_404(Category, id=category_id, isActive=True)

        # بررسی تکراری نبودن
        if MenuCategory.objects.filter(restaurant=restaurant, category=category).exists():
            return JsonResponse({
                'success': False,
                'message': 'این دسته‌بندی قبلاً به منو اضافه شده است'
            })

        # ایجاد دسته‌بندی منو
        menu_category = MenuCategory(
            restaurant=restaurant,
            category=category,
            isActive=data.get('is_active', 'true').lower() == 'true'
        )

        # ذخیره تصویر سفارشی
        if 'custom_image' in files:
            menu_category.customImage = files['custom_image']

        menu_category.save()

        return JsonResponse({
            'success': True,
            'message': 'دسته‌بندی با موفقیت به منو اضافه شد',
            'menu_category_id': menu_category.id,
            'category_title': category.title,
            'category_id': category.id
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در افزودن دسته‌بندی: {str(e)}'
        })

@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["POST"])
def toggle_menu_category_status(request, slug, menu_category_id):
    """تغییر وضعیت فعال/غیرفعال دسته‌بندی"""
    restaurant = request.restaurant
    menu_category = get_object_or_404(MenuCategory, id=menu_category_id, restaurant=restaurant)

    try:
        menu_category.isActive = not menu_category.isActive
        menu_category.save()

        status = "فعال" if menu_category.isActive else "غیرفعال"
        return JsonResponse({
            'success': True,
            'message': f'وضعیت دسته‌بندی به {status} تغییر کرد',
            'is_active': menu_category.isActive
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در تغییر وضعیت: {str(e)}'
        })

@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_menu_category(request, slug, menu_category_id):
    """حذف دسته‌بندی از منو"""
    restaurant = request.restaurant
    menu_category = get_object_or_404(MenuCategory, id=menu_category_id, restaurant=restaurant)

    try:
        # بررسی آیا غذاهایی در این دسته‌بندی وجود دارند
        if menu_category.foods.exists():
            return JsonResponse({
                'success': False,
                'message': 'امکان حذف دسته‌بندی وجود ندارد. ابتدا غذاهای این دسته‌بندی را حذف یا انتقال دهید.'
            })

        menu_category.delete()

        return JsonResponse({
            'success': True,
            'message': 'دسته‌بندی با موفقیت از منو حذف شد'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در حذف دسته‌بندی: {str(e)}'
        })


@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["POST"])
def update_restaurant_settings(request, slug):
    """به‌روزرسانی تنظیمات رستوران"""
    restaurant = request.restaurant

    try:
        data = request.POST
        files = request.FILES

        # بررسی نام انگلیسی تکراری
        english_name = data.get('english_name')
        if english_name and english_name != restaurant.english_name:
            if Restaurant.objects.filter(english_name=english_name).exclude(id=restaurant.id).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'این نام انگلیسی قبلاً انتخاب شده است'
                })

        # به‌روزرسانی فیلدها
        restaurant.title = data.get('title', restaurant.title)
        restaurant.english_name = english_name or restaurant.english_name
        restaurant.description = data.get('description', restaurant.description)
        restaurant.phone = data.get('phone', restaurant.phone)
        restaurant.address = data.get('address', restaurant.address)
        restaurant.openingTime = data.get('opening_time', restaurant.openingTime)
        restaurant.closingTime = data.get('closing_time', restaurant.closingTime)
        restaurant.minimumOrder = data.get('minimum_order', restaurant.minimumOrder)
        restaurant.deliveryFee = data.get('delivery_fee', restaurant.deliveryFee)
        restaurant.taxRate = data.get('tax_rate', restaurant.taxRate)

        # به‌روزرسانی لوگو
        if 'logo' in files:
            restaurant.logo = files['logo']

        # به‌روزرسانی تصویر کاور
        if 'cover_image' in files:
            restaurant.coverImage = files['cover_image']

        restaurant.save()

        return JsonResponse({
            'success': True,
            'message': 'تنظیمات رستوران با موفقیت به‌روزرسانی شد'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در به‌روزرسانی تنظیمات: {str(e)}'
        })


@login_required
@restaurant_owner_required
def get_foods_by_category(request, slug, category_id=None):
    """دریافت غذاها بر اساس دسته‌بندی"""
    restaurant = request.restaurant

    foods = Food.objects.filter(restaurants=restaurant)

    if category_id and category_id != 'all':
        foods = foods.filter(menuCategory__category__id=category_id)

    foods_data = []
    for food in foods:
        foods_data.append({
            'id': food.id,
            'title': food.title,
            'description': food.description,
            'price': food.price,
            'preparation_time': food.preparationTime,
            'image_url': food.image.url if food.image else '',
            'category_name': food.menuCategory.category.title if food.menuCategory and food.menuCategory.category else 'بدون دسته',
            'category_id': food.menuCategory.category.id if food.menuCategory and food.menuCategory.category else None,
            'is_active': food.isActive
        })

    return JsonResponse({
        'success': True,
        'foods': foods_data
    })

@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["POST"])
def update_food_order(request, slug):
    """به‌روزرسانی ترتیب نمایش غذاها"""
    restaurant = request.restaurant

    try:
        data = json.loads(request.body)
        order_data = data.get('order', [])

        for item in order_data:
            food = get_object_or_404(Food, id=item['id'], restaurants=restaurant)
            food.displayOrder = item['order']
            food.save()

        return JsonResponse({
            'success': True,
            'message': 'ترتیب نمایش با موفقیت به‌روزرسانی شد'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در به‌روزرسانی ترتیب: {str(e)}'
        })

# Context Processor
def restaurant_context(request):
    """Context processor برای دسترسی به رستوران‌های کاربر در همه تمپلیت‌ها"""
    context = {}

    if request.user.is_authenticated:
        user_restaurants = Restaurant.objects.filter(owner=request.user, isActive=True)
        context['user_restaurants'] = user_restaurants

        current_restaurant_slug = request.session.get('current_restaurant_slug')
        if current_restaurant_slug:
            try:
                current_restaurant = Restaurant.objects.get(
                    slug=current_restaurant_slug,
                    owner=request.user,
                    isActive=True
                )
                context['current_restaurant'] = current_restaurant
                context['current_restaurant_slug'] = current_restaurant_slug
            except Restaurant.DoesNotExist:
                if 'current_restaurant_slug' in request.session:
                    del request.session['current_restaurant_slug']

    return context

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def create_restaurant_modal(request):
    """مدیریت افتتاح رستوران از طریق مودال"""
    try:
        # تشخیص نوع داده دریافتی
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                files = None
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'message': 'داده‌های JSON نامعتبر است'
                })
        else:
            data = request.POST
            files = request.FILES

        step = data.get('step')
        menu_creation_type = data.get('menu_creation_type')

        print(f"Step: {step}, Menu Creation Type: {menu_creation_type}")

        if step == 3:  # ساخت رستوران توسط خود کاربر
            # دریافت داده‌ها
            name = data.get('name', '').strip()
            family = data.get('family', '').strip()
            restaurant_name = data.get('restaurant_name', '').strip()
            english_name = data.get('english_name', '').strip().lower()
            is_seo_enabled = data.get('is_seo_enabled', False)
            expire_days = data.get('expire_days', 29)

            # اعتبارسنجی داده‌ها
            if not name or not family or not restaurant_name or not english_name:
                return JsonResponse({
                    'success': False,
                    'message': 'لطفاً تمام فیلدهای ضروری را پر کنید'
                })

            # بررسی نام انگلیسی تکراری
            if Restaurant.objects.filter(english_name=english_name).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'این نام انگلیسی قبلاً انتخاب شده است'
                })

            # محاسبه تاریخ انقضا
            from datetime import timedelta
            from django.utils import timezone

            expire_date = timezone.now() + timedelta(days=int(expire_days))

            # ایجاد رستوران
            restaurant = Restaurant(
                owner=request.user,
                title=restaurant_name,
                english_name=english_name,
                isActive=True,
                isSeo=is_seo_enabled,
                expireDate=expire_date
            )
            restaurant.save()

            # به‌روزرسانی اطلاعات کاربر
            request.user.name = name
            request.user.family = family
            request.user.save()

            return JsonResponse({
                'success': True,
                'message': f'رستوران با موفقیت ایجاد شد و برای {expire_days} روز فعال است',
                'redirect_url': f'/panel/{restaurant.slug}/admin/'
            })

        elif step == 'create_with_company':
            # دریافت مستقیم داده‌ها از درخواست
            name = data.get('name', '').strip()
            family = data.get('family', '').strip()
            restaurant_name = data.get('restaurant_name', '').strip()
            english_name = data.get('english_name', '').strip().lower()
            is_seo_enabled_str = data.get('is_seo_enabled', '0')
            is_seo_enabled = is_seo_enabled_str == '1'

            print(f"Data received - Name: {name}, Family: {family}, Restaurant: {restaurant_name}, English: {english_name}, SEO: {is_seo_enabled}")

            # اعتبارسنجی داده‌ها
            if not name or not family or not restaurant_name or not english_name:
                missing_fields = []
                if not name: missing_fields.append('نام')
                if not family: missing_fields.append('نام خانوادگی')
                if not restaurant_name: missing_fields.append('نام رستوران')
                if not english_name: missing_fields.append('نام انگلیسی')

                return JsonResponse({
                    'success': False,
                    'message': f'لطفاً فیلدهای زیر را پر کنید: {", ".join(missing_fields)}'
                })

            # بررسی نام انگلیسی تکراری
            if Restaurant.objects.filter(english_name=english_name).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'این نام انگلیسی قبلاً انتخاب شده است'
                })

            if menu_creation_type == 'company_save_only':
                # ذخیره در session
                request.session['pending_restaurant'] = {
                    'name': name,
                    'family': family,
                    'restaurant_name': restaurant_name,
                    'english_name': english_name,
                    'is_seo_enabled': is_seo_enabled,
                    'menu_images_count': 0
                }

                # ذخیره اطلاعات عکس‌ها
                menu_images = files.getlist('menu_images') if files else []
                saved_images_count = 0
                image_info_list = []

                for image in menu_images:
                    if saved_images_count < 10:
                        image_info_list.append({
                            'name': image.name,
                            'size': image.size,
                            'type': image.content_type
                        })
                        saved_images_count += 1

                request.session['pending_restaurant']['menu_images_info'] = image_info_list
                request.session['pending_restaurant']['menu_images_count'] = saved_images_count
                request.session.modified = True

                # به‌روزرسانی اطلاعات کاربر
                request.user.name = name
                request.user.family = family
                request.user.save()

                return JsonResponse({
                    'success': True,
                    'message': f'عکس‌ها با موفقیت ذخیره شد ({saved_images_count} عکس)',
                    'saved_images': saved_images_count
                })

            else:
                # ایجاد رستوران (غیرفعال تا پرداخت انجام شود)
                restaurant = Restaurant(
                    owner=request.user,
                    title=restaurant_name,
                    english_name=english_name,
                    isActive=False,  # غیرفعال تا پرداخت انجام شود
                    isSeo=is_seo_enabled
                )
                restaurant.save()

                # ایجاد سفارش
                order = Ordermenu.objects.create(
                    restaurant=restaurant,
                    isfinaly=False,
                    isActive=False,
                    status=Ordermenu.STATUS_UNPAID,
                    is_seo_enabled=is_seo_enabled
                )

                # آپلود عکس‌ها
                menu_images = files.getlist('menu_images') if files else []
                saved_images_count = 0

                for image in menu_images:
                    if saved_images_count < 10:
                        MenuImage.objects.create(
                            order=order,
                            image=image
                        )
                        saved_images_count += 1

                # پاک کردن session
                if 'pending_restaurant' in request.session:
                    del request.session['pending_restaurant']

                # استفاده از سیستم پرداخت یکپارچه
                return JsonResponse({
                    'success': True,
                    'message': f'رستوران ایجاد شد و {saved_images_count} عکس آپلود شد',
                    'order_id': order.id,
                    'redirect_url': f'/peyment/request/menu/{order.id}/'
                })




    except Exception as e:
        print(f"Error in create_restaurant_modal: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': f'خطا در پردازش: {str(e)}'
        })

@login_required
def check_english_name(request):
    """بررسی تکراری نبودن نام انگلیسی"""
    english_name = request.GET.get('english_name', '').strip().lower()

    if not english_name:
        return JsonResponse({'available': False, 'message': 'نام انگلیسی نمی‌تواند خالی باشد'})

    exists = Restaurant.objects.filter(english_name=english_name).exists()

    if exists:
        return JsonResponse({
            'available': False,
            'message': 'این نام انگلیسی قبلاً انتخاب شده است'
        })
    else:
        return JsonResponse({
            'available': True,
            'message': 'نام انگلیسی قابل استفاده است',
            'menu_url': f'/menu/{english_name}'
        })

@login_required
@restaurant_owner_required
def get_category_tree(request, slug):
    """دریافت درخت دسته‌بندی‌ها به صورت سلسله‌مراتبی"""
    try:
        parent_categories = Category.objects.filter(
            parent=None,
            isActive=True
        ).prefetch_related('children').order_by('displayOrder')

        categories_data = []
        for parent in parent_categories:
            parent_data = {
                'id': parent.id,
                'title': parent.title,
                'image_url': parent.image.url if parent.image else '',
                'has_children': parent.is_parent,
                'subcategories': []
            }

            for child in parent.active_subcategories:
                child_data = {
                    'id': child.id,
                    'title': child.title,
                    'image_url': child.image.url if child.image else '',
                    'parent_title': parent.title
                }
                parent_data['subcategories'].append(child_data)

            categories_data.append(parent_data)

        return JsonResponse({
            'success': True,
            'categories': categories_data
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در دریافت دسته‌بندی‌ها: {str(e)}'
        })

@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["POST"])
def quick_add_menu_category(request, slug):
    """افزودن سریع چندین دسته‌بندی به منوی رستوران"""
    restaurant = request.restaurant

    try:
        data = json.loads(request.body)
        category_ids = data.get('category_ids', [])

        if not category_ids:
            return JsonResponse({
                'success': False,
                'message': 'لطفاً حداقل یک دسته‌بندی انتخاب کنید'
            })

        categories = Category.objects.filter(id__in=category_ids, isActive=True)
        if len(categories) != len(category_ids):
            return JsonResponse({
                'success': False,
                'message': 'برخی از دسته‌بندی‌ها یافت نشدند'
            })

        added_categories = []
        skipped_categories = []

        for category in categories:
            if MenuCategory.objects.filter(restaurant=restaurant, category=category).exists():
                skipped_categories.append(category.title)
                continue

            menu_category = MenuCategory(
                restaurant=restaurant,
                category=category,
                isActive=True
            )
            menu_category.save()
            added_categories.append({
                'id': menu_category.id,
                'title': category.title,
                'image_url': menu_category.displayImage.url if menu_category.displayImage else '',
                'has_custom_image': bool(menu_category.customImage)
            })

        message = ""
        if added_categories:
            message += f"{len(added_categories)} دسته‌بندی با موفقیت به منو اضافه شد"
        if skipped_categories:
            message += f" - {len(skipped_categories)} دسته‌بندی قبلاً اضافه شده بودند"

        return JsonResponse({
            'success': True,
            'message': message,
            'added_categories': added_categories,
            'skipped_categories': skipped_categories
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در افزودن دسته‌بندی‌ها: {str(e)}'
        })

@login_required
def user_menus_view(request):
    user_restaurants = request.user.restaurants.all()
    menu_categories = MenuCategory.objects.filter(
        restaurant__in=user_restaurants
    ).select_related('restaurant', 'category')

    return render(request, 'panel_app/free/myMenu.html', {
        'menu_categories': menu_categories,
    })

@login_required
def generate_qr_code(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug, owner=request.user)
    menu_url = request.build_absolute_uri(f'/menu/{restaurant.slug}/')

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(menu_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    img_str = base64.b64encode(buffer.getvalue()).decode()

    return JsonResponse({
        'success': True,
        'qr_code': f'data:image/png;base64,{img_str}',
        'menu_url': menu_url
    })

@login_required
def check_pending_restaurant(request):
    """بررسی وجود رستوران در حال انتظار"""
    pending_restaurant = request.session.get('pending_restaurant')

    if pending_restaurant:
        return JsonResponse({
            'has_pending': True,
            'data': pending_restaurant
        })
    else:
        return JsonResponse({
            'has_pending': False
        })

@login_required
def clear_pending_restaurant(request):
    """پاک کردن رستوران در حال انتظار"""
    if 'pending_restaurant' in request.session:
        del request.session['pending_restaurant']

    return JsonResponse({'success': True})





# views.py
@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["POST"])
def toggle_food_selection(request, slug, food_id):
    """تغییر وضعیت انتخاب غذا برای رستوران"""
    restaurant = request.restaurant

    try:
        food = get_object_or_404(Food, id=food_id, isActive=True)

        # تغییر وضعیت انتخاب
        if food.restaurants.filter(id=restaurant.id).exists():
            food.restaurants.remove(restaurant)
            selected = False
            message = "غذا از منو حذف شد"
        else:
            food.restaurants.add(restaurant)
            selected = True
            message = "غذا به منو اضافه شد"

        return JsonResponse({
            'success': True,
            'message': message,
            'selected': selected,
            'food_id': food_id
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در تغییر وضعیت: {str(e)}'
        })

@login_required
@restaurant_owner_required
@csrf_exempt
@require_http_methods(["POST"])
def assign_food_to_category(request, slug, food_id):
    """انتساب غذا به دسته‌بندی منوی رستوران"""
    restaurant = request.restaurant

    try:
        data = json.loads(request.body)
        category_id = data.get('category_id')

        food = get_object_or_404(Food, id=food_id, restaurants=restaurant)

        if category_id:
            menu_category = get_object_or_404(MenuCategory, id=category_id, restaurant=restaurant)
            food.menuCategory = menu_category
        else:
            food.menuCategory = None

        food.save()

        return JsonResponse({
            'success': True,
            'message': 'دسته‌بندی غذا به‌روزرسانی شد'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در انتساب دسته‌بندی: {str(e)}'
        })




# در فایل viewsfree.py - اضافه کردن ویوهای شخصی‌سازی

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json

@require_http_methods(["GET"])
def get_customized_foods(request, restaurant_slug):
    """دریافت لیست غذاهای شخصی‌سازی شده رستوران"""
    try:
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)

        # استفاده از related_name درست از مدل FoodRestaurant
        customized_foods = FoodRestaurant.objects.filter(
            restaurant=restaurant
        ).select_related('food')

        foods_data = []
        for custom_food in customized_foods:
            food = custom_food.food

            food_data = {
                'id': custom_food.id,
                'food_id': food.id,
                'title': food.title,
                'description': food.description,
                'original_price': food.price,
                'custom_price': custom_food.custom_price,
                'final_price': custom_food.final_price,
                'original_image': food.image.url if food.image else None,
                'custom_image': custom_food.custom_image.url if custom_food.custom_image else None,
                'final_image': custom_food.final_image.url if custom_food.final_image else None,
                'preparation_time': food.preparationTime,
                'category_name': food.menuCategory.category.title if food.menuCategory and food.menuCategory.category else None,
                'has_customizations': custom_food.has_customizations(),
                'is_active': custom_food.is_active,
                'created_at': custom_food.created_at.isoformat(),
                'updated_at': custom_food.updated_at.isoformat()
            }
            foods_data.append(food_data)

        return JsonResponse({
            'success': True,
            'customized_foods': foods_data,
            'total_count': len(foods_data)
        })

    except Exception as e:
        import traceback
        print("Error in get_customized_foods:", str(e))
        print(traceback.format_exc())

        return JsonResponse({
            'success': False,
            'message': f'خطا در دریافت لیست غذاهای شخصی‌سازی شده: {str(e)}'
        }, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def reset_food_customization(request, restaurant_slug, food_id):
    """بازنشانی شخصی‌سازی یک غذا"""
    try:
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
        food = get_object_or_404(Food, id=food_id)

        custom_food = get_object_or_404(
            FoodRestaurant,
            restaurant=restaurant,
            food=food
        )

        custom_food.reset_customizations()
        custom_food.save()

        return JsonResponse({
            'success': True,
            'message': 'شخصی‌سازی غذا با موفقیت بازنشانی شد'
        })

    except Exception as e:
        import traceback
        print("Error in reset_food_customization:", str(e))
        print(traceback.format_exc())

        return JsonResponse({
            'success': False,
            'message': f'خطا در بازنشانی شخصی‌سازی: {str(e)}'
        }, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def toggle_custom_food_status(request, restaurant_slug, food_id):
    """تغییر وضعیت فعال/غیرفعال بودن غذای شخصی‌سازی شده"""
    try:
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)
        food = get_object_or_404(Food, id=food_id)

        custom_food = get_object_or_404(
            FoodRestaurant,
            restaurant=restaurant,
            food=food
        )

        custom_food.is_active = not custom_food.is_active
        custom_food.save()

        return JsonResponse({
            'success': True,
            'message': f'وضعیت غذا با موفقیت {"فعال" if custom_food.is_active else "غیرفعال"} شد'
        })

    except Exception as e:
        import traceback
        print("Error in toggle_custom_food_status:", str(e))
        print(traceback.format_exc())

        return JsonResponse({
            'success': False,
            'message': f'خطا در تغییر وضعیت: {str(e)}'
        }, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def bulk_customize_foods(request, restaurant_slug):
    """ذخیره گروهی شخصی‌سازی غذاها"""
    try:
        print(f"=== شروع bulk_customize_foods برای رستوران: {restaurant_slug} ===")
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug)

        # لاگ هدرها و محتوای درخواست
        print(f"Content-Type: {request.content_type}")
        print(f"Method: {request.method}")
        print(f"POST data: {dict(request.POST)}")
        print(f"FILES: {list(request.FILES.keys())}")

        # دریافت داده‌ها
        if request.content_type.startswith("application/json"):
            try:
                raw_body = request.body
                body_str = raw_body.decode('utf-8')
                data = json.loads(body_str)
                print(f"JSON data received: {data}")
            except Exception as e:
                print(f"Error decoding JSON: {e}")
                return JsonResponse({
                    'success': False,
                    'message': f'خطا در پردازش داده‌های JSON: {str(e)}'
                }, status=400)
        else:
            # دریافت از FormData
            data = request.POST.dict()
            print(f"FormData received: {data}")

            # پردازش customizations
            if "customizations" in data:
                try:
                    customizations_str = data["customizations"]
                    print(f"Customizations string: {customizations_str}")
                    data["customizations"] = json.loads(customizations_str)
                    print(f"Parsed customizations: {data['customizations']}")
                except Exception as e:
                    print(f"Error parsing customizations: {e}")
                    data["customizations"] = []

        customizations = data.get('customizations', [])
        print(f"Final customizations: {customizations}")
        print(f"Number of customizations: {len(customizations)}")

        results = []
        errors = []

        with transaction.atomic():
            for i, customization in enumerate(customizations):
                try:
                    print(f"Processing customization {i+1}: {customization}")

                    food_id = customization.get('food_id')
                    custom_price = customization.get('custom_price')

                    print(f"Food ID: {food_id}, Custom Price: {custom_price}")

                    if not food_id:
                        errors.append('شناسه غذا الزامی است')
                        continue

                    # پیدا کردن غذا
                    food = Food.objects.get(id=food_id)
                    print(f"Found food: {food.title} (ID: {food.id})")

                    # بررسی قابل شخصی‌سازی بودن
                    if food.created_by != 'company':
                        error_msg = f'غذای {food.title} قابل شخصی‌سازی نیست (created_by: {food.created_by})'
                        errors.append(error_msg)
                        print(error_msg)
                        continue

                    # ایجاد یا به‌روزرسانی FoodRestaurant
                    custom_food, created = FoodRestaurant.objects.get_or_create(
                        restaurant=restaurant,
                        food=food
                    )

                    print(f"FoodRestaurant {'created' if created else 'updated'}: {custom_food.id}")

                    # به‌روزرسانی قیمت
                    old_price = custom_food.custom_price
                    if custom_price is not None:
                        custom_food.custom_price = custom_price

                    # پردازش تصویر
                    image_key = f'image_{food_id}'
                    if image_key in request.FILES:
                        custom_food.custom_image = request.FILES[image_key]
                        print(f"Image updated for food {food_id}")

                    custom_food.save()

                    print(f"Custom food saved - ID: {custom_food.id}, Custom Price: {custom_food.custom_price}, Final Price: {custom_food.final_price}")

                    results.append({
                        'food_id': food.id,
                        'food_title': food.title,
                        'custom_price': custom_food.custom_price,
                        'final_price': custom_food.final_price,
                        'success': True
                    })

                except Food.DoesNotExist:
                    error_msg = f'غذا با شناسه {food_id} یافت نشد'
                    errors.append(error_msg)
                    print(error_msg)
                except Exception as e:
                    error_msg = f'خطا در شخصی‌سازی غذا {food_id}: {str(e)}'
                    errors.append(error_msg)
                    print(error_msg)
                    import traceback
                    print(traceback.format_exc())

        print(f"Processing completed. Results: {len(results)}, Errors: {len(errors)}")
        print(f"Results: {results}")
        print(f"Errors: {errors}")

        response_data = {
            'success': len(errors) == 0,
            'message': f'{len(results)} غذا با موفقیت شخصی‌سازی شدند',
            'results': results,
            'errors': errors
        }

        print(f"Final response: {response_data}")
        return JsonResponse(response_data)

    except Exception as e:
        import traceback
        print("Error in bulk_customize_foods:", str(e))
        print(traceback.format_exc())

        return JsonResponse({
            'success': False,
            'message': f'خطا در ذخیره گروهی: {str(e)}'
        }, status=500)




@login_required
def restaurant_settings(request, restaurant_slug):
    restaurant = get_object_or_404(Restaurant, slug=restaurant_slug, owner=request.user)

    if request.method == 'POST':
        try:
            # Update color palette
            restaurant.primary_color = request.POST.get('primary_color', '#3B82F6')
            restaurant.secondary_color = request.POST.get('secondary_color', '#10B981')
            restaurant.background_color = request.POST.get('background_color', '#F9FAFB')
            restaurant.text_color = request.POST.get('text_color', '#1F2937')

            # Update theme settings
            restaurant.theme = request.POST.get('theme', 'auto')
            restaurant.menu_style = request.POST.get('menu_style', 'grid')

            # Update toggle settings
            restaurant.show_usd_price = request.POST.get('show_usd_price') == 'on'
            restaurant.show_preparation_time = request.POST.get('show_preparation_time') == 'on'
            restaurant.menu_active = request.POST.get('menu_active') == 'on'

            # Update logo and cover
            if 'logo' in request.FILES:
                restaurant.logo = request.FILES['logo']
            if 'cover_image' in request.FILES:
                restaurant.coverImage = request.FILES['cover_image']

            restaurant.save()

            return JsonResponse({
                'success': True,
                'message': 'تنظیمات با موفقیت ذخیره شد'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'خطا در ذخیره تنظیمات: {str(e)}'
            })
