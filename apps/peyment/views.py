# apps/peyment/views.py
import logging
import json
import requests
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone
from apps.order.models import Ordermenu
from apps.peyment.models import Peyment
import utils

# تنظیم لاگر
logger = logging.getLogger(__name__)

# تنظیمات زرین‌پال
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
MERCHANT_ID = 'ba3b94c2-bc0b-457a-899d-a6e8cc22b027'
CALLBACK_URL = 'https://menubesaz.ir/peyment/verify/'

class ZarinPal:
    """کلاس مدیریت درگاه زرین‌پال"""

    def __init__(self, merchant, call_back_url):
        self.MERCHANT = merchant
        self.callbackURL = call_back_url

    def send_request(self, amount, description, email=None, mobile=None):
        """ارسال درخواست پرداخت جدید"""
        try:
            req_data = {
                "merchant_id": self.MERCHANT,
                "amount": amount,
                "callback_url": self.callbackURL,
                "description": description,
                "metadata": {"mobile": mobile, "email": email}
            }

            req_header = {
                "accept": "application/json",
                "content-type": "application/json"
            }

            logger.info(f"ارسال درخواست به زرین‌پال: {json.dumps(req_data, ensure_ascii=False)}")

            response = requests.post(
                url=ZP_API_REQUEST,
                data=json.dumps(req_data),
                headers=req_header,
                timeout=30
            )

            response_data = response.json()
            logger.info(f"پاسخ زرین‌پال: {json.dumps(response_data, ensure_ascii=False)}")

            if 'errors' in response_data and len(response_data['errors']) > 0:
                error_code = response_data['errors'].get('code', 'نامشخص')
                error_message = response_data['errors'].get('message', 'خطای نامشخص')
                logger.error(f"خطا از زرین‌پال: کد {error_code} - {error_message}")
                return {
                    "status": "error",
                    "error_code": error_code,
                    "message": error_message
                }

            if 'data' in response_data and 'authority' in response_data['data']:
                authority = response_data['data']['authority']
                payment_url = ZP_API_STARTPAY.format(authority=authority)
                logger.info(f"دریافت authority: {authority}")
                return redirect(payment_url)

            logger.error("فرمت پاسخ زرین‌پال نامعتبر است")
            return {
                "status": "error",
                "message": "فرمت پاسخ درگاه پرداخت نامعتبر است"
            }

        except requests.exceptions.Timeout:
            logger.error("اتصال به زرین‌پال timeout شد")
            return {
                "status": "error",
                "message": "اتصال به درگاه پرداخت timeout شد"
            }
        except requests.exceptions.ConnectionError:
            logger.error("اتصال به زرین‌پال برقرار نشد")
            return {
                "status": "error",
                "message": "اتصال به درگاه پرداخت برقرار نشد"
            }
        except Exception as e:
            logger.error(f"خطای ناشناخته در ارسال درخواست: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "message": f"خطای سیستمی: {str(e)}"
            }

@login_required
def unified_send_request(request, payment_type, order_id):
    """ارسال درخواست پرداخت یکپارچه"""
    logger.info(f"شروع پرداخت - نوع: {payment_type}, سفارش: {order_id}, کاربر: {request.user.id}")

    if not utils.has_internet_connection():
        messages.error(request, 'اتصال اینترنت شما قابل تایید نیست')
        logger.warning("کاربر بدون اینترنت سعی در پرداخت دارد")
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
            logger.info(f"پرداخت منو - مبلغ: {amount:,} ریال")

        elif payment_type == 'plan':
            from apps.plan.models import PlanOrder
            order = PlanOrder.objects.get(id=order_id, user=user)
            amount = order.finalPrice * 10  # تبدیل به ریال
            description = f'پرداخت پلن {order.plan.name}'
            order_info = {'plan_order_id': order_id}
            logger.info(f"پرداخت پلن - مبلغ: {amount:,} ریال")

        elif payment_type == 'product':
            from apps.product.models import ProductOrder
            order = ProductOrder.objects.get(id=order_id, user=user)
            order.calculate_prices()
            amount = order.final_price * 10  # تبدیل به ریال
            description = f'پرداخت محصولات (شامل {order.tax_amount:,} تومان مالیات)'
            order_info = {'product_order_id': order_id}
            logger.info(f"پرداخت محصول - مبلغ: {amount:,} ریال")

        else:
            logger.error(f"نوع پرداخت نامعتبر: {payment_type}")
            messages.error(request, 'نوع پرداخت نامعتبر است')
            return redirect('panel:panel')

        # بررسی مبلغ
        if amount <= 0:
            logger.error(f"مبلغ پرداخت نامعتبر: {amount}")
            messages.error(request, 'مبلغ پرداخت نامعتبر است')
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

        logger.info(f"رکورد پرداخت ایجاد شد - ID: {peyment.id}")

        # ذخیره در session
        request.session['peyment_session'] = {
            'payment_type': payment_type,
            'order_id': order_id,
            'peyment_id': peyment.id,
            'amount': amount
        }
        request.session.modified = True

        # ارسال درخواست به درگاه پرداخت
        pay = ZarinPal(
            merchant=MERCHANT_ID,
            call_back_url=CALLBACK_URL
        )

        response = pay.send_request(
            amount=amount,
            description=description,
            email=user.email if user.email else None,
            mobile=user.mobileNumber
        )

        if isinstance(response, dict) and response.get('status') == 'error':
            logger.error(f"خطا در ارتباط با درگاه: {response.get('message')}")
            messages.error(request, f'خطا در اتصال به درگاه پرداخت: {response.get("message")}')
            return redirect('panel:panel')

        return response

    except ObjectDoesNotExist:
        logger.error(f"سفارش یافت نشد - نوع: {payment_type}, ID: {order_id}")
        messages.error(request, 'سفارش یافت نشد')
        return redirect('panel:panel')
    except Exception as e:
        logger.error(f"خطای ناشناخته در پردازش پرداخت: {str(e)}", exc_info=True)
        messages.error(request, f'خطا در پردازش پرداخت: {str(e)}')
        return redirect('panel:panel')

