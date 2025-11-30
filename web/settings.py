"""
Django settings for web project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-339igi*k2opmxfm^+3ys0gj&$m*a_x_#3y%bvod!)x7t@e#cv^')

DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third party apps
    'django_render_partial',
    'ckeditor',
    'ckeditor_uploader',
    'django_celery_results',
    'django_celery_beat',
    'channels',
    'storages',  # برای ذخیره‌سازی در لیارا

    # Your apps
    'apps.user.apps.UserConfig',
    'apps.menu.apps.MenuConfig',
    'apps.panel.apps.PanelConfig',
    'apps.blog.apps.BlogConfig',
    'apps.plan.apps.PlanConfig',
    'apps.product.apps.ProductConfig',
    'apps.order.apps.OrderConfig',
    'apps.peyment.apps.PeymentConfig',
    'apps.main.apps.MainConfig',
    'apps.table.apps.TableConfig',
    'apps.waiter.apps.WaiterConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'template/'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.main.views.media_admin',
                'apps.panel.views.viewsfree.restaurant_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'optimistic_nightingale',
        'USER': 'root',
        'PASSWORD': 'XjomClRJayAheMtDwB50RJQO',
        'HOST': 'web',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'use_unicode': True,
        },
        'CONN_MAX_AGE': 600,
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
TIME_ZONE = 'Asia/Tehran'
USE_TZ = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True
NUMBER_GROUPING = 3
THOUSAND_SEPARATOR = ','
LANGUAGE_CODE = 'fa-ir'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ==================== LIARA CONFIGURATION ====================

# WebSocket and Redis settings for Liara
if os.environ.get('LIARA'):
    # تنظیمات Redis برای لیارا
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')

    # تنظیمات Channels برای لیارا
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                "hosts": [REDIS_URL],
            },
        },
    }

    # تنظیمات Celery برای لیارا
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL

    # تنظیمات AWS S3 برای لیارا
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = os.environ.get('AWS_S3_ENDPOINT_URL')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'ir-thr-at1')

    # تنظیمات storage
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # تنظیمات اضافی
    AWS_S3_FILE_OVERWRITE = False
    AWS_DEFAULT_ACL = 'public-read'
    AWS_QUERYSTRING_AUTH = False
    AWS_LOCATION = 'media'

    # برای CKEditor
    CKEDITOR_STORAGE_BACKEND = 'storages.backends.s3boto3.S3Boto3Storage'

    # دیتابیس برای لیارا (اگر نیاز به تغییر داری)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'optimistic_nightingale'),
            'USER': os.environ.get('DB_USER', 'root'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'XjomClRJayAheMtDwB50RJQO'),
            'HOST': os.environ.get('DB_HOST', 'web'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {
                'charset': 'utf8mb4',
                'use_unicode': True,
            },
            'CONN_MAX_AGE': 600,
        }
    }

else:
    # تنظیمات لوکال
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    CKEDITOR_STORAGE_BACKEND = 'django.core.files.storage.FileSystemStorage'

    # تنظیمات Channels برای لوکال
CHANNEL_LAYERS = {
    "default": {
    "BACKEND": "channels_redis.pubsub.RedisPubSubChannelLayer",
    "CONFIG": {
        "hosts":[{
            "address": os.getenv('REDIS_URI'),
        }]}
    }
}

# Whitenoise برای فایل‌های استاتیک
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_USER_MODEL = 'user.CustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEditor settings
CKEDITOR_UPLOAD_PATH = 'images/cheditor/upload_files/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Bold', 'Link', 'Unlink', 'Image'],
        ],
    },
    'special': {
        'toolbar': 'full',
        'height': 500,
        'toolbar_Special': [
            ['Bold', 'Link', 'Unlink', 'Image'],
            ['CodeSnippet'],
        ],
        'extraPlugins': ','.join(['codesnippet', 'clipboard'])
    },
    'special_an': {
        'toolbar': 'Special',
        'height': 500,
        'toolbar_Special': [
            ['Bold'],
            ['CodeSnippet']
        ],
        'extraPlugins': ','.join(['codesnippet'])
    }
}

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    },
    'tokens': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'token-cache',
    }
}

# Celery settings (برای لوکال - در لیارا override می‌شود)
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tehran'

# Channels settings
ASGI_APPLICATION = 'web.asgi.application'

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True