from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime, time
import jdatetime
from .models import Restaurant, Table, Reservation, Customer, ReservationSettings, WorkingTime

def check_availability_ajax(request, restaurant_slug):
    """بررسی دسترسی میزها (AJAX) - نسخه نهایی"""
    print(f"🔍 درخواست بررسی دسترسی برای رستوران: {restaurant_slug}")
    print(f"📅 پارامترها: date={request.GET.get('date')}, guest_count={request.GET.get('guest_count')}")

    try:
        # پیدا کردن رستوران
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug, isActive=True)
        print(f"✅ رستوران پیدا شد: {restaurant.title}")

        jalali_date = request.GET.get('date')
        guest_count = request.GET.get('guest_count', 2)

        if not jalali_date:
            print("❌ تاریخ مشخص نشده")
            return JsonResponse({'error': 'تاریخ مشخص نشده'}, status=400)

        # اعتبارسنجی تاریخ
        try:
            year, month, day = map(int, jalali_date.split('/'))
            jalali_date_obj = jdatetime.date(year, month, day)
            print(f"✅ تاریخ معتبر در ویو: {jalali_date_obj}")
        except (ValueError, Exception):
            print("❌ تاریخ نامعتبر در ویو")
            return JsonResponse({'error': 'تاریخ نامعتبر است. فرمت صحیح: 1403/01/01'}, status=400)

        guest_count = int(guest_count)
        print(f"✅ تاریخ: {jalali_date}, مهمانان: {guest_count}")

        # بررسی تعطیلی
        settings = ReservationSettings.objects.filter(restaurant=restaurant).first()
        if settings and settings.is_holiday(jalali_date):
            print(f"❌ رستوران در این تاریخ تعطیل است")
            return JsonResponse({
                'available': False,
                'message': 'رستوران در این تاریخ تعطیل است'
            })

        # بررسی روز کاری
        weekday_map = {
            0: 'saturday', 1: 'sunday', 2: 'monday', 3: 'tuesday',
            4: 'wednesday', 5: 'thursday', 6: 'friday'
        }

        day_name = weekday_map[jalali_date_obj.weekday()]
        print(f"📅 روز هفته در ویو: {day_name}")

        working_time = WorkingTime.objects.filter(
            restaurant=restaurant,
            day__name=day_name,
            is_active=True
        ).first()

        if not working_time:
            print(f"❌ رستوران در این روز کاری نیست")
            return JsonResponse({
                'available': False,
                'message': 'رستوران در این روز تعطیل است'
            })

        print(f"✅ رستوران در این روز کاری است")
        print(f"🕒 ساعات کاری: {working_time.start_time} تا {working_time.end_time}")

        # پیدا کردن میزهای مناسب
        tables = Table.objects.filter(
            restaurant=restaurant,
            is_active=True,
            capacity__gte=guest_count
        )

        print(f"🔍 تعداد میزهای پیدا شده: {tables.count()}")

        available_tables = []
        for table in tables:
            print(f"\n🔍 بررسی میز: {table.table_number} (ظرفیت: {table.capacity})")

            # بررسی دسترسی میز
            availability = table.get_jalali_availability(jalali_date)

            if availability['available'] and availability['slots']:
                available_tables.append({
                    'id': table.id,
                    'table_number': table.table_number,
                    'capacity': table.capacity,
                    'table_type': table.get_table_type_display(),
                    'available_slots': availability['slots'][:20],
                    'working_hours': availability['working_hours']
                })
                print(f"✅ میز {table.table_number} قابل رزرو است")
            else:
                print(f"❌ میز {table.table_number} قابل رزرو نیست - دلیل: {availability.get('reason', 'نامشخص')}")

        print(f"\n🎯 تعداد میزهای قابل رزرو: {len(available_tables)}")

        return JsonResponse({
            'available': len(available_tables) > 0,
            'tables': available_tables,
            'jalali_date': jalali_date,
            'guest_count': guest_count
        })

    except Exception as e:
        print(f"❌ خطا در پردازش: {str(e)}")
        import traceback
        print(traceback.format_exc())
        return JsonResponse({'error': f'خطا در پردازش: {str(e)}'}, status=400)

