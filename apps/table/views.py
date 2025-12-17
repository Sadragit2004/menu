# table_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q, Count,Max
from datetime import datetime, date, timedelta, time
import json
import jdatetime
from .models import (
    Restaurant, Table, Reservation, WorkingTime, WorkingDay,
    ReservationSettings, Customer
)

# ----------------------------
# Decorators
# ----------------------------

def restaurant_owner_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'restaurants') or not request.user.restaurants.exists():
            messages.error(request, "شما دسترسی به این بخش را ندارید")
            return redirect('panel:panel')
        return view_func(request, *args, **kwargs)
    return wrapper

def get_restaurant_for_user(user):
    """دریافت رستوران کاربر جاری"""
    return user.restaurants.first()

def get_current_jalali_date():
    """دریافت تاریخ شمسی جاری"""
    return jdatetime.date.today()

def validate_jalali_date(jalali_date_str):
    """اعتبارسنجی تاریخ شمسی"""
    try:
        year, month, day = map(int, jalali_date_str.split('/'))
        jalali_date = jdatetime.JalaliDate(year, month, day)
        return jalali_date, True
    except (ValueError, AttributeError):
        return None, False

# ----------------------------
# Dashboard
# ----------------------------

@login_required
@restaurant_owner_required
def reservation_dashboard(request):
    """داشبورد مدیریت رزرو"""
    restaurant = get_restaurant_for_user(request.user)
    today_jalali = get_current_jalali_date()
    today_jalali_str = today_jalali.strftime('%Y/%m/%d')

    # آمار کلی
    total_tables = Table.objects.filter(restaurant=restaurant).count()
    active_tables = Table.objects.filter(restaurant=restaurant, is_active=True).count()

    # آمار رزروهای امروز
    today_reservations = Reservation.objects.filter(
        table__restaurant=restaurant,
        reservation_jalali_date=today_jalali_str
    )

    today_stats = {
        'total': today_reservations.count(),
        'pending': today_reservations.filter(reservation_status='pending').count(),
        'confirmed': today_reservations.filter(reservation_status='confirmed').count(),
        'seated': today_reservations.filter(reservation_status='seated').count(),
        'completed': today_reservations.filter(reservation_status='completed').count(),
        'cancelled': today_reservations.filter(reservation_status='cancelled').count(),
    }

    # رزروهای فردا
    tomorrow_jalali = today_jalali + jdatetime.timedelta(days=1)
    tomorrow_jalali_str = tomorrow_jalali.strftime('%Y/%m/%d')

    tomorrow_reservations = Reservation.objects.filter(
        table__restaurant=restaurant,
        reservation_jalali_date=tomorrow_jalali_str,
        reservation_status__in=['confirmed', 'pending']
    ).count()

    # آخرین رزروها
    recent_reservations = Reservation.objects.filter(
        table__restaurant=restaurant
    ).select_related('table', 'customer').order_by('-created_jalali')[:5]

    context = {
        'restaurant': restaurant,
        'total_tables': total_tables,
        'active_tables': active_tables,
        'today_stats': today_stats,
        'tomorrow_reservations': tomorrow_reservations,
        'today_jalali': today_jalali_str,
        'recent_reservations': recent_reservations,
    }
    return render(request, 'table_app/dashboard.html', context)

# ----------------------------
# Table Management
# ----------------------------

@login_required
@restaurant_owner_required
def table_list(request):
    """لیست میزها"""
    restaurant = get_restaurant_for_user(request.user)
    tables = Table.objects.filter(restaurant=restaurant).order_by('table_number')

    # فیلترها
    table_type = request.GET.get('table_type')
    is_active = request.GET.get('is_active')

    if table_type:
        tables = tables.filter(table_type=table_type)
    if is_active is not None:
        tables = tables.filter(is_active=(is_active == 'true'))

    # آمار برای هر میز
    for table in tables:
        table.reservation_count = table.reservations.count()
        table.active_reservations = table.reservations.filter(
            reservation_status__in=['pending', 'confirmed', 'seated']
        ).count()

    context = {
        'tables': tables,
        'table_types': Table.TABLE_TYPES,
    }
    return render(request, 'table_app/table_list.html', context)

