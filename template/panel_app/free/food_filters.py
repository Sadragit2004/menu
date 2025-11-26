# templatetags/food_filters.py
from django import template
from apps.menu.models.menufreemodels.models import FoodRestaurant

register = template.Library()

@register.filter
def get_final_food_data(restaurant, food):
    """فیلتر برای دریافت اطلاعات نهایی غذا"""
    try:
        custom_food = FoodRestaurant.objects.get(restaurant=restaurant, food=food)
        return {
            'id': food.id,
            'title': food.title,
            'title_en': food.title_en,
            'description': food.description,
            'description_en': food.description_en,
            'price': custom_food.final_price,
            'image': custom_food.final_image,
            'preparationTime': food.preparationTime,
            'isActive': custom_food.is_active and food.isActive,
            'menuCategory': food.menuCategory,
            'slug': food.slug,
            'displayOrder': custom_food.display_order,
            'is_customized': custom_food.has_customizations(),
            'custom_food_id': custom_food.id
        }
    except FoodRestaurant.DoesNotExist:
        return {
            'id': food.id,
            'title': food.title,
            'title_en': food.title_en,
            'description': food.description,
            'description_en': food.description_en,
            'price': food.price,
            'image': food.image,
            'preparationTime': food.preparationTime,
            'isActive': food.isActive,
            'menuCategory': food.menuCategory,
            'slug': food.slug,
            'displayOrder': food.displayOrder,
            'is_customized': False,
            'custom_food_id': None
        }