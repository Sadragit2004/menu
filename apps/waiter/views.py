from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
from django.db.models import Count, Q, Sum
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
import json
import csv

from .models import Waiter, Order
from apps.menu.models.menufreemodels.models import Restaurant
from .forms import WaiterForm, WaiterEditForm

# ----------------------------
# Waiter Dashboard Views
# ----------------------------

@login_required
def waiter_dashboard(request):
    """
    داشبورد اصلی مدیریت گارسون‌ها
    """
    # دریافت رستوران‌های متعلق به کاربر
    user_restaurants = Restaurant.objects.filter(owner=request.user)

    if not user_restaurants.exists():
        messages.warning(request, "شما هیچ رستورانی ندارید.")
        return render(request, 'waiter_app/dashboard.html', {
            'restaurants': [],
            'total_waiters': 0,
            'active_waiters': 0,
            'today_orders': 0
        })

    # آمار کلی
    total_waiters = Waiter.objects.filter(restaurant__in=user_restaurants).count()
    active_waiters = Waiter.objects.filter(
        restaurant__in=user_restaurants,
        isActive=True
    ).count()

    # سفارش‌های امروز
    today_orders = Order.objects.filter(
        restaurant__in=user_restaurants,
        createdAt__date=timezone.now().date()
    ).count()

    # رستوران انتخابی
    selected_restaurant_id = request.GET.get('restaurant')
    if selected_restaurant_id:
        selected_restaurant = get_object_or_404(
            Restaurant,
            id=selected_restaurant_id,
            owner=request.user
        )
    else:
        selected_restaurant = user_restaurants.first()

    # گارسون‌های رستوران انتخابی
    waiters = Waiter.objects.filter(restaurant=selected_restaurant).order_by('-isActive', '-createdAt')

    # آمار گارسون‌ها
    waiter_stats = []
    for waiter in waiters:
        stats = {
            'waiter': waiter,
            'active_orders': waiter.active_orders_count,
            'today_orders': waiter.today_orders_count,
            'total_orders': waiter.orders.count(),
        }
        waiter_stats.append(stats)

    context = {
        'restaurants': user_restaurants,
        'selected_restaurant': selected_restaurant,
        'waiters_stats': waiter_stats,
        'total_waiters': total_waiters,
        'active_waiters': active_waiters,
        'today_orders': today_orders,
        'current_tab': 'dashboard'
    }

    return render(request, 'waiter_app/dashboard.html', context)