@login_required
@restaurant_owner_required
def table_detail(request, table_id):
    """جزئیات میز"""
    restaurant = get_restaurant_for_user(request.user)
    table = get_object_or_404(Table, id=table_id, restaurant=restaurant)

    # دریافت رزروها با فیلتر تاریخ شمسی
    reservations = table.reservations.all().order_by('-reservation_jalali_date', '-start_time')

    date_filter = request.GET.get('date')
    if date_filter:
        reservations = reservations.filter(reservation_jalali_date=date_filter)

    status_filter = request.GET.get('status')
    if status_filter:
        reservations = reservations.filter(reservation_status=status_filter)

    context = {
        'table': table,
        'reservations': reservations,
        'status_choices': Reservation.RESERVATION_STATUS,
    }
    return render(request, 'table_app/table_detail.html', context)

@login_required
@restaurant_owner_required
def table_create(request):
    """ایجاد میز جدید"""
    restaurant = get_restaurant_for_user(request.user)

    if request.method == 'POST':
        try:
            table = Table(
                restaurant=restaurant,
                table_number=request.POST.get('table_number'),
                table_type=request.POST.get('table_type'),
                capacity=int(request.POST.get('capacity', 2)),
                description=request.POST.get('description', ''),
                min_reservation_duration=int(request.POST.get('min_reservation_duration', 60)),
                max_reservation_duration=int(request.POST.get('max_reservation_duration', 240)),
                has_view=request.POST.get('has_view') == 'on',
                is_smoking=request.POST.get('is_smoking') == 'on',
                is_vip=request.POST.get('is_vip') == 'on',
                floor=int(request.POST.get('floor', 1)),
                section=request.POST.get('section', ''),
                is_active=request.POST.get('is_active') == 'on'
            )
            table.save()
            messages.success(request, "میز با موفقیت ایجاد شد")
            return redirect('table:table_list')
        except Exception as e:
            messages.error(request, f"خطا در ایجاد میز: {str(e)}")

    context = {
        'table_types': Table.TABLE_TYPES,
        'action': 'create'
    }
    return render(request, 'table_app/table_form.html', context)

@login_required
@restaurant_owner_required
def table_edit(request, table_id):
    """ویرایش میز"""
    restaurant = get_restaurant_for_user(request.user)
    table = get_object_or_404(Table, id=table_id, restaurant=restaurant)

    if request.method == 'POST':
        try:
            table.table_number = request.POST.get('table_number')
            table.table_type = request.POST.get('table_type')
            table.capacity = int(request.POST.get('capacity', 2))
            table.description = request.POST.get('description', '')
            table.min_reservation_duration = int(request.POST.get('min_reservation_duration', 60))
            table.max_reservation_duration = int(request.POST.get('max_reservation_duration', 240))
            table.has_view = request.POST.get('has_view') == 'on'
            table.is_smoking = request.POST.get('is_smoking') == 'on'
            table.is_vip = request.POST.get('is_vip') == 'on'
            table.floor = int(request.POST.get('floor', 1))
            table.section = request.POST.get('section', '')
            table.is_active = request.POST.get('is_active') == 'on'
            table.save()

            messages.success(request, "میز با موفقیت ویرایش شد")
            return redirect('table:table_list')
        except Exception as e:
            messages.error(request, f"خطا در ویرایش میز: {str(e)}")

    context = {
        'table': table,
        'table_types': Table.TABLE_TYPES,
        'action': 'edit'
    }
    return render(request, 'table_app/table_form.html', context)

