from django import forms
from django.core.exceptions import ValidationError
from apps.user.validators.mobile_validator import validate_iranian_mobile
from .models import Waiter

class WaiterForm(forms.Form):
    """
    فرم ایجاد گارسون
    """
    restaurant = forms.ModelChoiceField(
        queryset=None,
        required=True,
        label="رستوران",
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    fullname = forms.CharField(
        max_length=255,
        required=True,
        label="نام کامل",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی گارسون'
        })
    )

    mobileNumber = forms.CharField(
        max_length=11,
        required=True,
        validators=[validate_iranian_mobile],
        label="شماره موبایل",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '09xxxxxxxxx'
        })
    )

    age = forms.IntegerField(
        required=False,
        label="سن",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'سن گارسون'
        })
    )

    description = forms.CharField(
        required=False,
        label="توضیحات",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'توضیحات اضافی (اختیاری)',
            'rows': 3
        })
    )

    def __init__(self, *args, **kwargs):
        # فقط restaurant_queryset را می‌گیریم
        restaurant_queryset = kwargs.pop('restaurant_queryset', None)
        super().__init__(*args, **kwargs)

        # تنظیم کوئری‌ست برای فیلد رستوران
        if restaurant_queryset is not None:
            self.fields['restaurant'].queryset = restaurant_queryset

    def clean_mobileNumber(self):
        mobile = self.cleaned_data.get('mobileNumber')
        if mobile:
            # بررسی تکراری نبودن شماره موبایل
            if Waiter.objects.filter(mobileNumber=mobile).exists():
                raise ValidationError("این شماره موبایل قبلاً ثبت شده است.")
        return mobile

    def save(self, commit=True):
        """
        متد save برای ایجاد گارسون جدید
        """
        waiter = Waiter(
            restaurant=self.cleaned_data['restaurant'],
            fullname=self.cleaned_data['fullname'],
            mobileNumber=self.cleaned_data['mobileNumber'],
            age=self.cleaned_data['age'],
            description=self.cleaned_data['description']
        )

        if commit:
            waiter.save()

        return waiter

class WaiterEditForm(forms.Form):
    """
    فرم ویرایش گارسون
    """
    fullname = forms.CharField(
        max_length=255,
        required=True,
        label="نام کامل",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی گارسون'
        })
    )

    mobileNumber = forms.CharField(
        max_length=11,
        required=True,
        validators=[validate_iranian_mobile],
        label="شماره موبایل",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '09xxxxxxxxx'
        })
    )

    age = forms.IntegerField(
        required=False,
        label="سن",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'سن گارسون'
        })
    )

    description = forms.CharField(
        required=False,
        label="توضیحات",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'توضیحات اضافی (اختیاری)',
            'rows': 3
        })
    )

    isActive = forms.BooleanField(
        required=False,
        label="فعال",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    def __init__(self, *args, **kwargs):
        # فقط instance را می‌گیریم
        self.waiter_instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

        # پر کردن مقدار اولیه اگر instance داده شده باشد
        if self.waiter_instance:
            self.fields['fullname'].initial = self.waiter_instance.fullname
            self.fields['mobileNumber'].initial = self.waiter_instance.mobileNumber
            self.fields['age'].initial = self.waiter_instance.age
            self.fields['description'].initial = self.waiter_instance.description
            self.fields['isActive'].initial = self.waiter_instance.isActive

    def clean_mobileNumber(self):
        mobile = self.cleaned_data.get('mobileNumber')
        if mobile and self.waiter_instance:
            # بررسی تکراری نبودن شماره موبایل (به جز خود گارسون)
            if Waiter.objects.filter(mobileNumber=mobile).exclude(id=self.waiter_instance.id).exists():
                raise ValidationError("این شماره موبایل قبلاً توسط گارسون دیگری ثبت شده است.")
        return mobile

    def save(self, commit=True):
        """
        متد save برای بروزرسانی گارسون موجود
        """
        if not self.waiter_instance:
            raise ValueError("Instance is required for saving")

        self.waiter_instance.fullname = self.cleaned_data['fullname']
        self.waiter_instance.mobileNumber = self.cleaned_data['mobileNumber']
        self.waiter_instance.age = self.cleaned_data['age']
        self.waiter_instance.description = self.cleaned_data['description']
        self.waiter_instance.isActive = self.cleaned_data['isActive']

        if commit:
            self.waiter_instance.save()

        return self.waiter_instance