from django.db import models
from django.core.validators import RegexValidator


class Restaurant(models.Model):

    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    address = models.TextField()
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'restaurants'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def is_available_today(self):
        from django.utils import timezone
        from lunch_service.apps.menus.models import Menu
        today = timezone.now().date()
        return Menu.objects.filter(restaurant=self, date=today, is_active=True).exists()
