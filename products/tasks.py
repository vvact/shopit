# products/tasks.py
from django.utils import timezone
from celery import shared_task
from .models import FlashDeal

@shared_task
def deactivate_expired_flash_deals():
    now = timezone.now()
    expired = FlashDeal.objects.filter(is_active=True, end_time__lt=now)
    count = expired.update(is_active=False)
    return f"Deactivated {count} expired deals."