@login_required
def waiter_list(request):
    """
    لیست کامل گارسون‌ها با قابلیت فیلتر و جستجو
    """
    user_restaurants = Restaurant.objects.filter(owner=request.user)

    # فیلتر رستوران
    restaurant_id = request.GET.get('restaurant')
    if restaurant_id:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=request.user)
        waiters = Waiter.objects.filter(restaurant=restaurant)
    else:
        waiters = Waiter.objects.filter(restaurant__in=user_restaurants)

    # فیلتر وضعیت
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        waiters = waiters.filter(isActive=True)
    elif status_filter == 'inactive':
        waiters = waiters.filter(isActive=False)

    # جستجو
    search_query = request.GET.get('search')
    if search_query:
        waiters = waiters.filter(
            Q(fullname__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(mobileNumber__icontains=search_query)
        )

    # مرتب‌سازی
    sort_by = request.GET.get('sort', '-createdAt')
    if sort_by in ['fullname', 'code', 'age', 'createdAt', '-createdAt']:
        waiters = waiters.order_by(sort_by)

    # صفحه‌بندی
    paginator = Paginator(waiters, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # آمار برای فیلترها
    total_count = waiters.count()
    active_count = waiters.filter(isActive=True).count()
    inactive_count = waiters.filter(isActive=False).count()

    context = {
        'restaurants': user_restaurants,
        'page_obj': page_obj,
        'total_count': total_count,
        'active_count': active_count,
        'inactive_count': inactive_count,
        'current_restaurant_id': restaurant_id,
        'status_filter': status_filter,
        'search_query': search_query,
        'sort_by': sort_by,
        'current_tab': 'list'
    }

    return render(request, 'waiter_app/waiter_list.html', context)

@login_required
def waiter_create(request):
    """
    ایجاد گارسون جدید
    """
    user_restaurants = Restaurant.objects.filter(owner=request.user)

    if request.method == 'POST':
        # فقط restaurant_queryset پاس داده شود - بدون user
        form = WaiterForm(request.POST, restaurant_queryset=user_restaurants)
        if form.is_valid():
            try:
                waiter = form.save()
                messages.success(request, f"گارسون {waiter.fullname} با موفقیت ایجاد شد.")
                return redirect('waiter:waiter_detail', pk=waiter.id)

            except Exception as e:
                messages.error(request, f"خطا در ایجاد گارسون: {str(e)}")
    else:
        # فقط restaurant_queryset پاس داده شود - بدون user
        form = WaiterForm(restaurant_queryset=user_restaurants)

    context = {
        'form': form,
        'restaurants': user_restaurants,
        'current_tab': 'create',
        'title': 'ایجاد گارسون جدید'
    }

    return render(request, 'waiter_app/waiter_form.html', context)

@login_required
def waiter_detail(request, pk):
    """
    جزئیات کامل یک گارسون با آمار و گزارش‌ها
    """
    waiter = get_object_or_404(Waiter, id=pk, restaurant__owner=request.user)

    # بازه زمانی برای آمار (پیش‌فرض 30 روز گذشته)
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)

    # سفارش‌ها در بازه زمانی
    orders = Order.objects.filter(
        waiter=waiter,
        createdAt__gte=start_date
    ).order_by('-createdAt')

    # آمار کلی
    total_orders = orders.count()
    completed_orders = orders.filter(status__in=['served', 'paid']).count()
    cancelled_orders = orders.filter(status='cancelled').count()

    # مجموع مبالغ
    total_revenue = orders.aggregate(
        total=Sum('final_price')
    )['total'] or 0

    # آخرین سفارش‌ها
    recent_orders = orders[:10]

    context = {
        'waiter': waiter,
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'days_range': days,
        'current_tab': 'detail'
    }

    return render(request, 'waiter_app/waiter_detail.html', context)

@login_required
def waiter_edit(request, pk):
    """
    ویرایش اطلاعات گارسون
    """
    waiter = get_object_or_404(Waiter, id=pk, restaurant__owner=request.user)

    if request.method == 'POST':
        # فقط instance پاس داده شود - بدون user
        form = WaiterEditForm(request.POST, instance=waiter)
        if form.is_valid():
            try:
                updated_waiter = form.save()
                messages.success(request, f"اطلاعات گارسون {updated_waiter.fullname} با موفقیت بروزرسانی شد.")
                return redirect('waiter:waiter_detail', pk=updated_waiter.id)

            except Exception as e:
                messages.error(request, f"خطا در بروزرسانی اطلاعات: {str(e)}")
    else:
        # فقط instance پاس داده شود - بدون user
        form = WaiterEditForm(instance=waiter)

    context = {
        'form': form,
        'waiter': waiter,
        'restaurants': Restaurant.objects.filter(owner=request.user),
        'current_tab': 'edit',
        'title': f'ویرایش گارسون - {waiter.fullname}'
    }

    return render(request, 'waiter_app/waiter_form.html', context)

@login_required
@require_http_methods(["POST"])
def waiter_toggle_active(request, pk):
    """
    تغییر وضعیت فعال/غیرفعال گارسون
    """
    waiter = get_object_or_404(Waiter, id=pk, restaurant__owner=request.user)

    try:
        if waiter.isActive:
            # بررسی اینکه گارسون سفارش فعال ندارد
            if waiter.active_orders_count > 0:
                return JsonResponse({
                    'success': False,
                    'message': 'امکان غیرفعال کردن گارسون با سفارش‌های فعال وجود ندارد'
                })

            waiter.isActive = False
            action = 'غیرفعال'
        else:
            waiter.isActive = True
            action = 'فعال'

        waiter.save()

        return JsonResponse({
            'success': True,
            'message': f'گارسون با موفقیت {action} شد',
            'is_active': waiter.isActive
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در تغییر وضعیت: {str(e)}'
        })

@login_required
@require_http_methods(["POST"])
def waiter_delete(request, pk):
    """
    حذف گارسون (فقط اگر سفارش فعال نداشته باشد)
    """
    waiter = get_object_or_404(Waiter, id=pk, restaurant__owner=request.user)

    try:
        # بررسی وجود سفارش‌های مرتبط
        if waiter.orders.exists():
            return JsonResponse({
                'success': False,
                'message': 'امکان حذف گارسون با سابقه سفارش وجود ندارد'
            })

        waiter_name = waiter.fullname
        waiter.delete()

        messages.success(request, f"گارسون {waiter_name} با موفقیت حذف شد.")
        return JsonResponse({
            'success': True,
            'message': 'گارسون با موفقیت حذف شد',
            'redirect_url': '/waiter_app/'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در حذف گارسون: {str(e)}'
        })

@login_required
def waiter_analytics(request):
    """
    آمار و تحلیل‌های پیشرفته گارسون‌ها
    """
    user_restaurants = Restaurant.objects.filter(owner=request.user)

    # فیلتر رستوران
    restaurant_id = request.GET.get('restaurant')
    if restaurant_id:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id, owner=request.user)
        waiters = Waiter.objects.filter(restaurant=restaurant)
    else:
        restaurant = None
        waiters = Waiter.objects.filter(restaurant__in=user_restaurants)

    # بازه زمانی
    days = int(request.GET.get('days', 30))
    start_date = timezone.now() - timedelta(days=days)

    # آمار کلی گارسون‌ها
    waiter_analytics = []
    for waiter in waiters:
        waiter_orders = Order.objects.filter(
            waiter=waiter,
            createdAt__gte=start_date
        )

        total_orders = waiter_orders.count()
        completed_orders = waiter_orders.filter(status__in=['served', 'paid']).count()
        cancelled_orders = waiter_orders.filter(status='cancelled').count()

        if total_orders > 0:
            completion_rate = (completed_orders / total_orders) * 100
            cancellation_rate = (cancelled_orders / total_orders) * 100
        else:
            completion_rate = 0
            cancellation_rate = 0

        total_revenue = waiter_orders.aggregate(
            total=Sum('final_price')
        )['total'] or 0

        waiter_analytics.append({
            'waiter': waiter,
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'cancelled_orders': cancelled_orders,
            'completion_rate': round(completion_rate, 1),
            'cancellation_rate': round(cancellation_rate, 1),
            'total_revenue': total_revenue,
        })

    context = {
        'restaurants': user_restaurants,
        'selected_restaurant': restaurant,
        'waiter_analytics': waiter_analytics,
        'days_range': days,
        'current_tab': 'analytics'
    }

    return render(request, 'waiter_app/waiter_analytics.html', context)