# بقیه توابع بدون تغییر...
def create_reservation_ajax(request, restaurant_slug):
    """ایجاد رزرو جدید (AJAX)"""
    print(f"🔍 درخواست ایجاد رزرو برای رستوران: {restaurant_slug}")

    try:
        restaurant = get_object_or_404(Restaurant, slug=restaurant_slug, isActive=True)
        print(f"✅ رستوران پیدا شد: {restaurant.title}")
    except:
        return JsonResponse({'success': False, 'message': 'رستوران یافت نشد'})

    if request.method == 'POST':
        try:
            # دریافت داده‌ها
            table_id = request.POST.get('table_id')
            jalali_date = request.POST.get('reservation_date')
            start_time_str = request.POST.get('start_time')  # تغییر نام متغیر
            end_time_str = request.POST.get('end_time')      # تغییر نام متغیر
            guest_count = request.POST.get('guest_count')
            full_name = request.POST.get('full_name')
            phone_number = request.POST.get('phone_number')
            national_code = request.POST.get('national_code')
            special_requests = request.POST.get('special_requests', '')

            print(f"📦 داده‌های دریافتی: table_id={table_id}, date={jalali_date}, time={start_time_str}-{end_time_str}, guests={guest_count}")

            # اعتبارسنجی داده‌ها
            if not all([table_id, jalali_date, start_time_str, end_time_str, guest_count, full_name, phone_number]):
                return JsonResponse({'success': False, 'message': 'لطفا تمام فیلدهای ضروری را پر کنید'})

            # تبدیل زمان‌ها - مدیریت فرمت‌های مختلف
            def parse_time(time_str):
                """تبدیل رشته زمان به time object"""
                time_str = time_str.strip()
                # اگر فرمت HH:MM است، تبدیل به HH:MM:00
                if len(time_str) == 5 and ':' in time_str:
                    time_str += ':00'
                try:
                    return datetime.strptime(time_str, '%H:%M:%S').time()
                except ValueError:
                    # اگر باز هم خطا داد، سعی کن با فرمت HH:MM
                    try:
                        return datetime.strptime(time_str, '%H:%M').time()
                    except ValueError as e:
                        raise ValueError(f"فرمت زمان نامعتبر: {time_str}") from e

            start_time_obj = parse_time(start_time_str)
            end_time_obj = parse_time(end_time_str)

            print(f"✅ زمان‌های تبدیل شده: start={start_time_obj}, end={end_time_obj}")

            # پیدا کردن یا ایجاد مشتری
            customer_identifier = national_code or phone_number
            customer, created = Customer.objects.get_or_create(
                national_code=customer_identifier,
                defaults={
                    'full_name': full_name,
                    'phone_number': phone_number,
                }
            )

            # اگر مشتری از قبل وجود داشت، اطلاعاتش را آپدیت کن
            if not created:
                customer.full_name = full_name
                customer.phone_number = phone_number
                customer.save()

            print(f"✅ مشتری پیدا/ایجاد شد: {customer.full_name}")

            # پیدا کردن میز
            table = Table.objects.get(id=table_id, restaurant=restaurant, is_active=True)
            print(f"✅ میز پیدا شد: {table.table_number}")

            # بررسی دسترسی میز
            if not table.is_available(jalali_date, start_time_obj, end_time_obj):
                return JsonResponse({
                    'success': False,
                    'message': 'متأسفانه میز در این بازه زمانی رزرو شده است'
                })

            # بررسی ظرفیت
            if table.capacity < int(guest_count):
                return JsonResponse({
                    'success': False,
                    'message': f'ظرفیت میز ({table.capacity} نفر) کمتر از تعداد مهمان است'
                })

            # ایجاد رزرو
            reservation = Reservation(
                table=table,
                customer=customer,
                reservation_jalali_date=jalali_date,
                start_time=start_time_obj,
                end_time=end_time_obj,
                guest_count=int(guest_count),
                special_requests=special_requests,
                reservation_status='pending'
            )
            reservation.save()

            print(f"✅ رزرو ایجاد شد: {reservation.reservation_code}")

            return JsonResponse({
                'success': True,
                'message': 'رزرو با موفقیت ثبت شد',
                'reservation_code': reservation.reservation_code,
                'confirmation_code': reservation.confirmation_code
            })

        except Table.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'میز مورد نظر یافت نشد'})
        except ValueError as e:
            print(f"❌ خطا در فرمت زمان: {str(e)}")
            return JsonResponse({'success': False, 'message': f'خطا در فرمت زمان: {str(e)}'})
        except Exception as e:
            print(f"❌ خطا در ایجاد رزرو: {str(e)}")
            import traceback
            print(traceback.format_exc())
            return JsonResponse({'success': False, 'message': f'خطا در ثبت رزرو: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'متد غیرمجاز'})

def verify_reservation_ajax(request, reservation_code):
    """تأیید رزرو با کد (AJAX)"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            confirmation_code = data.get('confirmation_code')

            reservation = Reservation.objects.get(reservation_code=reservation_code)

            if reservation.verify_confirmation_code(confirmation_code):
                reservation.confirm_reservation()
                return JsonResponse({
                    'success': True,
                    'message': 'رزرو با موفقیت تأیید شد',
                    'status': reservation.get_persian_status()
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'کد تأیید نامعتبر است'
                })

        except Reservation.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'رزرو یافت نشد'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'خطا در تأیید رزرو: {str(e)}'})

    return JsonResponse({'success': False, 'message': 'متد غیرمجاز'})

def reservation_status_ajax(request, reservation_code):
    """بررسی وضعیت رزرو (AJAX)"""
    try:
        reservation = Reservation.objects.get(reservation_code=reservation_code)

        return JsonResponse({
            'success': True,
            'reservation': {
                'code': reservation.reservation_code,
                'customer_name': reservation.customer.full_name,
                'table_number': reservation.table.table_number,
                'date': reservation.reservation_jalali_date,
                'start_time': reservation.start_time.strftime('%H:%M'),
                'end_time': reservation.end_time.strftime('%H:%M'),
                'guest_count': reservation.guest_count,
                'status': reservation.get_persian_status(),
                'is_confirmed': reservation.is_confirmed
            }
        })

    except Reservation.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'رزرو یافت نشد'})