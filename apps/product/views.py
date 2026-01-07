# views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import Product, ProductOrder, ProductOrderDetail
from apps.plan.models import Plan
from django.contrib.auth.decorators import login_required
from apps.user.model.user import CustomUser
from django.contrib import messages


def get_or_create_cart(request):
    """دریافت یا ایجاد سبد خرید برای کاربر"""
    if request.user.is_authenticated:
        user = request.user
        # جستجوی سبد خرید فعال (draft) برای کاربر
        cart = ProductOrder.objects.filter(
            user=user,
            status='draft'
        ).first()

        if not cart:
            # اگر سبد خرید وجود ندارد، یک پلن پیش‌فرض ایجاد کنید
            default_plan = Plan.objects.filter(isActive=True).first()
            if default_plan:
                cart = ProductOrder.objects.create(
                    user=user,
                    plan=default_plan,
                    status='draft'
                )

        return cart
    return None

@csrf_exempt
@require_http_methods(["POST"])
def add_to_cart(request):
    """افزودن محصول به سبد خرید"""
    try:
        # خواندن داده‌های JSON
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Content-Type باید application/json باشد'
            }, status=400)

        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))

        if not product_id:
            return JsonResponse({
                'success': False,
                'message': 'شناسه محصول الزامی است'
            }, status=400)

        # بررسی وجود محصول
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'محصول یافت نشد'
            }, status=404)

        # بررسی احراز هویت کاربر
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'لطفاً ابتدا وارد حساب کاربری خود شوید'
            }, status=401)

        # دریافت یا ایجاد سبد خرید
        cart = get_or_create_cart(request)
        if not cart:
            return JsonResponse({
                'success': False,
                'message': 'سبد خرید ایجاد نشد'
            }, status=500)

        # افزودن محصول به سبد
        cart.add_product(product, quantity)

        return JsonResponse({
            'success': True,
            'message': 'محصول به سبد خرید اضافه شد',
            'cart_total': cart.final_price,
            'items_count': cart.items_count,
            'product_name': product.name
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'داده‌های JSON نامعتبر است'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در افزودن به سبد خرید: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def update_cart_item(request):
    """بروزرسانی تعداد محصول در سبد خرید"""
    try:
        # خواندن داده‌های JSON
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Content-Type باید application/json باشد'
            }, status=400)

        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))

        if not product_id:
            return JsonResponse({
                'success': False,
                'message': 'شناسه محصول الزامی است'
            }, status=400)

        # بررسی وجود محصول
        try:
            product = Product.objects.get(id=product_id, is_active=True)
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'محصول یافت نشد'
            }, status=404)

        # بررسی احراز هویت کاربر
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'لطفاً ابتدا وارد حساب کاربری خود شوید'
            }, status=401)

        # دریافت سبد خرید
        cart = get_or_create_cart(request)
        if not cart:
            return JsonResponse({
                'success': False,
                'message': 'سبد خرید یافت نشد'
            }, status=404)

        # بروزرسانی تعداد
        success = cart.update_quantity(product, quantity)

        if success:
            # محاسبه قیمت آیتم
            try:
                item = cart.items.get(product=product)
                item_total = float(item.total_price)
            except ProductOrderDetail.DoesNotExist:
                item_total = 0

            return JsonResponse({
                'success': True,
                'message': 'تعداد محصول بروزرسانی شد',
                'cart_total': cart.final_price,
                'items_count': cart.items_count,
                'item_total': item_total
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'محصول در سبد خرید یافت نشد'
            }, status=404)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'داده‌های JSON نامعتبر است'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در بروزرسانی سبد خرید: {str(e)}'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def remove_from_cart(request):
    """حذف محصول از سبد خرید"""
    try:
        # خواندن داده‌های JSON
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            return JsonResponse({
                'success': False,
                'message': 'Content-Type باید application/json باشد'
            }, status=400)

        product_id = data.get('product_id')

        if not product_id:
            return JsonResponse({
                'success': False,
                'message': 'شناسه محصول الزامی است'
            }, status=400)

        # بررسی وجود محصول
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'محصول یافت نشد'
            }, status=404)

        # بررسی احراز هویت کاربر
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'لطفاً ابتدا وارد حساب کاربری خود شوید'
            }, status=401)

        # دریافت سبد خرید
        cart = get_or_create_cart(request)
        if not cart:
            return JsonResponse({
                'success': False,
                'message': 'سبد خرید یافت نشد'
            }, status=404)

        # حذف محصول
        success = cart.remove_product(product)

        if success:
            return JsonResponse({
                'success': True,
                'message': 'محصول از سبد خرید حذف شد',
                'cart_total': cart.final_price,
                'items_count': cart.items_count
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'محصول در سبد خرید یافت نشد'
            }, status=404)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'message': 'داده‌های JSON نامعتبر است'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'خطا در حذف از سبد خرید: {str(e)}'
        }, status=500)

