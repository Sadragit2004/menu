# apps/order/tasks.py
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from apps.menu.models.menufreemodels.models import Restaurant
from .models import Ordermenu, MenuImage
import logging

logger = logging.getLogger(__name__)
