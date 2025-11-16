from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import ListView, DetailView
from .models import Plan
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import json
from django.contrib import messages
from django.utils import timezone
from .models import Plan, PlanOrder
from apps.product.models import Product

@login_required



def plan_list(request):
    plans = Plan.objects.filter(isActive=True).prefetch_related('features').order_by('price')

    context = {
        'plans': plans
    }
    return render(request, 'plan_app/plan_list.html', context)



@login_required
def purchase_plan(request, plan_slug):
    """انتخاب پلن و اضافه کردن به سبد خرید (بدون پرداخت)"""
    plan = get_object_or_404(Plan, slug=plan_slug, isActive=True)

    # بررسی آیا کاربر همین پلن رو قبلاً انتخاب کرده و پرداخت نکرده
    existing_unpaid_order = PlanOrder.objects.filter(
        user=request.user,
        plan=plan,
        isPaid=False  # فقط بررسی پلن‌های پرداخت نشده
    ).first()

    if existing_unpaid_order:
        messages.info(request, 'این پلن قبلاً در سبد خرید شما وجود دارد')
        return redirect('plan:shop_cart')

    # ایجاد سفارش با وضعیت پرداخت نشده
    plan_order = PlanOrder.objects.create(
        plan=plan,
        user=request.user,
        finalPrice=plan.price if plan.price else 0,
        isPaid=False,  # مهم: ابتدا False باشد
        paidAt=None    # پرداخت نشده
    )

    messages.success(request, f'پلن {plan.name} به سبد خرید اضافه شد')
    return redirect('plan:shop_cart')  # هدایت به سبد خرید


# apps/plan/views.py
@login_required
def shop_cart(request):
    """
    نمایش سبد خرید کاربر با آخرین پلن انتخابی (پرداخت نشده) و محصولات
    """
    # دریافت آخرین پلن پرداخت نشده کاربر
    latest_plan_order = PlanOrder.objects.filter(
        user=request.user,
        isPaid=False  # فقط پلن‌های پرداخت نشده
    ).select_related('plan').order_by('-createdAt').first()

    # دریافت محصولات فعال به همراه گالری و ویژگی‌ها
    products = Product.objects.filter(
        is_active=True
    ).prefetch_related(
        'features',
        'gallery'
    ).order_by('-publish_date')

    selected_plan = None
    plan_cost = 0
    stands_cost = 0
    tax_cost = 0
    total_cost = 0

    if latest_plan_order:
        selected_plan = latest_plan_order.plan
        plan_cost = selected_plan.price if selected_plan.price else 0

        # محاسبات مالی
        stands_cost = 0
        tax_cost = int((plan_cost + stands_cost) * 0.09)
        total_cost = plan_cost + stands_cost + tax_cost

    context = {
        'selected_plan': selected_plan,
        'plan_cost': plan_cost,
        'stands_cost': stands_cost,
        'tax_cost': tax_cost,
        'total_cost': total_cost,
        'latest_plan_order': latest_plan_order,
        'products': products,  # اضافه کردن محصولات به context
    }

    return render(request, 'plan_app/shop_cart.html', context)


# views.py
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from apps.product.models import ProductOrder, ProductOrderDetail

@login_required
@require_POST
def add_product_to_cart(request):
    """افزودن محصول به سبد خرید"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))

        # پیدا کردن آخرین سفارش پرداخت نشده کاربر
        product_order = ProductOrder.objects.filter(
            user=request.user,
            isPaid=False
        ).order_by('-createdAt').first()

        if not product_order:
            return JsonResponse({
                'success': False,
                'message': 'لطفاً ابتدا یک پلن انتخاب کنید'
            }, status=400)

        product = get_object_or_404(Product, id=product_id, is_active=True)

        # بررسی آیا محصول قبلاً اضافه شده
        order_item, created = ProductOrderDetail.objects.get_or_create(
            product_order=product_order,
            product=product,
            defaults={
                'quantity': quantity,
                'price': product.price
            }
        )

        if not created:
            order_item.quantity += quantity
            order_item.save()

        # محاسبه قیمت‌های به روز شده
        product_order.calculate_prices()
        product_order.save()

        return JsonResponse({
            'success': True,
            'message': 'محصول به سبد خرید اضافه شد',
            'cart_total': product_order.final_price,
            'items_count': product_order.items.count()
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'خطا در افزودن محصول'
        }, status=400)

@login_required
@require_POST
def update_cart_item(request):
    """بروزرسانی تعداد محصول در سبد خرید"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))

        if quantity <= 0:
            return JsonResponse({
                'success': False,
                'message': 'تعداد باید بیشتر از صفر باشد'
            }, status=400)

        order_item = get_object_or_404(
            ProductOrderDetail,
            id=item_id,
            product_order__user=request.user,
            product_order__isPaid=False
        )

        order_item.quantity = quantity
        order_item.save()

        # محاسبه مجدد قیمت‌ها
        product_order = order_item.product_order
        product_order.calculate_prices()
        product_order.save()

        return JsonResponse({
            'success': True,
            'message': 'تعداد محصول بروزرسانی شد',
            'item_total': order_item.total_price,
            'cart_total': product_order.final_price
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'خطا در بروزرسانی محصول'
        }, status=400)

@login_required
@require_POST
def remove_cart_item(request):
    """حذف محصول از سبد خرید"""
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')

        order_item = get_object_or_404(
            ProductOrderDetail,
            id=item_id,
            product_order__user=request.user,
            product_order__isPaid=False
        )

        product_order = order_item.product_order
        order_item.delete()

        # محاسبه مجدد قیمت‌ها
        product_order.calculate_prices()
        product_order.save()

        return JsonResponse({
            'success': True,
            'message': 'محصول از سبد خرید حذف شد',
            'cart_total': product_order.final_price,
            'items_count': product_order.items.count()
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': 'خطا در حذف محصول'
        }, status=400)

@login_required
def get_cart_summary(request):
    """دریافت خلاصه سبد خرید برای نمایش در لحظه"""
    product_order = ProductOrder.objects.filter(
        user=request.user,
        isPaid=False
    ).order_by('-createdAt').first()

    if not product_order:
        return JsonResponse({
            'cart_total': 0,
            'items_count': 0,
            'items': []
        })

    items_data = []
    for item in product_order.items.all():
        items_data.append({
            'id': item.id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'unit_price': float(item.price),
            'total_price': float(item.total_price)
        })

    return JsonResponse({
        'cart_total': product_order.final_price,
        'items_count': product_order.items.count(),
        'items': items_data,
        'plan_price': product_order.plan.price if product_order.plan.price else 0,
        'products_total': product_order.total_price - (product_order.plan.price if product_order.plan.price else 0)
    })



    