@login_required
@restaurant_owner_required
def table_delete(request, table_id):
    """حذف میز"""
    restaurant = get_restaurant_for_user(request.user)
    table = get_object_or_404(Table, id=table_id, restaurant=restaurant)

    # بررسی رزروهای فعال
    active_reservations = table.reservations.filter(
        reservation_status__in=['confirmed', 'pending', 'seated']
    ).exists()

    if active_reservations:
        messages.error(request, "امکان حذف میز با رزروهای فعال وجود ندارد")
        return redirect('table:table_list')

    table.delete()
    messages.success(request, "میز با موفقیت حذف شد")
    return redirect('table:table_list')

# ----------------------------
# Customer Management
# ----------------------------

@login_required
@restaurant_owner_required
def customer_list(request):
    """لیست مشتریان"""
    restaurant = get_restaurant_for_user(request.user)

    # دریافت مشتریانی که در این رستوران رزرو داشته‌اند
    customer_ids = Reservation.objects.filter(
        table__restaurant=restaurant
    ).values_list('customer_id', flat=True).distinct()

    customers = Customer.objects.filter(id__in=customer_ids).order_by('-created_jalali')

    # فیلترها
    is_vip = request.GET.get('is_vip')
    search = request.GET.get('search')

    if is_vip is not None:
        customers = customers.filter(is_vip=(is_vip == 'true'))

    if search:
        customers = customers.filter(
            Q(full_name__icontains=search) |
            Q(phone_number__icontains=search) |
            Q(national_code__icontains=search)
        )

    context = {
        'customers': customers,
    }
    return render(request, 'table_app/customer_list.html', context)

@login_required
@restaurant_owner_required
def customer_detail(request, customer_id):
    """جزئیات مشتری"""
    restaurant = get_restaurant_for_user(request.user)

    customer = get_object_or_404(Customer, id=customer_id)

    # دریافت رزروهای مشتری در این رستوران
    reservations = Reservation.objects.filter(
        customer=customer,
        table__restaurant=restaurant
    ).order_by('-reservation_jalali_date', '-start_time')

    context = {
        'customer': customer,
        'reservations': reservations,
    }
    return render(request, 'table_app/customer_detail.html', context)

# ----------------------------
# Reservation Management
# ----------------------------

@login_required
@restaurant_owner_required
def reservation_list(request):
    """لیست رزروها"""
    restaurant = get_restaurant_for_user(request.user)
    reservations = Reservation.objects.filter(
        table__restaurant=restaurant
    ).select_related('table', 'customer').order_by('-reservation_jalali_date', '-start_time')

    # فیلترها
    date_filter = request.GET.get('date')
    status_filter = request.GET.get('status')
    table_filter = request.GET.get('table')
    customer_name_filter = request.GET.get('customer_name')

    if date_filter:
        reservations = reservations.filter(reservation_jalali_date=date_filter)

    if status_filter:
        reservations = reservations.filter(reservation_status=status_filter)

    if table_filter:
        reservations = reservations.filter(table__table_number__icontains=table_filter)

    if customer_name_filter:
        reservations = reservations.filter(customer__full_name__icontains=customer_name_filter)

    context = {
        'reservations': reservations,
        'status_choices': Reservation.RESERVATION_STATUS,
        'tables': Table.objects.filter(restaurant=restaurant),
        'today_jalali': get_current_jalali_date().strftime('%Y/%m/%d'),
    }
    return render(request, 'table_app/reservation_list.html', context)

@login_required
@restaurant_owner_required
def reservation_detail(request, reservation_id):
    """جزئیات رزرو"""
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    context = {
        'reservation': reservation,
    }
    return render(request, 'table_app/reservation_detail.html', context)

