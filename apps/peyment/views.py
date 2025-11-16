# apps/peyment/views.py
from django.shortcuts import render, redirect
import requests
import json
from django.views import View
from django.contrib import messages
from apps.order.models import Ordermenu
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from apps.peyment.models import Peyment
from apps.user.models import CustomUser
import utils
from django.contrib.auth.decorators import login_required
from .zarinpal import ZarinPal
from django.http import JsonResponse

ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"

merchant = '41cb2cdd-3a44-4fb4-a0b3-db471b673078'

# ویوهای پرداخت یکپارچه
# apps/peyment/views.py
@login_required
def unified_send_request(request, payment_type, order_id):
    """ارسال درخواست پرداخت یکپارچه برای همه انواع سفارش"""
    if not utils.has_internet_connection():
        messages.error(request, 'اتصال اینترنت شما قابل تایید نیست', 'danger')
        return redirect('panel:panel')

    try:
        user = request.user
        amount = 0
        description = ""
        order_info = {}

        # تشخیص نوع سفارش و محاسبه مبلغ
        if payment_type == 'menu':
            order = Ordermenu.objects.get(id=order_id, restaurant__owner=user)
            amount = order.get_fixed_price()
            description = 'پرداخت هزینه ساخت منو دیجیتال'
            order_info = {'order': order}

        elif payment_type == 'plan':
            from apps.plan.models import PlanOrder
            order = PlanOrder.objects.get(id=order_id, user=user)
            amount = order.finalPrice * 10  # تبدیل به ریال
            description = f'پرداخت پلن {order.plan.name}'
            order_info = {'plan_order_id': order_id}

        elif payment_type == 'product':
            from apps.product.models import ProductOrder
            order = ProductOrder.objects.get(id=order_id, user=user)

            # ابتدا مطمئن شویم قیمت‌ها محاسبه شده‌اند
            order.calculate_prices()

            # کل مبلغ با مالیات ۹٪ به ریال
            amount = order.final_price * 10  # تبدیل به ریال

            description = f'پرداخت محصولات (شامل {order.tax_amount:,} تومان مالیات)'
            order_info = {'product_order_id': order_id}

        else:
            messages.error(request, 'نوع پرداخت نامعتبر است')
            return redirect('panel:panel')

        # ایجاد رکورد پرداخت
        peyment = Peyment.objects.create(
            customer=user,
            amount=amount,
            description=description,
            payment_type=payment_type,
            status='pending',
            **order_info
        )

        # ذخیره در session
        request.session['peyment_session'] = {
            'payment_type': payment_type,
            'order_id': order_id,
            'peyment_id': peyment.id,
        }
        request.session.modified = True

        # ارسال درخواست به درگاه پرداخت
        pay = ZarinPal(
            merchant=merchant,
            call_back_url="https://rank0.ir/peyment/verify/"
        )

        response = pay.send_request(
            amount=amount,
            description=description,
            email=user.email if user.email else "Example@test.com",
            mobile=user.mobileNumber
        )

        if response.get('error_code') is None:
            return response  # redirect به درگاه
        else:
            messages.error(request, f'خطا در اتصال به درگاه پرداخت: {response.get("message")}')
            return redirect('panel:panel')

    except ObjectDoesNotExist:
        messages.error(request, 'سفارش یافت نشد')
        return redirect('panel:panel')
    except Exception as e:
        messages.error(request, f'خطا در پردازش پرداخت: {str(e)}')
        return redirect('panel:panel')

# ویو قدیمی برای backward compatibility
@login_required
def send_request(request, order_id):
    """ویو قدیمی برای سازگاری با لینک‌های موجود"""
    return unified_send_request(request, 'menu', order_id)

class UnifiedVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']

        if 'peyment_session' not in request.session:
            messages.error(request, 'سشن پرداخت یافت نشد')
            return redirect('panel:panel')

        # دریافت اطلاعات از session
        payment_type = request.session['peyment_session']['payment_type']
        order_id = request.session['peyment_session']['order_id']
        peyment_id = request.session['peyment_session']['peyment_id']

        peyment = Peyment.objects.get(id=peyment_id)

        if t_status == 'OK':
            req_header = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            req_data = {
                "merchant_id": merchant,
                "amount": peyment.amount,
                "authority": t_authority
            }

            try:
                req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
                response_data = req.json()

                if len(response_data.get('errors', [])) == 0:
                    t_status_code = response_data['data']['code']

                    if t_status_code in [100, 101]:  # پرداخت موفق یا تکراری
                        # بروزرسانی وضعیت پرداخت
                        peyment.isFinaly = True
                        peyment.status = 'success'
                        peyment.statusCode = t_status_code
                        peyment.refId = str(response_data['data']['refId'])
                        peyment.save()

                        # بروزرسانی وضعیت سفارش مرتبط
                        self.update_related_order(payment_type, order_id, True)

                        # پاک کردن session
                        self.clear_session(request)

                        return redirect('peyment:show_success',
                                      f'پرداخت موفق - کد رهگیری: {peyment.refId}')

                    else:
                        # پرداخت ناموفق
                        peyment.status = 'failed'
                        peyment.statusCode = t_status_code
                        peyment.save()

                        self.update_related_order(payment_type, order_id, False)
                        return redirect('peyment:show_failed', 'پرداخت ناموفق بود')

                else:
                    e_code = response_data['errors']['code']
                    e_message = response_data['errors']['message']
                    return JsonResponse({
                        "status": 'error',
                        "message": e_message,
                        "error_code": e_code
                    })

            except Exception as e:
                messages.error(request, f'خطا در تأیید پرداخت: {str(e)}')
                return redirect('panel:panel')

        else:
            # پرداخت لغو شده توسط کاربر
            peyment.status = 'canceled'
            peyment.save()

            self.update_related_order(payment_type, order_id, False)
            return redirect('peyment:show_failed', 'پرداخت توسط کاربر لغو شد')

    def update_related_order(self, payment_type, order_id, is_success):
        """بروزرسانی وضعیت سفارش مرتبط"""
        try:
            if payment_type == 'menu':
                order = Ordermenu.objects.get(id=order_id)
                if is_success:
                    order.isfinaly = True
                    order.status = Ordermenu.STATUS_PAID
                    order.isActive = True
                else:
                    order.status = Ordermenu.STATUS_UNPAID
                order.save()

            elif payment_type == 'plan':
                from apps.plan.models import PlanOrder
                order = PlanOrder.objects.get(id=order_id)
                if is_success:
                    order.isPaid = True
                    order.paidAt = timezone.now()
                    # فعال‌سازی پلن
                    order.activate_plan()
                order.save()

            elif payment_type == 'product':
                from apps.product.models import ProductOrder
                order = ProductOrder.objects.get(id=order_id)
                if is_success:
                    order.status = 'paid'
                    order.isPaid = True
                    order.paidAt = timezone.now()
                else:
                    order.status = 'failed'
                order.save()

        except ObjectDoesNotExist as e:
            print(f"خطا در بروزرسانی سفارش: {e}")
        except Exception as e:
            print(f"خطای ناشناخته در بروزرسانی سفارش: {e}")

    def clear_session(self, request):
        """پاک کردن session"""
        if 'peyment_session' in request.session:
            del request.session['peyment_session']
        if 'pending_order' in request.session:
            del request.session['pending_order']

# ویو قدیمی برای backward compatibility
class Zarin_pal_view_verfiy(UnifiedVerifyView):
    """ویو قدیمی برای سازگاری با لینک‌های موجود"""
    pass

def show_success(request, message):
    """نمایش پیام موفقیت پرداخت"""
    return render(request, 'peyment_app/peyment.html', {
        'message': message,
        'title': 'پرداخت موفق'
    })

def show_failed(request, message):
    """نمایش پیام عدم موفقیت پرداخت"""
    return render(request, 'peyment_app/unpeyment.html', {
        'message': message,
        'title': 'پرداخت ناموفق'
    })

# ویوهای قدیمی برای backward compatibility
def show_verfiy_message(request, message):
    return show_success(request, message)

def show_verfiy_unmessage(request, message):
    return show_failed(request, message)