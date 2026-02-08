# web/celery.py (کنار settings.py)
import os
from celery import Celery

# تنظیم متغیر محیطی Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

app = Celery('web')

# بارگیری تنظیمات از Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# جستجوی خودکار تسک‌ها
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')