@login_required
@restaurant_owner_required
def reservation_create(request):
    """ایجاد رزرو جدید"""
    restaurant = get_restaurant_for_user(request.user)

    if request.method == 'POST':
        try:
            # پیدا کردن یا ایجاد مشتری
            national_code = request.POST.get('national_code')
            customer, created = Customer.objects.get_or_create(
                national_code=national_code,
                defaults={
                    'full_name': request.POST.get('full_name'),
                    'phone_number': request.POST.get('phone_number'),
                    'email': request.POST.get('email', ''),
                }
            )

            # اگر مشتری از قبل وجود داشت، اطلاعاتش را آپدیت کن
            if not created:
                customer.full_name = request.POST.get('full_name')
                customer.phone_number = request.POST.get('phone_number')
                if request.POST.get('email'):
                    customer.email = request.POST.get('email')
                customer.save()

            # ایجاد رزرو
            reservation = Reservation(
                table_id=request.POST.get('table_id'),
                customer=customer,
                reservation_jalali_date=request.POST.get('reservation_date'),
                start_time=request.POST.get('start_time'),
                end_time=request.POST.get('end_time'),
                guest_count=int(request.POST.get('guest_count', 2)),
                special_requests=request.POST.get('special_requests', ''),
                reservation_status='confirmed'  # رزرو دستی مستقیم تأیید می‌شود
            )
            reservation.save()

            messages.success(request, f"رزرو با کد {reservation.reservation_code} با موفقیت ایجاد شد")
            return redirect('table:reservation_list')

        except Exception as e:
            messages.error(request, f"خطا در ایجاد رزرو: {str(e)}")

    # دریافت میزهای فعال
    tables = Table.objects.filter(restaurant=restaurant, is_active=True)

    # تاریخ پیش‌فرض (امروز)
    today_jalali = get_current_jalali_date().strftime('%Y/%m/%d')

    context = {
        'tables': tables,
        'today_jalali': today_jalali,
    }
    return render(request, 'table_app/reservation_form.html', context)

@login_required
@restaurant_owner_required
def reservation_confirm(request, reservation_id):
    """تأیید رزرو"""
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    if reservation.reservation_status == 'pending':
        reservation.confirm_reservation()
        messages.success(request, "رزرو با موفقیت تأیید شد")
    else:
        messages.warning(request, "این رزرو قبلاً تأیید شده است")

    return redirect('table:reservation_list')

@login_required
@restaurant_owner_required
def reservation_cancel(request, reservation_id):
    """لغو رزرو"""
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    if reservation.reservation_status in ['pending', 'confirmed']:
        reservation.cancel_reservation()
        messages.success(request, "رزرو با موفقیت لغو شد")
    else:
        messages.warning(request, "امکان لغو این رزرو وجود ندارد")

    return redirect('table:reservation_list')

@login_required
@restaurant_owner_required
def reservation_mark_seated(request, reservation_id):
    """علامت‌گذاری حضور مشتری"""
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    if reservation.reservation_status == 'confirmed':
        reservation.mark_customer_arrived()
        messages.success(request, "حضور مشتری ثبت شد")
    else:
        messages.warning(request, "امکان ثبت حضور برای این رزرو وجود ندارد")

    return redirect('table:reservation_list')

@login_required
@restaurant_owner_required
def reservation_mark_completed(request, reservation_id):
    """تکمیل رزرو"""
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    if reservation.reservation_status in ['confirmed', 'seated']:
        reservation.complete_reservation()
        messages.success(request, "رزرو به وضعیت تکمیل شده تغییر یافت")
    else:
        messages.warning(request, "امکان تکمیل این رزرو وجود ندارد")

    return redirect('table:reservation_list')


@login_required
@restaurant_owner_required
def reservation_mark_no_show(request, reservation_id):
    """ثبت عدم حضور مشتری"""
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    if reservation.reservation_status in ['confirmed', 'pending']:
        reservation.mark_no_show()
        messages.success(request, "عدم حضور مشتری ثبت شد")
    else:
        messages.warning(request, "امکان ثبت عدم حضور برای این رزرو وجود ندارد")

    return redirect('table:reservation_list')

# ----------------------------
# Working Time Management
# ----------------------------


