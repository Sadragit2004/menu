from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from django.db.models import Count, Sum, Avg, Q, F
from django.db.models.functions import TruncDate, TruncWeek, TruncMonth, TruncYear
from django.http import JsonResponse
import json
from datetime import timedelta, datetime
from ...models.menufreemodels.models import (
    Restaurant, MenuView, Food,
     MenuCategory, Category
)

from apps.waiter.models import Waiter,Order,OrderItem

from django.db.models import (
    Count, Sum, Avg, Q, F, Min, Max,
    ExpressionWrapper, DurationField,
    Case, When, Value, FloatField
)


@staff_member_required
def analytics_dashboard(request):
    """داشبورد اصلی آمار و آنالیتیکس"""
    context = {
        'title': 'داشبورد آمار و آنالیتیکس',
        'restaurants': Restaurant.objects.filter(isActive=True)
    }
    return render(request, 'menuview_app/dashboard.html', context)

@staff_member_required
def api_daily_views(request):
    """آمار بازدیدهای روزانه"""
    days = int(request.GET.get('days', 30))
    restaurant_id = request.GET.get('restaurant_id')

    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)

    queryset = MenuView.objects.filter(created_at__gte=start_date)

    if restaurant_id:
        queryset = queryset.filter(restaurant_id=restaurant_id)

    daily_views = queryset.annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        views=Count('id')
    ).order_by('date')

    # پر کردن تاریخ‌های فاقد داده
    dates = []
    current_date = start_date.date()
    while current_date <= end_date.date():
        dates.append(current_date)
        current_date += timedelta(days=1)

    result = []
    for date in dates:
        view_data = next((item for item in daily_views if item['date'] == date), None)
        result.append({
            'date': date.strftime('%Y-%m-%d'),
            'views': view_data['views'] if view_data else 0
        })

    return JsonResponse(result, safe=False)

@staff_member_required
def api_weekly_views(request):
    """آمار بازدیدهای هفتگی"""
    weeks = int(request.GET.get('weeks', 12))
    restaurant_id = request.GET.get('restaurant_id')

    end_date = timezone.now()
    start_date = end_date - timedelta(weeks=weeks)

    queryset = MenuView.objects.filter(created_at__gte=start_date)

    if restaurant_id:
        queryset = queryset.filter(restaurant_id=restaurant_id)

    weekly_views = queryset.annotate(
        week=TruncWeek('created_at')
    ).values('week').annotate(
        views=Count('id')
    ).order_by('week')

    return JsonResponse(list(weekly_views), safe=False)

@staff_member_required
def api_monthly_views(request):
    """آمار بازدیدهای ماهانه"""
    months = int(request.GET.get('months', 12))
    restaurant_id = request.GET.get('restaurant_id')

    end_date = timezone.now()
    start_date = end_date - timedelta(days=months*30)

    queryset = MenuView.objects.filter(created_at__gte=start_date)

    if restaurant_id:
        queryset = queryset.filter(restaurant_id=restaurant_id)

    monthly_views = queryset.annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        views=Count('id')
    ).order_by('month')

    return JsonResponse(list(monthly_views), safe=False)

@staff_member_required
def api_top_foods(request):
    """لیست غذاهای پرفروش"""
    restaurant_id = request.GET.get('restaurant_id')
    limit = int(request.GET.get('limit', 10))

    queryset = OrderItem.objects.filter(
        order__status__in=['confirmed', 'preparing', 'ready', 'served', 'paid']
    )

    if restaurant_id:
        queryset = queryset.filter(order__restaurant_id=restaurant_id)

    top_foods = queryset.values(
        'food__title',
        'food__id'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('final_price')),
        order_count=Count('order', distinct=True)
    ).order_by('-total_quantity')[:limit]

    result = []
    for food in top_foods:
        result.append({
            'food_name': food['food__title'],
            'food_id': food['food__id'],
            'total_quantity': food['total_quantity'] or 0,
            'total_revenue': food['total_revenue'] or 0,
            'order_count': food['order_count'] or 0
        })

    return JsonResponse(result, safe=False)

