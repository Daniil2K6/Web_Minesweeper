from django.urls import path
from . import views

urlpatterns = [
    # CSRF
    path('csrf-token', views.get_csrf_token, name='csrf_token'),
    
    # Auth
    path('login', views.login_view, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('admin/logout', views.admin_logout, name='admin_logout'),
    path('current-user', views.current_user, name='current_user'),
    
    # Game
    path('save-score', views.save_score, name='save_score'),
    
    # Leaderboard
    path('leaderboard', views.leaderboard, name='leaderboard'),
    path('user-stats', views.user_stats, name='user_stats'),
    
    # Admin
    path('admin/reset-leaderboard', views.reset_leaderboard, name='reset_leaderboard'),
    path('admin/delete-player/<str:username>', views.delete_player, name='delete_player'),
]