@login_required
@restaurant_owner_required
def working_time_management(request):
    """مدیریت ساعات کاری"""
    restaurant = get_restaurant_for_user(request.user)

    if request.method == 'POST':
        try:
            # دریافت ساعات کاری
            opening_hour = int(request.POST.get('opening_hour', 9))
            opening_minute = int(request.POST.get('opening_minute', 0))
            closing_hour = int(request.POST.get('closing_hour', 23))
            closing_minute = int(request.POST.get('closing_minute', 0))

            opening_time = time(opening_hour, opening_minute)
            closing_time = time(closing_hour, closing_minute)

            # به‌روزرسانی ساعات کاری برای روزهای فعال
            active_days = request.POST.getlist('active_days')
            for day in WorkingDay.objects.all():
                working_time, created = WorkingTime.objects.get_or_create(
                    restaurant=restaurant,
                    day=day
                )
                working_time.is_active = str(day.id) in active_days
                if working_time.is_active:
                    working_time.start_time = opening_time
                    working_time.end_time = closing_time
                working_time.save()

            messages.success(request, "ساعات کاری با موفقیت ذخیره شد")
            return redirect('table:working_time_management')

        except Exception as e:
            messages.error(request, f"خطا در ذخیره ساعات کاری: {str(e)}")

    working_times = WorkingTime.objects.filter(restaurant=restaurant)
    settings = ReservationSettings.objects.filter(restaurant=restaurant).first()

    context = {
        'restaurant': restaurant,
        'days': WorkingDay.objects.all(),
        'working_times': working_times,
        'settings': settings,
    }
    return render(request, 'table_app/working_time_management.html', context)

# ----------------------------
# Settings
# ----------------------------

@login_required
@restaurant_owner_required
def reservation_settings(request):
    """تنظیمات رزرو"""
    restaurant = get_restaurant_for_user(request.user)
    settings, created = ReservationSettings.objects.get_or_create(restaurant=restaurant)

    if request.method == 'POST':
        try:
            settings.max_advance_days = int(request.POST.get('max_advance_days', 30))
            settings.min_advance_hours = int(request.POST.get('min_advance_hours', 2))
            settings.max_guests_per_reservation = int(request.POST.get('max_guests_per_reservation', 20))
            settings.default_reservation_duration = int(request.POST.get('default_reservation_duration', 120))
            settings.slot_duration = int(request.POST.get('slot_duration', 30))
            settings.auto_confirm_reservations = request.POST.get('auto_confirm_reservations') == 'on'
            settings.require_phone_verification = request.POST.get('require_phone_verification') == 'on'
            settings.max_reservations_per_time_slot = int(request.POST.get('max_reservations_per_time_slot', 1))
            settings.allow_same_day_reservations = request.POST.get('allow_same_day_reservations') == 'on'
            settings.friday_off = request.POST.get('friday_off') == 'on'
            settings.thursday_evening_off = request.POST.get('thursday_evening_off') == 'on'
            settings.special_holidays = request.POST.get('special_holidays', '')

            settings.save()
            messages.success(request, "تنظیمات با موفقیت ذخیره شد")
            return redirect('table:reservation_settings')
        except Exception as e:
            messages.error(request, f"خطا در ذخیره تنظیمات: {str(e)}")

    context = {
        'settings': settings,
    }
    return render(request, 'table_app/reservation_settings.html', context)

# ----------------------------
# AJAX Views
# ----------------------------

@login_required
@restaurant_owner_required
def get_table_availability_ajax(request, table_id):
    """دریافت وضعیت دسترسی میز برای تاریخ مشخص (AJAX)"""
    restaurant = get_restaurant_for_user(request.user)
    table = get_object_or_404(Table, id=table_id, restaurant=restaurant)

    jalali_date = request.GET.get('date')
    if not jalali_date:
        return JsonResponse({'error': 'تاریخ مشخص نشده'}, status=400)

    availability = table.get_jalali_availability(jalali_date)
    return JsonResponse(availability)

