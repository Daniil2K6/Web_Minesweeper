from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('admin/logout', views.admin_logout, name='admin_logout'),
    
    # Game
    path('game-result', views.game_result, name='game_result'),
    path('save-score', views.save_score, name='save_score'),
    
    # Leaderboard
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('user-stats', views.user_stats, name='user_stats'),
    
    # Admin
    path('admin/reset-leaderboard', views.reset_leaderboard, name='reset_leaderboard'),
    path('admin/delete-player/<str:username>', views.delete_player, name='delete_player'),
]