@staff_member_required
def api_low_performing_foods(request):
    """لیست غذاهای کم‌فروش"""
    restaurant_id = request.GET.get('restaurant_id')
    limit = int(request.GET.get('limit', 10))

    queryset = OrderItem.objects.filter(
        order__status__in=['confirmed', 'preparing', 'ready', 'served', 'paid']
    )

    if restaurant_id:
        queryset = queryset.filter(order__restaurant_id=restaurant_id)

    # غذاهایی که در 30 روز گذشته فروش کمی داشته‌اند
    thirty_days_ago = timezone.now() - timedelta(days=30)
    low_foods = queryset.filter(
        order__createdAt__gte=thirty_days_ago
    ).values(
        'food__title',
        'food__id'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('final_price')),
        order_count=Count('order', distinct=True)
    ).order_by('total_quantity')[:limit]

    result = []
    for food in low_foods:
        result.append({
            'food_name': food['food__title'],
            'food_id': food['food__id'],
            'total_quantity': food['total_quantity'] or 0,
            'total_revenue': food['total_revenue'] or 0,
            'order_count': food['order_count'] or 0
        })

    return JsonResponse(result, safe=False)

@staff_member_required
def api_customer_notes_analysis(request):
    """آنالیز نظرات و نوت‌های مشتریان"""
    restaurant_id = request.GET.get('restaurant_id')
    limit = int(request.GET.get('limit', 50))

    queryset = Order.objects.filter(
        customer_notes__isnull=False
    ).exclude(
        customer_notes__exact=''
    )

    if restaurant_id:
        queryset = queryset.filter(restaurant_id=restaurant_id)

    notes = queryset.values(
        'id',
        'customer_notes',
        'table_number',
        'createdAt',
        'restaurant__title'
    ).order_by('-createdAt')[:limit]

    result = []
    for note in notes:
        result.append({
            'order_id': note['id'],
            'note': note['customer_notes'],
            'table_number': note['table_number'] or 'نامشخص',
            'date': note['createdAt'].strftime('%Y-%m-%d %H:%M'),
            'restaurant': note['restaurant__title']
        })

    return JsonResponse(result, safe=False)

@staff_member_required
def api_order_analytics(request):
    """آمار کلی سفارش‌ها"""
    restaurant_id = request.GET.get('restaurant_id')

    # امروز
    today = timezone.now().date()
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))

    # این هفته
    week_start = today - timedelta(days=today.weekday())
    week_start = timezone.make_aware(datetime.combine(week_start, datetime.min.time()))

    # این ماه
    month_start = today.replace(day=1)
    month_start = timezone.make_aware(datetime.combine(month_start, datetime.min.time()))

    queryset = Order.objects.all()
    if restaurant_id:
        queryset = queryset.filter(restaurant_id=restaurant_id)

    # آمار امروز
    today_stats = queryset.filter(createdAt__gte=today_start).aggregate(
        total_orders=Count('id'),
        total_revenue=Sum('final_price'),
        avg_order_value=Avg('final_price')
    )

    # آمار این هفته
    week_stats = queryset.filter(createdAt__gte=week_start).aggregate(
        total_orders=Count('id'),
        total_revenue=Sum('final_price'),
        avg_order_value=Avg('final_price')
    )

    # آمار این ماه
    month_stats = queryset.filter(createdAt__gte=month_start).aggregate(
        total_orders=Count('id'),
        total_revenue=Sum('final_price'),
        avg_order_value=Avg('final_price')
    )

    # آمار وضعیت سفارش‌ها
    status_stats = queryset.values('status').annotate(
        count=Count('id'),
        revenue=Sum('final_price')
    ).order_by('status')

    result = {
        'today': today_stats,
        'week': week_stats,
        'month': month_stats,
        'status_breakdown': list(status_stats)
    }

    return JsonResponse(result)

@staff_member_required
def api_waiter_performance(request):
    """عملکرد گارسون‌ها"""
    restaurant_id = request.GET.get('restaurant_id')

    queryset = Waiter.objects.filter(isActive=True)

    if restaurant_id:
        queryset = queryset.filter(restaurant_id=restaurant_id)

    waiter_stats = queryset.annotate(
        total_orders=Count('orders'),
        completed_orders=Count('orders', filter=Q(orders__status__in=['served', 'paid'])),
        total_revenue=Sum('orders__final_price'),
        avg_rating=Avg('orders__rating')  # اگر فیلد ریتینگ داشته باشید
    ).order_by('-total_orders')

    result = []
    for waiter in waiter_stats:
        completion_rate = (waiter.completed_orders / waiter.total_orders * 100) if waiter.total_orders > 0 else 0

        result.append({
            'waiter_name': waiter.fullname,
            'waiter_code': waiter.code,
            'total_orders': waiter.total_orders,
            'completed_orders': waiter.completed_orders,
            'completion_rate': round(completion_rate, 1),
            'total_revenue': waiter.total_revenue or 0,
            'avg_rating': round(waiter.avg_rating or 0, 1)
        })

    return JsonResponse(result, safe=False)

