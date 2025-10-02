from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from lunch_service.apps.restaurants.models import Restaurant


class Menu(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='menus'
    )
    date = models.DateField()
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menus'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'
        unique_together = ['restaurant', 'date']
        ordering = ['-date', 'restaurant__name']

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"

    @property
    def is_today(self):
        return self.date == timezone.now().date()

    @property
    def total_items(self):
        return self.items.count()


class MenuItem(models.Model):

    CATEGORY_CHOICES = [
        ('appetizer', 'Appetizer'),
        ('main_course', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
        ('salad', 'Salad'),
        ('soup', 'Soup'),
    ]

    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name='items'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    is_vegetarian = models.BooleanField(default=False)
    is_vegan = models.BooleanField(default=False)
    is_gluten_free = models.BooleanField(default=False)
    allergens = models.TextField(blank=True, null=True, help_text="List of allergens")
    calories = models.PositiveIntegerField(blank=True, null=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menu_items'
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} - {self.menu.restaurant.name}"

    @property
    def dietary_info(self):
        info = []
        if self.is_vegetarian:
            info.append('Vegetarian')
        if self.is_vegan:
            info.append('Vegan')
        if self.is_gluten_free:
            info.append('Gluten Free')
        return info
