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
from apps.user.models import CustomUser

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
    """صفحه checkout با داده‌های داینامیک و اطلاعات قبلی کاربر"""
    # دریافت سفارش با بررسی مالکیت
    cart = get_object_or_404(ProductOrder, id=order_id, user=request.user, status='draft')

    if cart.items.count() == 0:
        return redirect('cart_empty')

    # محاسبه قیمت‌ها
    cart.calculate_prices()

    # محاسبه مالیات و هزینه‌ها
    tax_amount = int(cart.final_price * 0.09)  # 9% مالیات
    shipping_cost = 0  # هزینه ارسال
    total_with_tax = cart.final_price + tax_amount + shipping_cost

    # بررسی آیا اطلاعات قبلی برای این سفارش وجود دارد
    previous_info = None
    try:
        previous_info = OrderDetailInfo.objects.get(product_order=cart)
    except OrderDetailInfo.DoesNotExist:
        # اگر اطلاعات برای این سفارش وجود ندارد، اطلاعات آخرین سفارش کاربر را پیدا کن
        previous_orders = ProductOrder.objects.filter(
            user=request.user
        ).exclude(id=order_id).order_by('-createdAt')

        for order in previous_orders:
            try:
                previous_info = OrderDetailInfo.objects.get(product_order=order)
                break
            except OrderDetailInfo.DoesNotExist:
                continue

    context = {
        'cart': cart,
        'plan': cart.plan,
        'items': cart.items.all(),
        'subtotal': cart.total_price,
        'tax': tax_amount,
        'shipping': shipping_cost,
        'total': total_with_tax,
        'order_id': order_id,
        'previous_info': previous_info  # اطلاعات قبلی کاربر
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
    """تکمیل سفارش و ذخیره اطلاعات"""
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'message': 'لطفاً وارد شوید'})

    try:
        # بررسی مالکیت سفارش
        cart = get_object_or_404(ProductOrder, id=order_id, user=request.user, status='draft')

        if cart.items.count() == 0:
            return JsonResponse({'success': False, 'message': 'سبد خرید خالی است'})

        # دریافت اطلاعات از فرم
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        province = request.POST.get('province')
        postal_code = request.POST.get('postal_code')
        description = request.POST.get('description')
        discount_code = request.POST.get('discount_code', '')

        # اعتبارسنجی داده‌ها
        if not all([full_name, phone_number, address, city, province, postal_code]):
            return JsonResponse({'success': False, 'message': 'لطفاً تمام فیلدهای ضروری را پر کنید'})

        # محاسبه تخفیف
        discount_amount = 0
        if discount_code:
            if discount_code == "WELCOME10":
                discount_amount = int(cart.final_price * 0.1)
            elif discount_code == "SAVE5":
                discount_amount = int(cart.final_price * 0.05)
            elif discount_code == "FIXED5000" and cart.final_price >= 100000:
                discount_amount = 5000

        # اعمال تخفیف بر روی قیمت نهایی
        if discount_amount > 0:
            cart.final_price -= discount_amount
            cart.save()

        # ایجاد یا بروزرسانی اطلاعات سفارش
        order_info, created = OrderDetailInfo.objects.get_or_create(
            product_order=cart,
            defaults={
                'full_name': full_name,
                'phone_number': phone_number,
                'email': email,
                'address': address,
                'city': city,
                'province': province,
                'codePost': postal_code,
                'description': description,
                'discount_code': discount_code if discount_amount > 0 else '',
                'discount_amount': discount_amount
            }
        )

        if not created:
            order_info.full_name = full_name
            order_info.phone_number = phone_number
            order_info.email = email
            order_info.address = address
            order_info.city = city
            order_info.province = province
            order_info.codePost = postal_code
            order_info.description = description
            order_info.discount_code = discount_code if discount_amount > 0 else ''
            order_info.discount_amount = discount_amount
            order_info.save()

        # تغییر وضعیت سفارش به pending
        cart.status = 'pending'
        cart.save()

        return JsonResponse({
            'success': True,
            'message': 'سفارش با موفقیت ثبت شد',
            'order_id': cart.id,
            'redirect_url': f'/payment/{cart.id}/'  # صفحه پرداخت
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': f'خطا در ثبت سفارش: {str(e)}'})

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
    if not cart or cart.items.count() == 0:
        return redirect('cart_empty')

    # redirect به صفحه checkout با ID سفارش
    return redirect('product:checkout', order_id=cart.id)