@staff_member_required
def api_category_analytics(request):
    """آمار دسته‌بندی‌ها"""
    restaurant_id = request.GET.get('restaurant_id')

    queryset = OrderItem.objects.filter(
        order__status__in=['confirmed', 'preparing', 'ready', 'served', 'paid']
    )

    if restaurant_id:
        queryset = queryset.filter(order__restaurant_id=restaurant_id)

    category_stats = queryset.values(
        'food__menuCategory__category__title',
        'food__menuCategory__id'
    ).annotate(
        total_orders=Count('order', distinct=True),
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('final_price'))
    ).order_by('-total_revenue')

    result = []
    for category in category_stats:
        result.append({
            'category_name': category['food__menuCategory__category__title'] or 'دسته‌بندی نشده',
            'category_id': category['food__menuCategory__id'],
            'total_orders': category['total_orders'] or 0,
            'total_quantity': category['total_quantity'] or 0,
            'total_revenue': category['total_revenue'] or 0
        })

    return JsonResponse(result, safe=False)

@staff_member_required
def api_real_time_stats(request):
    """آمار لحظه‌ای"""
    restaurant_id = request.GET.get('restaurant_id')

    # بازدیدهای امروز
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_views = MenuView.objects.filter(created_at__gte=today_start)

    # سفارش‌های فعال
    active_orders = Order.objects.filter(
        status__in=['pending', 'confirmed', 'preparing', 'ready']
    )

    if restaurant_id:
        today_views = today_views.filter(restaurant_id=restaurant_id)
        active_orders = active_orders.filter(restaurant_id=restaurant_id)

    result = {
        'today_views': today_views.count(),
        'active_orders': active_orders.count(),
        'online_waiters': Waiter.objects.filter(isActive=True).count(),
        'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    return JsonResponse(result)

@staff_member_required
def api_peak_hours(request):
    """ساعات پیک بازدید و سفارش"""
    restaurant_id = request.GET.get('restaurant_id')
    days = int(request.GET.get('days', 7))

    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)

    # آمار ساعات پیک بازدید
    view_hours = MenuView.objects.filter(
        created_at__gte=start_date
    ).extra({
        'hour': "EXTRACT(hour FROM created_at)"
    }).values('hour').annotate(
        views=Count('id')
    ).order_by('hour')

    # آمار ساعات پیک سفارش
    order_hours = Order.objects.filter(
        createdAt__gte=start_date
    ).extra({
        'hour': "EXTRACT(hour FROM createdAt)"
    }).values('hour').annotate(
        orders=Count('id')
    ).order_by('hour')

    if restaurant_id:
        view_hours = view_hours.filter(restaurant_id=restaurant_id)
        order_hours = order_hours.filter(restaurant_id=restaurant_id)

    result = {
        'view_peak_hours': list(view_hours),
        'order_peak_hours': list(order_hours)
    }

    return JsonResponse(result)

@staff_member_required
def api_customer_behavior(request):
    """رفتار مشتریان"""
    restaurant_id = request.GET.get('restaurant_id')

    # میانگین زمان بین بازدید و سفارش
    # مشتریانی که بیشترین سفارش را داشته‌اند
    # ارزش طول عمر مشتری (CLV)

    queryset = Order.objects.filter(
        status__in=['confirmed', 'preparing', 'ready', 'served', 'paid']
    )

    if restaurant_id:
        queryset = queryset.filter(restaurant_id=restaurant_id)

    customer_stats = queryset.values(
        'session_key'
    ).annotate(
        total_orders=Count('id'),
        total_spent=Sum('final_price'),
        first_order=Min('createdAt'),
        last_order=Max('createdAt')
    ).order_by('-total_spent')[:20]

    result = []
    for customer in customer_stats:
        result.append({
            'session_key': customer['session_key'][:10] + '...',  # مخفی کردن برای حفظ حریم خصوصی
            'total_orders': customer['total_orders'],
            'total_spent': customer['total_spent'] or 0,
            'first_order': customer['first_order'].strftime('%Y-%m-%d'),
            'last_order': customer['last_order'].strftime('%Y-%m-%d'),
            'avg_order_value': (customer['total_spent'] or 0) / customer['total_orders'] if customer['total_orders'] > 0 else 0
        })

    return JsonResponse(result, safe=False)