@login_required
@restaurant_owner_required
def get_daily_calendar_ajax(request):
    """دریافت تقویم روزانه برای تمام میزها (AJAX) - نسخه شمسی"""
    restaurant = get_restaurant_for_user(request.user)

    selected_date = request.GET.get('date')
    if not selected_date:
        return JsonResponse({'error': 'تاریخ مشخص نشده'}, status=400)

    try:
        # اعتبارسنجی تاریخ شمسی
        jalali_date_obj, is_valid = validate_jalali_date(selected_date)
        if not is_valid:
            return JsonResponse({'error': 'تاریخ شمسی نامعتبر'}, status=400)

        tables = Table.objects.filter(restaurant=restaurant, is_active=True)
        reservations = Reservation.objects.filter(
            table__restaurant=restaurant,
            reservation_jalali_date=selected_date
        ).select_related('table', 'customer')

        calendar_data = []
        for table in tables:
            table_reservations = [r for r in reservations if r.table_id == table.id]

            table_data = {
                'table_id': table.id,
                'table_number': table.table_number,
                'capacity': table.capacity,
                'table_type': table.get_table_type_display(),
                'table_type_class': table.table_type,
                'reservations': []
            }

            for reservation in table_reservations:
                table_data['reservations'].append({
                    'id': reservation.id,
                    'reservation_code': reservation.reservation_code,
                    'customer_name': reservation.customer.full_name,
                    'customer_phone': reservation.customer.phone_number,
                    'start_time': reservation.start_time.strftime('%H:%M'),
                    'end_time': reservation.end_time.strftime('%H:%M'),
                    'status': reservation.reservation_status,
                    'status_display': reservation.get_persian_status(),
                    'guest_count': reservation.guest_count,
                    'jalali_date': reservation.reservation_jalali_date,
                    'duration_minutes': reservation.duration_minutes,
                })

            calendar_data.append(table_data)

        return JsonResponse({
            'jalali_date': selected_date,
            'tables': calendar_data
        })

    except Exception as e:
        return JsonResponse({'error': f'خطا در پردازش: {str(e)}'}, status=400)

@login_required
@restaurant_owner_required
def get_available_tables_ajax(request):
    """دریافت میزهای آزاد برای تاریخ و زمان مشخص (AJAX)"""
    restaurant = get_restaurant_for_user(request.user)

    jalali_date = request.GET.get('date')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')
    guest_count = int(request.GET.get('guest_count', 2))

    if not all([jalali_date, start_time, end_time]):
        return JsonResponse({'error': 'پارامترهای لازم ارسال نشده'}, status=400)

    try:
        # تبدیل زمان‌ها
        start_time_obj = datetime.strptime(start_time, '%H:%M').time()
        end_time_obj = datetime.strptime(end_time, '%H:%M').time()

        # پیدا کردن میزهای آزاد
        available_tables = []
        tables = Table.objects.filter(
            restaurant=restaurant,
            is_active=True,
            capacity__gte=guest_count
        )

        for table in tables:
            if table.is_available(jalali_date, start_time_obj, end_time_obj):
                available_tables.append({
                    'id': table.id,
                    'table_number': table.table_number,
                    'capacity': table.capacity,
                    'table_type': table.get_table_type_display(),
                    'min_duration': table.min_reservation_duration,
                    'max_duration': table.max_reservation_duration,
                })

        return JsonResponse({
            'available_tables': available_tables,
            'count': len(available_tables)
        })

    except Exception as e:
        return JsonResponse({'error': f'خطا در پردازش: {str(e)}'}, status=400)


