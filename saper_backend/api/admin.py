from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Leaderboard

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'total_games', 'wins']
    list_filter = ['is_superuser', 'is_active']
    search_fields = ['username', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Статистика', {
            'fields': ('total_games', 'wins')
        }),
    )

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'time', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    ordering = ['time']