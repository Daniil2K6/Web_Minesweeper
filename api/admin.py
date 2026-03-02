from django.contrib import admin
from .models import SimpleUser, Leaderboard

@admin.register(SimpleUser)
class SimpleUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'best_time']
    search_fields = ['username']
    ordering = ['id']

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'time', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username']
    ordering = ['time']