@login_required
def waiter_export(request):
    """
    خروجی گرفتن از اطلاعات گارسون‌ها
    """
    user_restaurants = Restaurant.objects.filter(owner=request.user)
    waiters = Waiter.objects.filter(restaurant__in=user_restaurants)

    # فرمت خروجی
    export_format = request.GET.get('format', 'csv')

    if export_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="waiters.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'کد گارسون', 'نام کامل', 'شماره موبایل', 'سن', 'رستوران',
            'وضعیت', 'تعداد سفارش‌های فعال', 'تعداد سفارش‌های امروز',
            'تاریخ ایجاد'
        ])

        for waiter in waiters:
            writer.writerow([
                waiter.code,
                waiter.fullname,
                waiter.mobileNumber,
                waiter.age or '-',
                waiter.restaurant.title,
                'فعال' if waiter.isActive else 'غیرفعال',
                waiter.active_orders_count,
                waiter.today_orders_count,
                waiter.createdAt.strftime('%Y-%m-%d %H:%M')
            ])

        return response

    else:
        messages.error(request, "فرمت خروجی پشتیبانی نمی‌شود.")
        return redirect('waiter:waiter_list')
# ----------------------------
# Utility Functions
# ----------------------------

def get_waiter_avg_preparation_time(waiter, days=30):
    """
    محاسبه میانگین زمان آماده‌سازی سفارش‌های گارسون
    """
    start_date = timezone.now() - timedelta(days=days)

    orders = Order.objects.filter(
        waiter=waiter,
        status__in=['served', 'paid'],
        prepared_at__isnull=False,
        confirmed_at__isnull=False,
        createdAt__gte=start_date
    )

    total_seconds = 0
    count = 0

    for order in orders:
        if order.preparation_time:
            total_seconds += order.preparation_time.total_seconds()
            count += 1

    if count > 0:
        avg_seconds = total_seconds / count
        avg_minutes = avg_seconds / 60
        return round(avg_minutes, 1)

    return 0

