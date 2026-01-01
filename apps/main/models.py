from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
import utils

class TextImageBlock(models.Model):

    POSITION_CHOICES = [
        ('left', ('تصویر در چپ')),
        ('right', ('تصویر در راست')),
    ]
    title = models.CharField(max_length=255, verbose_name=('عنوان'))
    text = RichTextUploadingField(verbose_name=('متن'))
    upload_file = utils.FileUpload('images','Review')
    image = models.FileField(upload_to=upload_file.upload_to, verbose_name=('تصویر'))
    image_position = models.CharField(max_length=5, choices=POSITION_CHOICES, default='right', verbose_name=('موقعیت تصویر'))
    order = models.PositiveIntegerField(default=0, verbose_name=('ترتیب نمایش'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = ('باکس متن و تصویر')
        verbose_name_plural = ('باکس‌های متن و تصویر')
        ordering = ['order']




from django.db import models

class Content(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    image = models.ImageField(upload_to='images/', verbose_name="عکس")
    description = models.TextField(verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "محتوا"
        verbose_name_plural = "محتواها"
        ordering = ['-created_at']

    def __str__(self):
        return self.title




# models.py
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import os

class Course(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name="عنوان",
        help_text="عنوان دوره آموزشی"
    )

    description = models.TextField(
        verbose_name="توضیحات",
        help_text="توضیحات کامل دوره"
    )

    video_link = models.URLField(
        max_length=500,
        verbose_name="لینک ویدیو",
        help_text="لینک ویدیو آموزشی",
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال",
        help_text="آیا دوره فعال است؟"
    )

    thumbnail = models.ImageField(
        upload_to='courses/thumbnails/',
        verbose_name="عکس پیش فرض",
        help_text="تصویر شاخص دوره",
        default='courses/default_thumbnail.jpg',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="ساخته شده"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخرین بروزرسانی"
    )



    class Meta:
        verbose_name = "دوره"
        verbose_name_plural = "دوره‌ها"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    