from django.contrib import admin
from .models import Menu, MenuItem


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('name', 'category', 'price', 'is_vegetarian', 'is_vegan', 'is_gluten_free', 'is_available')


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'date', 'title', 'is_active', 'total_items', 'created_at')
    list_filter = ('is_active', 'date', 'restaurant', 'created_at')
    search_fields = ('title', 'restaurant__name', 'description')
    ordering = ('-date', 'restaurant__name')
    inlines = [MenuItemInline]
    
    fieldsets = (
        ('Menu Information', {
            'fields': ('restaurant', 'date', 'title', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'total_items')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu', 'category', 'price', 'is_vegetarian', 'is_vegan', 'is_gluten_free', 'is_available')
    list_filter = ('category', 'is_vegetarian', 'is_vegan', 'is_gluten_free', 'is_available', 'menu__restaurant')
    search_fields = ('name', 'description', 'menu__title', 'menu__restaurant__name')
    ordering = ('menu', 'category', 'name')
    
    fieldsets = (
        ('Item Information', {
            'fields': ('menu', 'name', 'description', 'category', 'price')
        }),
        ('Dietary Information', {
            'fields': ('is_vegetarian', 'is_vegan', 'is_gluten_free', 'allergens')
        }),
        ('Additional Information', {
            'fields': ('calories', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