def get_waiter_total_served_amount(waiter, days=30):
    """
    محاسبه مجموع مبلغ سفارش‌های سرو شده توسط گارسون
    """
    start_date = timezone.now() - timedelta(days=days)

    total = Order.objects.filter(
        waiter=waiter,
        status__in=['served', 'paid'],
        createdAt__gte=start_date
    ).aggregate(
        total=Sum('final_price')
    )['total'] or 0

    return total

def get_waiter_daily_stats(waiter, days=30):
    """
    آمار روزانه سفارش‌های گارسون برای نمودار
    """
    start_date = timezone.now() - timedelta(days=days)

    from django.db.models.functions import TruncDate
    from django.db.models import Count

    daily_stats = Order.objects.filter(
        waiter=waiter,
        createdAt__gte=start_date
    ).annotate(
        date=TruncDate('createdAt')
    ).values('date').annotate(
        order_count=Count('id'),
        total_revenue=Sum('final_price')
    ).order_by('date')

    result = {
        'dates': [],
        'order_counts': [],
        'revenues': []
    }

    for stat in daily_stats:
        result['dates'].append(stat['date'].strftime('%Y-%m-%d'))
        result['order_counts'].append(stat['order_count'])
        result['revenues'].append(stat['total_revenue'] or 0)

    return result

def get_waiter_popular_foods(waiter, days=30, limit=5):
    """
    محبوب‌ترین غذاهای سرو شده توسط گارسون
    """
    start_date = timezone.now() - timedelta(days=days)

    from django.db.models import Count

    popular_foods = Order.objects.filter(
        waiter=waiter,
        createdAt__gte=start_date
    ).values(
        'items__food__title',
        'items__food__id'
    ).annotate(
        total_ordered=Count('items'),
        total_quantity=Sum('items__quantity')
    ).order_by('-total_quantity')[:limit]

    return popular_foods

def calculate_efficiency_score(completion_rate, cancellation_rate, avg_preparation_time):
    """
    محاسبه امتیاز کارایی گارسون
    """
    # نرمال‌سازی زمان آماده‌سازی (فرض: زمان ایده‌آل 20 دقیقه)
    ideal_time = 20
    if avg_preparation_time > 0:
        time_score = max(0, 100 - (avg_preparation_time - ideal_time) * 2)
    else:
        time_score = 50  # مقدار پیش‌فرض برای گارسون‌های بدون سابقه

    # محاسبه امتیاز نهایی
    efficiency_score = (
        completion_rate * 0.5 +          # 50% نرخ تکمیل
        (100 - cancellation_rate) * 0.3 + # 30% نرخ عدم لغو
        time_score * 0.2                  # 20% سرعت
    )

    return round(efficiency_score, 1)




# apps/waiter/views.py
@login_required
def waiter_panel(request, pk):
    """
    پنل real-time گارسون برای دریافت سفارش‌ها
    """
    waiter = get_object_or_404(Waiter, id=pk, restaurant__owner=request.user)

    context = {
        'waiter': waiter,
        'restaurant': waiter.restaurant,
        'current_tab': 'panel'
    }

    return render(request, 'waiter_app/waiter_panel.html', context)