@staff_member_required
def api_revenue_analytics(request):
    """آمار درآمد و مالی"""
    restaurant_id = request.GET.get('restaurant_id')
    days = int(request.GET.get('days', 30))

    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)

    queryset = Order.objects.filter(
        createdAt__gte=start_date,
        status__in=['confirmed', 'preparing', 'ready', 'served', 'paid']
    )

    if restaurant_id:
        queryset = queryset.filter(restaurant_id=restaurant_id)

    # درآمد روزانه
    daily_revenue = queryset.annotate(
        date=TruncDate('createdAt')
    ).values('date').annotate(
        revenue=Sum('final_price'),
        orders=Count('id'),
        avg_order_value=Avg('final_price')
    ).order_by('date')

    # درآمد بر اساس دسته‌بندی
    category_revenue = OrderItem.objects.filter(
        order__in=queryset
    ).values(
        'food__menuCategory__category__title'
    ).annotate(
        revenue=Sum(F('quantity') * F('final_price')),
        orders=Count('order', distinct=True)
    ).order_by('-revenue')

    result = {
        'daily_revenue': list(daily_revenue),
        'category_revenue': list(category_revenue),
        'total_revenue': queryset.aggregate(total=Sum('final_price'))['total'] or 0,
        'total_orders': queryset.count(),
        'avg_daily_revenue': queryset.aggregate(avg=Avg('final_price'))['avg'] or 0
    }

    return JsonResponse(result)





@staff_member_required
def api_food_preparation_analytics(request):
    """آمار زمان آماده‌سازی غذاها"""
    restaurant_id = request.GET.get('restaurant_id')

    queryset = Order.objects.filter(
        status__in=['served', 'paid'],
        prepared_at__isnull=False,
        confirmed_at__isnull=False
    )

    if restaurant_id:
        queryset = queryset.filter(restaurant_id=restaurant_id)

    # محاسبه زمان آماده‌سازی
    from django.db.models import ExpressionWrapper, DurationField
    preparation_stats = queryset.annotate(
        prep_time=ExpressionWrapper(
            F('prepared_at') - F('confirmed_at'),
            output_field=DurationField()
        )
    ).aggregate(
        avg_prep_time=Avg('prep_time'),
        max_prep_time=Max('prep_time'),
        min_prep_time=Min('prep_time'),
        total_orders=Count('id')
    )

    # آمار زمان آماده‌سازی بر اساس غذا
    food_prep_stats = OrderItem.objects.filter(
        order__in=queryset
    ).values(
        'food__title',
        'food__id'
    ).annotate(
        avg_prep_time=Avg('order__prepared_at' - 'order__confirmed_at'),
        order_count=Count('id'),
        total_quantity=Sum('quantity')
    ).order_by('-order_count')[:10]

    # فرمت کردن زمان‌ها
    def format_timedelta(td):
        if td is None:
            return "نامشخص"
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        if hours > 0:
            return f"{hours} ساعت و {minutes} دقیقه"
        elif minutes > 0:
            return f"{minutes} دقیقه و {seconds} ثانیه"
        else:
            return f"{seconds} ثانیه"

    result = {
        'overall_prep_stats': {
            'avg_prep_time': format_timedelta(preparation_stats['avg_prep_time']),
            'max_prep_time': format_timedelta(preparation_stats['max_prep_time']),
            'min_prep_time': format_timedelta(preparation_stats['min_prep_time']),
            'total_orders': preparation_stats['total_orders'] or 0
        },
        'food_prep_stats': [
            {
                'food_name': stat['food__title'],
                'food_id': stat['food__id'],
                'avg_prep_time': format_timedelta(stat['avg_prep_time']),
                'order_count': stat['order_count'] or 0,
                'total_quantity': stat['total_quantity'] or 0
            }
            for stat in food_prep_stats
        ]
    }

    return JsonResponse(result)

