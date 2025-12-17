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