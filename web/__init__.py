# myproject/__init__.py (کنار settings.py)
from .celery import app as celery_app

__all__ = ('celery_app',)