@login_required
@restaurant_owner_required
def get_table_reservations_ajax(request, table_id):
    """دریافت رزروهای یک میز برای تاریخ مشخص (AJAX)"""
    restaurant = get_restaurant_for_user(request.user)
    table = get_object_or_404(Table, id=table_id, restaurant=restaurant)

    selected_date = request.GET.get('date')
    if not selected_date:
        return JsonResponse({'error': 'تاریخ مشخص نشده'}, status=400)

    try:
        # اگر تاریخ میلادی است، تبدیل به شمسی کنیم
        if '-' in selected_date:
            # تاریخ میلادی - تبدیل به شمسی
            gregorian_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            jalali_date_obj = jdatetime.date.fromgregorian(date=gregorian_date)
            jalali_date = jalali_date_obj.strftime('%Y/%m/%d')
        else:
            # تاریخ شمسی
            jalali_date = selected_date
            jalali_date_obj, is_valid = validate_jalali_date(jalali_date)
            if not is_valid:
                return JsonResponse({'error': 'تاریخ شمسی نامعتبر'}, status=400)
            gregorian_date = jalali_date_obj.togregorian()

        # دریافت رزروها
        reservations = Reservation.objects.filter(
            table=table,
            reservation_jalali_date=jalali_date
        ).select_related('customer').order_by('start_time')

        reservations_data = []
        for reservation in reservations:
            reservations_data.append({
                'id': reservation.id,
                'reservation_code': reservation.reservation_code,
                'customer_name': reservation.customer.full_name,
                'customer_phone': reservation.customer.phone_number,
                'start_time': reservation.start_time.strftime('%H:%M'),
                'end_time': reservation.end_time.strftime('%H:%M'),
                'status': reservation.reservation_status,
                'status_display': reservation.get_persian_status(),
                'guest_count': reservation.guest_count,
                'duration_minutes': reservation.duration_minutes,
                'special_requests': reservation.special_requests or '',
            })

        return JsonResponse({
            'table_number': table.table_number,
            'table_capacity': table.capacity,
            'table_type': table.get_table_type_display(),
            'jalali_date': jalali_date,
            'gregorian_date': gregorian_date.strftime('%Y-%m-%d'),
            'reservations': reservations_data,
            'reservations_count': len(reservations_data)
        })

    except ValueError as e:
        return JsonResponse({'error': f'تاریخ نامعتبر: {str(e)}'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'خطا در پردازش: {str(e)}'}, status=400)






@login_required
@restaurant_owner_required
def customer_search(request):
    """صفحه جستجوی مشتری"""
    restaurant = get_restaurant_for_user(request.user)

    context = {
        'restaurant': restaurant,
        'today_jalali': jdatetime.date.today().strftime('%Y/%m/%d')
    }
    return render(request, 'table_app/customer_search.html', context)

from django.db.models import Q, Count, Case, When, IntegerField

