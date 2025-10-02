from django.contrib import admin
from .models import EmployeeProfile


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'position', 'hire_date', 'is_active')
    list_filter = ('department', 'is_active', 'hire_date')
    search_fields = ('employee_id', 'user__first_name', 'user__last_name', 'user__email', 'department')
    ordering = ('employee_id',)
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('user', 'employee_id', 'department', 'position')
        }),
        ('Employment Details', {
            'fields': ('hire_date', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
