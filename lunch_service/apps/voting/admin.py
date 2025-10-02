from django.contrib import admin
from .models import Vote, VotingResult


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'menu', 'date', 'created_at')
    list_filter = ('date', 'created_at', 'menu__restaurant')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'menu__restaurant__name')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Vote Information', {
            'fields': ('user', 'menu', 'date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


@admin.register(VotingResult)
class VotingResultAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_votes', 'created_at')
    list_filter = ('date', 'created_at')
    search_fields = ('date',)
    ordering = ('-date',)
    
    fieldsets = (
        ('Result Information', {
            'fields': ('date', 'total_votes', 'results')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
