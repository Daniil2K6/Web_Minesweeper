from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Leaderboard, GameResult

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'total_games', 'wins', 'last_game_result']
    list_filter = ['is_superuser', 'is_active']
    search_fields = ['username', 'email']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Статистика', {
            'fields': ('total_games', 'wins', 'best_time_beginner', 
                      'best_time_intermediate', 'best_time_expert', 'last_game_result')
        }),
    )

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'mines', 'time', 'difficulty', 'created_at']
    list_filter = ['difficulty']
    search_fields = ['user__username']

@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'result', 'mines', 'timestamp']
    list_filter = ['result']
    search_fields = ['user__username']