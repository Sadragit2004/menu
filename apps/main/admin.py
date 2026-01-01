from django.contrib import admin
from django.utils.html import format_html
from .models import TextImageBlock


@admin.register(TextImageBlock)
class TextImageBlockAdmin(admin.ModelAdmin):
    list_display = ("title", "image_position", "order")
    search_fields = ("title", "text",)





from django.contrib import admin
from .models import Content

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['is_active']
    list_per_page = 20

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'image', 'description', 'is_active')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ['created_at', 'updated_at']

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('-created_at')

# admin.py - نسخه ساده‌تر
from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # نمایش در لیست ادمین
    list_display = [
        'title',
        'is_active',
        'created_at',
        'has_thumbnail',
        'has_video_link'
    ]

    # فیلدهای قابل جستجو
    search_fields = ['title', 'description']

    # فیلترها
    list_filter = ['is_active', 'created_at']

    # فیلدهای قابل ویرایش در لیست
    list_editable = ['is_active']

    # فیلدهای فقط خواندنی
    readonly_fields = ['created_at', 'updated_at']

    # فیلدهایی که به صورت خودکار پر می‌شوند

    # چیدمان فرم
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('title', 'description')
        }),
        ('رسانه‌ها', {
            'fields': ('thumbnail', 'video_link')
        }),
        ('تنظیمات', {
            'fields': ('is_active',)
        }),
        ('اطلاعات زمانی', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    # متدهای کمکی برای نمایش
    def has_thumbnail(self, obj):
        return "✅" if obj.thumbnail else "❌"
    has_thumbnail.short_description = 'تصویر'

    def has_video_link(self, obj):
        return "✅" if obj.video_link else "❌"
    has_video_link.short_description = 'ویدیو'