@require_http_methods(["GET"])
def get_cart_details(request):
    """دریافت جزئیات سبد خرید"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'لطفاً ابتدا وارد حساب کاربری خود شوید'
        }, status=401)

    cart = get_or_create_cart(request)

    if not cart:
        return JsonResponse({
            'success': False,
            'message': 'سبد خرید یافت نشد'
        }, status=404)

    items = []
    for item in cart.items.all():
        first_image = item.product.gallery.first()
        items.append({
            'id': item.product.id,
            'name': item.product_name,
            'price': float(item.price),
            'quantity': item.quantity,
            'total_price': float(item.total_price),
            'image': first_image.image.url if first_image else None
        })

    return JsonResponse({
        'success': True,
        'cart': {
            'id': cart.id,
            'plan_name': cart.plan.name,
            'plan_price': cart.plan.price if cart.plan.price else 0,
            'total_price': cart.total_price,
            'final_price': cart.final_price,
            'items_count': cart.items_count,
            'items': items
        }
    })


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
from .models import ProductOrder, ProductOrderDetail, OrderDetailInfo, Plan

@login_required
def checkout_view(request, order_id):
    """صفحه checkout بسیار ساده"""
    # دریافت سفارش با بررسی مالکیت
    cart = get_object_or_404(ProductOrder, id=order_id, user=request.user, status='draft')

    # بررسی آیا پلنی وجود دارد
    plan = cart.plan
    if not plan:
        messages.error(request, 'پلنی برای این سفارش یافت نشد')
        return redirect('plan:plan_list')

    # محاسبه قیمت‌ها
    plan_price = plan.price if plan.price else 0
    tax_amount = int(plan_price * 0.09)
    total_price = plan_price + tax_amount

    # دریافت شماره موبایل کاربر
    mobile_number = request.user.mobileNumber

    context = {
        'plan': plan,
        'plan_price': plan_price,
        'tax_amount': tax_amount,
        'total_price': total_price,
        'order_id': order_id,
        'mobile_number': mobile_number,
    }

    return render(request, 'plan_app/checkout.html', context)

@require_http_methods(["POST"])
@csrf_exempt
def apply_discount(request, order_id):
    """اعمال کد تخفیف برای سفارش خاص"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'لطفاً وارد شوید'})

    try:
        data = json.loads(request.body)
        discount_code = data.get('discount_code')

        # بررسی مالکیت سفارش
        cart = get_object_or_404(ProductOrder, id=order_id, user=request.user, status='draft')

        # محاسبه مجدد قیمت‌ها
        cart.calculate_prices()

        # منطق اعمال تخفیف
        discount_amount = 0
        if discount_code == "WELCOME10":
            discount_amount = int(cart.final_price * 0.1)  # 10% تخفیف
        elif discount_code == "SAVE5":
            discount_amount = int(cart.final_price * 0.05)  # 5% تخفیف
        elif discount_code == "FIXED5000" and cart.final_price >= 100000:
            discount_amount = 5000  # 5000 تومان تخفیف ثابت
        else:
            return JsonResponse({'success': False, 'message': 'کد تخفیف نامعتبر است'})

        # محاسبه قیمت جدید با تخفیف
        new_final_price = cart.final_price - discount_amount
        tax_amount = int(new_final_price * 0.09)
        shipping_cost = 0
        new_total = new_final_price + tax_amount + shipping_cost

        return JsonResponse({
            'success': True,
            'message': 'کد تخفیف اعمال شد',
            'discount_amount': discount_amount,
            'new_final_price': new_final_price,
            'new_total': new_total,
            'tax_amount': tax_amount,
            'original_total': cart.final_price + int(cart.final_price * 0.09)
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'خطا: {str(e)}'})


@require_http_methods(["POST"])
def complete_order(request, order_id):
    """هدایت مستقیم به درگاه پرداخت بدون ذخیره داده"""
    if not request.user.is_authenticated:
        messages.error(request, 'لطفاً وارد شوید')
        return redirect('accounts:send_mobile')

    try:
        # فقط بررسی مالکیت سفارش
        cart = get_object_or_404(ProductOrder, id=order_id, user=request.user, status='draft')

        # تغییر وضعیت سفارش به pending (اختیاری)
        cart.status = 'pending'
        cart.save()

        # هدایت مستقیم به درگاه پرداخت
        from apps.peyment.views import unified_send_request
        return unified_send_request(request, 'product', cart.id)

    except ProductOrder.DoesNotExist:
        messages.error(request, 'سفارش یافت نشد')
        return redirect('plan:plan_list')
    except Exception as e:
        logger.error(f"Error in complete_order: {str(e)}")
        messages.error(request, 'خطا در اتصال به درگاه پرداخت')
        return redirect('product:checkout_view', order_id=order_id)


def get_or_create_cart(request):
    """دریافت یا ایجاد سبد خرید - تابع کمکی"""
    if request.user.is_authenticated:
        cart = ProductOrder.objects.filter(
            user=request.user,
            status='draft'
        ).first()

        if not cart:
            default_plan = Plan.objects.filter(isActive=True).first()
            if default_plan:
                cart = ProductOrder.objects.create(
                    user=request.user,
                    plan=default_plan,
                    status='draft'
                )

        return cart
    return None

def create_checkout_session(request):
    """ایجاد session برای checkout و redirect به صفحه checkout"""
    if not request.user.is_authenticated:
        return redirect('login')

    cart = get_or_create_cart(request)


    # redirect به صفحه checkout با ID سفارش
    return redirect('product:checkout', order_id=cart.id)