@login_required
def send_request(request, order_id):
    """ویو قدیمی برای سازگاری با لینک‌های موجود"""
    return unified_send_request(request, 'menu', order_id)

class UnifiedVerifyView(LoginRequiredMixin, View):
    """تأیید پرداخت یکپارچه"""

    def get(self, request):
        logger.info(f"شروع تأیید پرداخت - کاربر: {request.user.id}")

        t_status = request.GET.get('Status', '')
        t_authority = request.GET.get('Authority', '')

        logger.info(f"پارامترهای بازگشت: Status={t_status}, Authority={t_authority}")

        if 'peyment_session' not in request.session:
            logger.error("سشن پرداخت یافت نشد")
            messages.error(request, 'سشن پرداخت یافت نشد')
            return redirect('panel:panel')

        try:
            # دریافت اطلاعات از session
            session_data = request.session['peyment_session']
            payment_type = session_data['payment_type']
            order_id = session_data['order_id']
            peyment_id = session_data['peyment_id']
            amount = session_data['amount']

            logger.info(f"داده‌های سشن - نوع: {payment_type}, سفارش: {order_id}, پرداخت: {peyment_id}")

            peyment = Peyment.objects.get(id=peyment_id)

            if t_status == 'OK':
                logger.info("کاربر از درگاه بازگشت موفقیت‌آمیز")
                return self.verify_payment(request, peyment, t_authority, amount, payment_type, order_id)
            else:
                logger.warning("کاربر پرداخت را لغو کرد")
                return self.handle_cancelled_payment(peyment, payment_type, order_id)

        except ObjectDoesNotExist:
            logger.error("رکورد پرداخت یافت نشد")
            messages.error(request, 'رکورد پرداخت یافت نشد')
            return redirect('panel:panel')
        except Exception as e:
            logger.error(f"خطای ناشناخته در تأیید پرداخت: {str(e)}", exc_info=True)
            messages.error(request, 'خطا در تأیید پرداخت')
            return redirect('panel:panel')

    def verify_payment(self, request, peyment, authority, amount, payment_type, order_id):
        """تأیید پرداخت با زرین‌پال"""
        try:
            req_header = {
                "accept": "application/json",
                "content-type": "application/json"
            }
            req_data = {
                "merchant_id": MERCHANT_ID,
                "amount": amount,
                "authority": authority
            }

            logger.info(f"ارسال درخواست تأیید به زرین‌پال: {json.dumps(req_data)}")

            response = requests.post(
                url=ZP_API_VERIFY,
                data=json.dumps(req_data),
                headers=req_header,
                timeout=30
            )

            response_data = response.json()
            logger.info(f"پاسخ تأیید زرین‌پال: {json.dumps(response_data, ensure_ascii=False)}")

            if 'errors' in response_data and len(response_data['errors']) > 0:
                error_code = response_data['errors'].get('code', 'نامشخص')
                error_message = response_data['errors'].get('message', 'خطای نامشخص')
                logger.error(f"خطا در تأیید: کد {error_code} - {error_message}")

                peyment.status = 'failed'
                peyment.statusCode = error_code
                peyment.save()

                self.update_related_order(payment_type, order_id, False)
                return redirect('peyment:show_failed', 'خطا در تأیید پرداخت')

            if 'data' in response_data:
                data = response_data['data']
                status_code = data.get('code')
                ref_id = data.get('ref_id')  # در زرین‌پال ref_id است

                logger.info(f"کد وضعیت: {status_code}, RefID: {ref_id}")

                if status_code in [100, 101]:  # پرداخت موفق یا تکراری
                    # بروزرسانی وضعیت پرداخت
                    peyment.isFinaly = True
                    peyment.status = 'success'
                    peyment.statusCode = status_code
                    peyment.refId = str(ref_id) if ref_id else None
                    peyment.save()

                    logger.info(f"پرداخت موفق - RefID: {ref_id}")

                    # بروزرسانی وضعیت سفارش مرتبط
                    self.update_related_order(payment_type, order_id, True)

                    # پاک کردن session
                    self.clear_session(request)

                 
                    if ref_id:
                        success_message += f'{ref_id}'

                    return redirect('peyment:show_success', success_message)
                else:
                    # پرداخت ناموفق
                    error_message = data.get('message', 'پرداخت ناموفق بود')
                    logger.warning(f"پرداخت ناموفق: {error_message}")

                    peyment.status = 'failed'
                    peyment.statusCode = status_code
                    peyment.save()

                    self.update_related_order(payment_type, order_id, False)
                    return redirect('peyment:show_failed', error_message)

            logger.error("پاسخ زرین‌پال بدون فیلد data")
            return redirect('peyment:show_failed', 'خطا در دریافت اطلاعات از درگاه')

        except requests.exceptions.Timeout:
            logger.error("تایم‌اوت در تأیید پرداخت")
            return redirect('peyment:show_failed', 'تایم‌اوت در تأیید پرداخت')
        except requests.exceptions.ConnectionError:
            logger.error("عدم اتصال در تأیید پرداخت")
            return redirect('peyment:show_failed', 'عدم اتصال به درگاه پرداخت')
        except Exception as e:
            logger.error(f"خطای ناشناخته در تأیید: {str(e)}", exc_info=True)
            return redirect('peyment:show_failed', f'خطا در تأیید پرداخت: {str(e)}')

    def handle_cancelled_payment(self, peyment, payment_type, order_id):
        """مدیریت پرداخت لغو شده"""
        peyment.status = 'canceled'
        peyment.save()

        logger.info("پرداخت توسط کاربر لغو شد")

        self.update_related_order(payment_type, order_id, False)
        return redirect('peyment:show_failed', 'پرداخت توسط کاربر لغو شد')

    def update_related_order(self, payment_type, order_id, is_success):
        """بروزرسانی وضعیت سفارش مرتبط"""
        try:
            logger.info(f"بروزرسانی سفارش - نوع: {payment_type}, ID: {order_id}, موفق: {is_success}")

            if payment_type == 'menu':
                order = Ordermenu.objects.get(id=order_id)
                if is_success:
                    order.isfinaly = True
                    order.status = Ordermenu.STATUS_PAID
                    order.isActive = True
                    logger.info(f"منو فعال شد - ID: {order_id}")
                else:
                    order.status = Ordermenu.STATUS_UNPAID
                order.save()

            elif payment_type == 'plan':
                from apps.plan.models import PlanOrder
                order = PlanOrder.objects.get(id=order_id)
                if is_success:
                    order.isPaid = True
                    order.paidAt = timezone.now()
                    order.activate_plan()
                    logger.info(f"پلن فعال شد - ID: {order_id}")
                order.save()

            elif payment_type == 'product':
                from apps.product.models import ProductOrder
                order = ProductOrder.objects.get(id=order_id)
                if is_success:
                    order.status = 'paid'
                    order.isPaid = True
                    order.paidAt = timezone.now()
                    logger.info(f"سفارش محصول پرداخت شد - ID: {order_id}")
                else:
                    order.status = 'failed'
                order.save()

            logger.info(f"بروزرسانی سفارش با موفقیت انجام شد")

        except ObjectDoesNotExist as e:
            logger.error(f"سفارش یافت نشد برای بروزرسانی: {str(e)}")
        except Exception as e:
            logger.error(f"خطا در بروزرسانی سفارش: {str(e)}", exc_info=True)

    def clear_session(self, request):
        """پاک کردن session"""
        try:
            if 'peyment_session' in request.session:
                del request.session['peyment_session']
                logger.info("سشن پرداخت پاک شد")
            if 'pending_order' in request.session:
                del request.session['pending_order']
        except Exception as e:
            logger.error(f"خطا در پاک کردن سشن: {str(e)}")

class Zarin_pal_view_verfiy(UnifiedVerifyView):
    """ویو قدیمی برای سازگاری با لینک‌های موجود"""
    pass

def show_success(request, message):
    """نمایش پیام موفقیت پرداخت"""
    logger.info(f"نمایش صفحه موفقیت: {message}")
    return render(request, 'peyment_app/peyment.html', {
        'message': message,
        'title': 'پرداخت موفق',
        'success': True
    })

def show_failed(request, message):
    """نمایش پیام عدم موفقیت پرداخت"""
    logger.info(f"نمایش صفحه ناموفق: {message}")
    return render(request, 'peyment_app/unpeyment.html', {
        'message': message,
        'title': 'پرداخت ناموفق',
        'success': False
    })

# ویوهای قدیمی برای backward compatibility
def show_verfiy_message(request, message):
    return show_success(request, message)

def show_verfiy_unmessage(request, message):
    return show_failed(request, message)