@staff_member_required
def api_restaurant_comparison(request):
    """مقایسه عملکرد رستوران‌ها"""
    # آمار کلی همه رستوران‌ها
    restaurants_stats = Restaurant.objects.filter(isActive=True).annotate(
        total_views=Count('menu_views'),
        total_orders=Count('orders'),
        total_revenue=Sum('orders__final_price'),
        avg_order_value=Avg('orders__final_price'),
        active_orders=Count('orders', filter=Q(orders__status__in=['pending', 'confirmed', 'preparing', 'ready'])),
        completed_orders=Count('orders', filter=Q(orders__status__in=['served', 'paid']))
    ).order_by('-total_revenue')

    # محاسبه نرخ تبدیل (بازدید به سفارش)
    result = []
    for restaurant in restaurants_stats:
        conversion_rate = (restaurant.total_orders / restaurant.total_views * 100) if restaurant.total_views > 0 else 0
        completion_rate = (restaurant.completed_orders / restaurant.total_orders * 100) if restaurant.total_orders > 0 else 0

        result.append({
            'restaurant_name': restaurant.title,
            'restaurant_id': restaurant.id,
            'total_views': restaurant.total_views or 0,
            'total_orders': restaurant.total_orders or 0,
            'total_revenue': restaurant.total_revenue or 0,
            'avg_order_value': restaurant.avg_order_value or 0,
            'active_orders': restaurant.active_orders or 0,
            'completion_rate': round(completion_rate, 1),
            'conversion_rate': round(conversion_rate, 1),
            'performance_score': calculate_performance_score(
                restaurant.total_orders or 0,
                restaurant.total_revenue or 0,
                completion_rate
            )
        })

    return JsonResponse(result, safe=False)

def calculate_performance_score(orders, revenue, completion_rate):
    """محاسبه امتیاز عملکرد رستوران"""
    # نرمالایز کردن مقادیر
    orders_score = min(orders / 100, 1.0) * 40  # حداکثر 40 امتیاز برای تعداد سفارشات
    revenue_score = min(revenue / 10000000, 1.0) * 40  # حداکثر 40 امتیاز برای درآمد (10 میلیون)
    completion_score = (completion_rate / 100) * 20  # 20 امتیاز برای نرخ تکمیل

    total_score = orders_score + revenue_score + completion_score
    return round(total_score, 1)

@staff_member_required
def api_restaurant_ranking(request):
    """رتبه‌بندی رستوران‌ها بر اساس معیارهای مختلف"""
    restaurant_id = request.GET.get('restaurant_id')

    # رتبه‌بندی بر اساس درآمد
    revenue_ranking = Restaurant.objects.filter(isActive=True).annotate(
        total_revenue=Sum('orders__final_price')
    ).exclude(total_revenue__isnull=True).order_by('-total_revenue')

    # رتبه‌بندی بر اساس تعداد سفارشات
    orders_ranking = Restaurant.objects.filter(isActive=True).annotate(
        total_orders=Count('orders')
    ).exclude(total_orders__isnull=True).order_by('-total_orders')

    # رتبه‌بندی بر اساس بازدید
    views_ranking = Restaurant.objects.filter(isActive=True).annotate(
        total_views=Count('menu_views')
    ).exclude(total_views__isnull=True).order_by('-total_views')

    # رتبه‌بندی بر اساس نرخ تبدیل
    conversion_ranking = Restaurant.objects.filter(isActive=True).annotate(
        total_views=Count('menu_views'),
        total_orders=Count('orders')
    ).exclude(total_views__isnull=True, total_orders__isnull=True).annotate(
        conversion_rate=Case(
            When(total_views=0, then=Value(0)),
            default=F('total_orders') * 100.0 / F('total_views'),
            output_field=FloatField()
        )
    ).order_by('-conversion_rate')

    result = {
        'revenue_ranking': [
            {
                'rank': idx + 1,
                'restaurant_name': restaurant.title,
                'restaurant_id': restaurant.id,
                'value': restaurant.total_revenue or 0,
                'metric': 'درآمد'
            }
            for idx, restaurant in enumerate(revenue_ranking[:10])
        ],
        'orders_ranking': [
            {
                'rank': idx + 1,
                'restaurant_name': restaurant.title,
                'restaurant_id': restaurant.id,
                'value': restaurant.total_orders or 0,
                'metric': 'تعداد سفارشات'
            }
            for idx, restaurant in enumerate(orders_ranking[:10])
        ],
        'views_ranking': [
            {
                'rank': idx + 1,
                'restaurant_name': restaurant.title,
                'restaurant_id': restaurant.id,
                'value': restaurant.total_views or 0,
                'metric': 'بازدید'
            }
            for idx, restaurant in enumerate(views_ranking[:10])
        ],
        'conversion_ranking': [
            {
                'rank': idx + 1,
                'restaurant_name': restaurant.title,
                'restaurant_id': restaurant.id,
                'value': round(restaurant.conversion_rate or 0, 1),
                'metric': 'نرخ تبدیل'
            }
            for idx, restaurant in enumerate(conversion_ranking[:10])
        ]
    }

    return JsonResponse(result)

