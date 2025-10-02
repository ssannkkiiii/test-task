from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EmployeeProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_profile')
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'employee_profiles'
        verbose_name = 'Employee Profile'
        verbose_name_plural = 'Employee Profiles'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.full_name} ({self.employee_id})"

    @property
    def full_name(self):
        return self.user.full_name

    @property
    def email(self):
        return self.user.email
