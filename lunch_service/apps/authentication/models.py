from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):        
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, verbose_name='User first name')
    last_name = models.CharField(max_length=255, verbose_name='User last name')
    date_of_birth = models.DateField(null=True, blank=True)
    is_employee = models.BooleanField(default=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)
