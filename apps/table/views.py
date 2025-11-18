# table_app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Q, Count
from datetime import datetime, date, timedelta
import json
from .models import Restaurant, Table, Reservation, WorkingTime, WorkingDay, ReservationSettings

# ----------------------------
# Decorators
# ----------------------------

def restaurant_owner_required(view_func):
    """
    دکوراتور برای بررسی مالک رستوران
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        # اگر کاربر مالک رستوران نباشد
        if not request.user.restaurants.exists():
            messages.error(request, "شما دسترسی به این بخش را ندارید")
            return redirect('dashboard')

        return view_func(request, *args, **kwargs)
    return wrapper

def get_restaurant_for_user(user):
    """
    دریافت رستوران کاربر
    """
    return user.restaurants.first()

# ----------------------------
# Dashboard & Overview
# ----------------------------

@login_required
@restaurant_owner_required
def reservation_dashboard(request):
    """
    داشبورد مدیریت رزروها
    """
    restaurant = get_restaurant_for_user(request.user)
    today = date.today()

    # آمار کلی
    total_tables = Table.objects.filter(restaurant=restaurant).count()
    active_tables = Table.objects.filter(restaurant=restaurant, is_active=True).count()

    # رزروهای امروز
    today_reservations = Reservation.objects.filter(
        table__restaurant=restaurant,
        reservation_date=today
    )

    today_stats = {
        'total': today_reservations.count(),
        'confirmed': today_reservations.filter(reservation_status='confirmed').count(),
        'seated': today_reservations.filter(reservation_status='seated').count(),
        'completed': today_reservations.filter(reservation_status='completed').count(),
        'cancelled': today_reservations.filter(reservation_status='cancelled').count(),
    }

    # رزروهای فردا
    tomorrow = today + timedelta(days=1)
    tomorrow_reservations = Reservation.objects.filter(
        table__restaurant=restaurant,
        reservation_date=tomorrow,
        reservation_status__in=['confirmed', 'pending']
    ).count()

    # رزروهای آینده (7 روز آینده)
    next_week = today + timedelta(days=7)
    upcoming_reservations = Reservation.objects.filter(
        table__restaurant=restaurant,
        reservation_date__range=[today, next_week],
        reservation_status__in=['confirmed', 'pending']
    ).count()

    context = {
        'restaurant': restaurant,
        'total_tables': total_tables,
        'active_tables': active_tables,
        'today_stats': today_stats,
        'tomorrow_reservations': tomorrow_reservations,
        'upcoming_reservations': upcoming_reservations,
        'today': today,
    }

    return render(request, 'table_app/dashboard.html', context)

# ----------------------------
# Table Management
# ----------------------------

@login_required
@restaurant_owner_required
def table_list(request):
    """
    لیست میزهای رستوران
    """
    restaurant = get_restaurant_for_user(request.user)
    tables = Table.objects.filter(restaurant=restaurant).order_by('table_number')

    # فیلترها
    table_type = request.GET.get('table_type')
    is_active = request.GET.get('is_active')

    if table_type:
        tables = tables.filter(table_type=table_type)
    if is_active is not None:
        tables = tables.filter(is_active=(is_active == 'true'))

    context = {
        'tables': tables,
        'table_types': Table.TABLE_TYPES,
    }

    return render(request, 'table_app/table_list.html', context)

@login_required
@restaurant_owner_required
def table_detail(request, table_id):
    """
    جزئیات میز و رزروهای آن
    """
    restaurant = get_restaurant_for_user(request.user)
    table = get_object_or_404(Table, id=table_id, restaurant=restaurant)

    # رزروهای این میز
    reservations = Reservation.objects.filter(table=table).order_by('-reservation_date', '-start_time')

    # فیلتر بر اساس تاریخ
    date_filter = request.GET.get('date')
    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            reservations = reservations.filter(reservation_date=filter_date)
        except ValueError:
            messages.error(request, "تاریخ نامعتبر است")

    context = {
        'table': table,
        'reservations': reservations,
        'today': date.today(),
    }

    return render(request, 'table_app/table_detail.html', context)

@login_required
@restaurant_owner_required
def table_create(request):
    """
    ایجاد میز جدید
    """
    restaurant = get_restaurant_for_user(request.user)

    if request.method == 'POST':
        try:
            table = Table(
                restaurant=restaurant,
                table_number=request.POST.get('table_number'),
                table_type=request.POST.get('table_type'),
                capacity=request.POST.get('capacity'),
                description=request.POST.get('description'),
                min_reservation_duration=request.POST.get('min_reservation_duration', 60),
                is_active=request.POST.get('is_active') == 'on'
            )
            table.save()

            messages.success(request, "میز با موفقیت ایجاد شد")
            return redirect('table:table_list')

        except Exception as e:
            messages.error(request, f"خطا در ایجاد میز: {str(e)}")

    context = {
        'table_types': Table.TABLE_TYPES,
    }

    return render(request, 'table_app/table_form.html', context)

@login_required
@restaurant_owner_required
def table_edit(request, table_id):
    """
    ویرایش میز
    """
    restaurant = get_restaurant_for_user(request.user)
    table = get_object_or_404(Table, id=table_id, restaurant=restaurant)

    if request.method == 'POST':
        try:
            table.table_number = request.POST.get('table_number')
            table.table_type = request.POST.get('table_type')
            table.capacity = request.POST.get('capacity')
            table.description = request.POST.get('description')
            table.min_reservation_duration = request.POST.get('min_reservation_duration', 60)
            table.is_active = request.POST.get('is_active') == 'on'
            table.save()

            messages.success(request, "میز با موفقیت ویرایش شد")
            return redirect('table:table_list')

        except Exception as e:
            messages.error(request, f"خطا در ویرایش میز: {str(e)}")

    context = {
        'table': table,
        'table_types': Table.TABLE_TYPES,
    }

    return render(request, 'table_app/table_form.html', context)

@login_required
@restaurant_owner_required
def table_delete(request, table_id):
    """
    حذف میز
    """
    restaurant = get_restaurant_for_user(request.user)
    table = get_object_or_404(Table, id=table_id, restaurant=restaurant)

    # بررسی وجود رزروهای فعال
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
# Reservation Management
# ----------------------------

@login_required
@restaurant_owner_required
def reservation_list(request):
    """
    لیست تمام رزروها با فیلترهای پیشرفته
    """
    restaurant = get_restaurant_for_user(request.user)
    reservations = Reservation.objects.filter(table__restaurant=restaurant).order_by('-reservation_date', '-start_time')

    # فیلترها
    date_filter = request.GET.get('date')
    status_filter = request.GET.get('status')
    table_filter = request.GET.get('table')
    customer_name_filter = request.GET.get('customer_name')

    if date_filter:
        try:
            filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            reservations = reservations.filter(reservation_date=filter_date)
        except ValueError:
            messages.error(request, "تاریخ نامعتبر است")

    if status_filter:
        reservations = reservations.filter(reservation_status=status_filter)

    if table_filter:
        reservations = reservations.filter(table__table_number__icontains=table_filter)

    if customer_name_filter:
        reservations = reservations.filter(customer_full_name__icontains=customer_name_filter)

    context = {
        'reservations': reservations,
        'status_choices': Reservation.RESERVATION_STATUS,
        'tables': Table.objects.filter(restaurant=restaurant),
        'today': date.today(),
    }

    return render(request, 'table_app/reservation_list.html', context)

@login_required
@restaurant_owner_required
def reservation_detail(request, reservation_id):
    """
    جزئیات رزرو
    """
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
def reservation_confirm(request, reservation_id):
    """
    تأیید رزرو توسط رستوران
    """
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    if reservation.reservation_status == 'pending':
        reservation.reservation_status = 'confirmed'
        reservation.is_confirmed = True
        reservation.save()

        messages.success(request, "رزرو با موفقیت تأیید شد")
    else:
        messages.warning(request, "این رزرو قبلاً تأیید شده است")

    return redirect('table:reservation_list')

@login_required
@restaurant_owner_required
def reservation_cancel(request, reservation_id):
    """
    لغو رزرو توسط رستوران
    """
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    if reservation.reservation_status in ['pending', 'confirmed']:
        reservation.reservation_status = 'cancelled'
        reservation.save()

        messages.success(request, "رزرو با موفقیت لغو شد")
    else:
        messages.warning(request, "امکان لغو این رزرو وجود ندارد")

    return redirect('table:reservation_list')

@login_required
@restaurant_owner_required
def reservation_mark_seated(request, reservation_id):
    """
    علامت‌گذاری حضور مشتری
    """
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    if reservation.reservation_status == 'confirmed':
        reservation.reservation_status = 'seated'
        reservation.customer_arrived = True
        reservation.arrival_time = timezone.now()
        reservation.save()

        messages.success(request, "حضور مشتری ثبت شد")
    else:
        messages.warning(request, "امکان ثبت حضور برای این رزرو وجود ندارد")

    return redirect('table:reservation_list')

@login_required
@restaurant_owner_required
def reservation_mark_completed(request, reservation_id):
    """
    تکمیل رزرو
    """
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    if reservation.reservation_status in ['confirmed', 'seated']:
        reservation.reservation_status = 'completed'
        reservation.save()

        messages.success(request, "رزرو به وضعیت تکمیل شده تغییر یافت")
    else:
        messages.warning(request, "امکان تکمیل این رزرو وجود ندارد")

    return redirect('table:reservation_list')

@login_required
@restaurant_owner_required
def reservation_mark_no_show(request, reservation_id):
    """
    علامت‌گذاری عدم حضور مشتری
    """
    restaurant = get_restaurant_for_user(request.user)
    reservation = get_object_or_404(
        Reservation,
        id=reservation_id,
        table__restaurant=restaurant
    )

    if reservation.reservation_status in ['confirmed', 'pending']:
        reservation.reservation_status = 'no_show'
        reservation.save()

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
    """
    مدیریت ساعات کاری رستوران
    """
    restaurant = get_restaurant_for_user(request.user)

    if request.method == 'POST':
        try:
            # ذخیره ساعت شروع و پایان در مدل رستوران
            opening_time = request.POST.get('opening_time')
            closing_time = request.POST.get('closing_time')
            slot_duration = request.POST.get('slot_duration')

            if opening_time:
                restaurant.openingTime = opening_time
            if closing_time:
                restaurant.closingTime = closing_time
            restaurant.save()

            # ذخیره مدت زمان در تنظیمات
            settings, created = ReservationSettings.objects.get_or_create(restaurant=restaurant)
            if slot_duration:
                settings.slot_duration = int(slot_duration)
            settings.save()

            # ذخیره روزهای فعال
            active_days = request.POST.getlist('active_days')
            for day in WorkingDay.objects.all():
                working_time, created = WorkingTime.objects.get_or_create(
                    restaurant=restaurant,
                    day=day
                )
                working_time.is_active = str(day.id) in active_days
                working_time.save()

            messages.success(request, "ساعات کاری با موفقیت ذخیره شد")
            return redirect('table:working_time_management')

        except Exception as e:
            messages.error(request, f"خطا در ذخیره ساعات کاری: {str(e)}")

    # دریافت ساعات کاری فعلی
    working_times = WorkingTime.objects.filter(restaurant=restaurant)

    context = {
        'restaurant': restaurant,
        'days': WorkingDay.objects.all(),
        'working_times': working_times,
        'settings': ReservationSettings.objects.filter(restaurant=restaurant).first(),
    }

    return render(request, 'table_app/working_time_management.html', context)
# ----------------------------
# Settings
# ----------------------------

@login_required
@restaurant_owner_required
def reservation_settings(request):
    """
    تنظیمات رزرو رستوران
    """
    restaurant = get_restaurant_for_user(request.user)

    # ایجاد تنظیمات پیش‌فرض اگر وجود نداشته باشد
    settings, created = ReservationSettings.objects.get_or_create(restaurant=restaurant)

    if request.method == 'POST':
        try:
            settings.max_advance_days = request.POST.get('max_advance_days', 30)
            settings.min_advance_hours = request.POST.get('min_advance_hours', 2)
            settings.max_guests_per_reservation = request.POST.get('max_guests_per_reservation', 20)
            settings.default_reservation_duration = request.POST.get('default_reservation_duration', 120)
            settings.slot_duration = request.POST.get('slot_duration', 30)
            settings.auto_confirm_reservations = request.POST.get('auto_confirm_reservations') == 'on'
            settings.require_phone_verification = request.POST.get('require_phone_verification') == 'on'
            settings.max_reservations_per_time_slot = request.POST.get('max_reservations_per_time_slot', 1)
            settings.allow_same_day_reservations = request.POST.get('allow_same_day_reservations') == 'on'

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
def get_table_reservations_ajax(request, table_id):
    """
    دریافت رزروهای یک میز برای تاریخ مشخص (AJAX)
    """
    restaurant = get_restaurant_for_user(request.user)
    table = get_object_or_404(Table, id=table_id, restaurant=restaurant)

    selected_date = request.GET.get('date')
    if not selected_date:
        return JsonResponse({'error': 'تاریخ مشخص نشده'}, status=400)

    try:
        filter_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'تاریخ نامعتبر'}, status=400)

    reservations = Reservation.objects.filter(
        table=table,
        reservation_date=filter_date
    ).order_by('start_time')

    reservations_data = []
    for reservation in reservations:
        reservations_data.append({
            'id': reservation.id,
            'reservation_code': reservation.reservation_code,
            'customer_name': reservation.customer_full_name,
            'start_time': reservation.start_time.strftime('%H:%M'),
            'end_time': reservation.end_time.strftime('%H:%M'),
            'status': reservation.reservation_status,
            'status_display': reservation.get_reservation_status_display(),
            'guest_count': reservation.guest_count,
        })

    return JsonResponse({
        'table_number': table.table_number,
        'date': selected_date,
        'reservations': reservations_data
    })

@login_required
@restaurant_owner_required
def get_daily_calendar_ajax(request):
    """
    دریافت تقویم روزانه برای تمام میزها (AJAX)
    """
    restaurant = get_restaurant_for_user(request.user)

    selected_date = request.GET.get('date')
    if not selected_date:
        return JsonResponse({'error': 'تاریخ مشخص نشده'}, status=400)

    try:
        filter_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'تاریخ نامعتبر'}, status=400)

    tables = Table.objects.filter(restaurant=restaurant, is_active=True)
    reservations = Reservation.objects.filter(
        table__restaurant=restaurant,
        reservation_date=filter_date
    ).select_related('table')

    calendar_data = []
    for table in tables:
        table_reservations = [r for r in reservations if r.table_id == table.id]

        table_data = {
            'table_id': table.id,
            'table_number': table.table_number,
            'capacity': table.capacity,
            'table_type': table.get_table_type_display(),
            'reservations': []
        }

        for reservation in table_reservations:
            table_data['reservations'].append({
                'id': reservation.id,
                'reservation_code': reservation.reservation_code,
                'customer_name': reservation.customer_full_name,
                'start_time': reservation.start_time.strftime('%H:%M'),
                'end_time': reservation.end_time.strftime('%H:%M'),
                'status': reservation.reservation_status,
                'status_display': reservation.get_reservation_status_display(),
                'guest_count': reservation.guest_count,
            })

        calendar_data.append(table_data)

    return JsonResponse({
        'date': selected_date,
        'tables': calendar_data
    })