@login_required
@restaurant_owner_required
def customer_search_api(request):

    print(f"Request method: {request.method}")
    print(f"POST data: {dict(request.POST)}")


    """API جستجوی مشتری بر اساس شماره موبایل"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'})

    phone_number = request.POST.get('phone_number', '').strip()

    if not phone_number:
        return JsonResponse({'success': False, 'error': 'شماره موبایل را وارد کنید'})

    try:
        restaurant = get_restaurant_for_user(request.user)

        # جستجوی مشتری - فقط مشتریانی که حداقل یک رزرو در این رستوران دارند
        customers = Customer.objects.filter(
            phone_number__icontains=phone_number,
            reservations__table__restaurant=restaurant
        ).distinct().annotate(
            total_reservations_count=Count('reservations'),
            successful_reservations_count=Count(
                Case(
                    When(reservations__reservation_status__in=['completed', 'seated'], then=1),
                    output_field=IntegerField()
                )
            ),
            last_reservation_date=Max('reservations__created_jalali')
        ).order_by('-created_jalali')[:10]

        customers_data = []
        for customer in customers:
            # محاسبه امتیاز مشتری
            score = calculate_customer_score(customer)

            # آخرین رزرو
            last_reservation = customer.reservations.filter(
                table__restaurant=restaurant
            ).order_by('-created_jalali').first()

            customers_data.append({
                'id': customer.id,
                'full_name': customer.full_name,
                'phone_number': customer.phone_number,
                'national_code': customer.national_code,
                'is_vip': customer.is_vip,
                'total_reservations': customer.total_reservations_count or 0,
                'successful_reservations': customer.successful_reservations_count or 0,
                'cancellation_count': customer.cancellation_count,
                'success_rate': customer.get_success_rate(),
                'customer_score': score,
                'score_label': get_score_label(score),
                'score_color': get_score_color(score),
                'last_reservation': {
                    'date': last_reservation.reservation_jalali_date if last_reservation else None,
                    'status': last_reservation.get_reservation_status_display() if last_reservation else None,
                    'table': last_reservation.table.table_number if last_reservation else None
                } if last_reservation else None,
                'created_jalali': customer.created_jalali,
                'is_active': customer.is_active
            })

        return JsonResponse({
            'success': True,
            'customers': customers_data,
            'count': len(customers_data)
        })

    except Exception as e:
        import traceback
        print(f"Error in customer_search_api: {str(e)}")
        print(traceback.format_exc())
        return JsonResponse({'success': False, 'error': 'خطای سرور: ' + str(e)})

@login_required
@restaurant_owner_required
def customer_detail_modal(request, customer_id):
    """نمایش جزئیات مشتری در مودال"""
    restaurant = get_restaurant_for_user(request.user)
    customer = get_object_or_404(Customer, id=customer_id)

    # تاریخچه رزروها
    reservations = customer.reservations.select_related('table').order_by('-reservation_jalali_date', '-start_time')

    # آمار پیشرفته
    total_reservations = reservations.count()
    successful_reservations = reservations.filter(
        reservation_status__in=['completed', 'seated']
    ).count()
    cancelled_reservations = reservations.filter(
        reservation_status='cancelled'
    ).count()
    no_show_reservations = reservations.filter(
        reservation_status='no_show'
    ).count()

    # محاسبه امتیاز
    score = calculate_customer_score(customer)

    # رزروهای آینده
    upcoming_reservations = reservations.filter(
        reservation_status__in=['pending', 'confirmed'],
        reservation_jalali_date__gte=jdatetime.date.today().strftime('%Y/%m/%d')
    )

    context = {
        'customer': customer,
        'reservations': reservations[:10],  # 10 رزرو آخر
        'total_reservations': total_reservations,
        'successful_reservations': successful_reservations,
        'cancelled_reservations': cancelled_reservations,
        'no_show_reservations': no_show_reservations,
        'customer_score': score,
        'score_label': get_score_label(score),
        'score_color': get_score_color(score),
        'upcoming_reservations': upcoming_reservations,
        'restaurant': restaurant
    }

    return render(request, 'table_app/partials/customer_detail_modal.html', context)

def calculate_customer_score(customer):
    """محاسبه امتیاز مشتری"""
    score = 50  # امتیاز پایه

    # امتیاز بر اساس تعداد رزروهای موفق
    if customer.successful_reservations > 10:
        score += 20
    elif customer.successful_reservations > 5:
        score += 10
    elif customer.successful_reservations > 2:
        score += 5

    # امتیاز منفی برای لغوها
    if customer.cancellation_count > 5:
        score -= 20
    elif customer.cancellation_count > 2:
        score -= 10
    elif customer.cancellation_count > 0:
        score -= 5

    # امتیاز VIP
    if customer.is_vip:
        score += 15

    # امتیاز بر اساس نرخ موفقیت
    success_rate = customer.get_success_rate()
    if success_rate > 80:
        score += 20
    elif success_rate > 60:
        score += 10
    elif success_rate < 30:
        score -= 10

    return max(0, min(100, score))  # محدود کردن بین 0 تا 100

def get_score_label(score):
    """برچسب امتیاز"""
    if score >= 80:
        return "مشتری عالی"
    elif score >= 60:
        return "مشتری خوب"
    elif score >= 40:
        return "مشتری متوسط"
    elif score >= 20:
        return "نیاز به توجه"
    else:
        return "مشتری مشکل‌دار"

def get_score_color(score):
    """رنگ امتیاز"""
    if score >= 80:
        return "success"
    elif score >= 60:
        return "info"
    elif score >= 40:
        return "warning"
    else:
        return "danger"