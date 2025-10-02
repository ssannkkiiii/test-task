from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import User
from lunch_service.apps.employees.models import EmployeeProfile

@receiver(post_save, sender=User)
def create_employee_profile(sender, instance, created, **kwargs):
    if created and instance.is_employee:
        EmployeeProfile.objects.create(
            user=instance,
            employee_id=f"EMP{instance.id:04d}",
            department=instance.department or "General",
            hire_date=timezone.now().date()
        )