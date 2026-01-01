from django.shortcuts import render
import web.settings as sett
from .models import TextImageBlock
# Create your views here.




def media_admin(request):

    context = {
        'media_url':sett.MEDIA_URL
    }

    return context



def main(request):

    return render(request,'main_app/main.html')



def main_content_view(request):
    contents = TextImageBlock.objects.all()
    return render(request, 'main_app/main_content.html', {'text_image_blocks': contents})







from .models import Content

def section1_view(request):
    contents = Content.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'main_app/section1.html', {'contents': contents})







from django.views.generic import ListView, TemplateView
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from django.core.paginator import Paginator
from apps.menu.models.menufreemodels.models import Restaurant
import math

# ویو برای لیست 20 رستوران جدیدترین با Swiper
class LatestRestaurantsView(TemplateView):
    template_name = 'main_app/latest_restaurants.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # فقط رستوران‌های فعال و منقضی نشده
        restaurants = Restaurant.objects.filter(isActive=True).exclude(
            Q(expireDate__lt=timezone.now()) & Q(expireDate__isnull=False)
        ).order_by('-createdAt')[:20]

        context['restaurants'] = restaurants
        context['title'] = 'جدیدترین رستوران‌ها'
        context['description'] = 'لیست ۲۰ رستوران جدید اضافه شده به سیستم'

        return context


# ویو برای نمایش همه رستوران‌ها با Infinite Scroll
class AllRestaurantsView(ListView):
    model = Restaurant
    template_name = 'main_app/all_restaurants.html'
    context_object_name = 'restaurants'
    paginate_by = 10  # هر بار 10 تا لود می‌شود

    def get_queryset(self):
        # فقط رستوران‌های فعال و منقضی نشده
        queryset = Restaurant.objects.filter(isActive=True).exclude(
            Q(expireDate__lt=timezone.now()) & Q(expireDate__isnull=False)
        ).order_by('-createdAt')

        # اعمال جستجو
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(title_en__icontains=search) |
                Q(english_name__icontains=search) |
                Q(description__icontains=search)
            )

        # فیلتر بر اساس دسته‌بندی
        category_slug = self.request.GET.get('category')
        if category_slug:
            from apps.menu.models.menufreemodels.models import Category, MenuCategory
            try:
                category = Category.objects.get(slug=category_slug, isActive=True)
                restaurant_ids = MenuCategory.objects.filter(
                    category=category,
                    restaurant__isActive=True
                ).values_list('restaurant_id', flat=True)
                queryset = queryset.filter(id__in=restaurant_ids)
            except Category.DoesNotExist:
                pass

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'همه رستوران‌ها'
        context['description'] = 'لیست کامل رستوران‌های موجود در سیستم'

        # اضافه کردن پارامترهای جستجو
        search_params = {}
        for key in ['search', 'category']:
            value = self.request.GET.get(key)
            if value:
                search_params[key] = value

        context['search_params'] = search_params

        # آمار
        context['total_restaurants'] = Restaurant.objects.filter(isActive=True).exclude(
            Q(expireDate__lt=timezone.now()) & Q(expireDate__isnull=False)
        ).count()

        from apps.menu.models.menufreemodels.models import Category
        context['categories'] = Category.objects.filter(
            isActive=True,
            parent__isnull=True
        )[:10]

        # اطلاعات برای infinite scroll
        page_obj = context.get('page_obj')
        if page_obj:
            context['has_next'] = page_obj.has_next()
            context['next_page'] = page_obj.next_page_number() if page_obj.has_next() else None

        return context


# API برای Infinite Scroll
def load_more_restaurants(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            page = int(request.GET.get('page', 1))
            search = request.GET.get('search', '')
            category = request.GET.get('category', '')

            # فیلتر اصلی
            queryset = Restaurant.objects.filter(isActive=True).exclude(
                Q(expireDate__lt=timezone.now()) & Q(expireDate__isnull=False)
            ).order_by('-createdAt')

            # اعمال فیلتر جستجو
            if search:
                queryset = queryset.filter(
                    Q(title__icontains=search) |
                    Q(title_en__icontains=search) |
                    Q(english_name__icontains=search) |
                    Q(description__icontains=search)
                )

            # فیلتر دسته‌بندی
            if category:
                from apps.menu.models.menufreemodels.models import Category, MenuCategory
                try:
                    category_obj = Category.objects.get(slug=category, isActive=True)
                    restaurant_ids = MenuCategory.objects.filter(
                        category=category_obj,
                        restaurant__isActive=True
                    ).values_list('restaurant_id', flat=True)
                    queryset = queryset.filter(id__in=restaurant_ids)
                except Category.DoesNotExist:
                    pass

            # صفحه‌بندی
            paginator = Paginator(queryset, 10)
            page_obj = paginator.get_page(page)

            restaurants_data = []
            for restaurant in page_obj:
                restaurants_data.append({
                    'id': restaurant.id,
                    'title': restaurant.title,
                    'slug': restaurant.slug,
                    'description': restaurant.description[:100] + '...' if restaurant.description and len(restaurant.description) > 100 else restaurant.description,
                    'cover_image': restaurant.coverImage.url if restaurant.coverImage else '',
                    'logo': restaurant.logo.url if restaurant.logo else '',
                    'created_at': restaurant.createdAt.strftime('%Y/%m/%d') if restaurant.createdAt else '',
                    'expiry_status': restaurant.expiry_status,
                    'is_expired': restaurant.is_expired,
                    'menu_url': f"/menu/{restaurant.slug}/"
                })

            return JsonResponse({
                'success': True,
                'restaurants': restaurants_data,
                'has_next': page_obj.has_next(),
                'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
                'current_page': page,
                'total_pages': paginator.num_pages
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)





def faq(request):

    return render(request,'main_app/partials/faq.html')



from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Course



def active_courses(request):
    """لیست دوره‌های فعال"""
    courses = Course.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'courses_َapp/course_list.html', {'courses': courses})