@staff_member_required
def api_trend_analysis(request):
    """آنالیز روندها و پیش‌بینی‌ها"""
    restaurant_id = request.GET.get('restaurant_id')
    days = int(request.GET.get('days', 30))

    end_date = timezone.now()
    start_date = end_date - timedelta(days=days)

    # داده‌های تاریخی
    daily_data = Order.objects.filter(
        createdAt__gte=start_date,
        status__in=['confirmed', 'preparing', 'ready', 'served', 'paid']
    )

    if restaurant_id:
        daily_data = daily_data.filter(restaurant_id=restaurant_id)

    daily_stats = daily_data.annotate(
        date=TruncDate('createdAt')
    ).values('date').annotate(
        orders=Count('id'),
        revenue=Sum('final_price'),
        avg_order_value=Avg('final_price')
    ).order_by('date')

    # محاسبه روندها
    if len(daily_stats) >= 2:
        first_day = daily_stats[0]
        last_day = daily_stats[-1]

        orders_growth = ((last_day['orders'] - first_day['orders']) / first_day['orders'] * 100) if first_day['orders'] > 0 else 0
        revenue_growth = ((last_day['revenue'] - first_day['revenue']) / first_day['revenue'] * 100) if first_day['revenue'] > 0 else 0
        avg_order_growth = ((last_day['avg_order_value'] - first_day['avg_order_value']) / first_day['avg_order_value'] * 100) if first_day['avg_order_value'] > 0 else 0
    else:
        orders_growth = revenue_growth = avg_order_growth = 0

    # پیش‌بینی ساده (میانگین 7 روز آخر)
    recent_days = daily_stats.order_by('-date')[:7]
    if recent_days:
        avg_recent_orders = sum(day['orders'] for day in recent_days) / len(recent_days)
        avg_recent_revenue = sum(day['revenue'] or 0 for day in recent_days) / len(recent_days)
    else:
        avg_recent_orders = avg_recent_revenue = 0

    result = {
        'historical_data': list(daily_stats),
        'growth_rates': {
            'orders': round(orders_growth, 1),
            'revenue': round(revenue_growth, 1),
            'avg_order_value': round(avg_order_growth, 1)
        },
        'predictions': {
            'next_day_orders': round(avg_recent_orders),
            'next_day_revenue': round(avg_recent_revenue),
            'confidence': 'متوسط' if len(recent_days) >= 3 else 'پایین'
        },
        'insights': generate_insights(daily_stats)
    }

    return JsonResponse(result)

def generate_insights(daily_stats):
    """تولید بینش‌های خودکار از داده‌ها"""
    insights = []

    if not daily_stats:
        return ["داده کافی برای تحلیل موجود نیست"]

    # تحلیل روزهای پیک
    peak_day = max(daily_stats, key=lambda x: x['orders'])
    low_day = min(daily_stats, key=lambda x: x['orders'])

    insights.append(f"پربازدیدترین روز: {peak_day['date'].strftime('%Y-%m-%d')} با {peak_day['orders']} سفارش")
    insights.append(f"کم‌بازدیدترین روز: {low_day['date'].strftime('%Y-%m-%d')} با {low_day['orders']} سفارش")

    # تحلیل روند
    if len(daily_stats) >= 7:
        last_week_avg = sum(day['orders'] for day in daily_stats[-7:]) / 7
        previous_week_avg = sum(day['orders'] for day in daily_stats[-14:-7]) / 7 if len(daily_stats) >= 14 else last_week_avg

        if last_week_avg > previous_week_avg:
            growth = ((last_week_avg - previous_week_avg) / previous_week_avg * 100)
            insights.append(f"رشد مثبت هفته اخیر: +{growth:.1f}% نسبت به هفته قبل")
        else:
            decline = ((previous_week_avg - last_week_avg) / previous_week_avg * 100)
            insights.append(f"کاهش هفته اخیر: -{decline:.1f}% نسبت به هفته قبل")

    return insights