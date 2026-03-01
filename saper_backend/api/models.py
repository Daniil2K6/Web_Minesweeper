from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Модель пользователя"""
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="api_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="api_user_set",
        related_query_name="user",
    )
    
    total_games = models.IntegerField(default=0, verbose_name="Всего игр")
    wins = models.IntegerField(default=0, verbose_name="Побед")
    
    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
    
    def __str__(self):
        return self.username

class Leaderboard(models.Model):
    """Таблица лидеров"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    time = models.FloatField(verbose_name="Время (секунды)", help_text="Время в секундах с точностью 0.001")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Рекорд"
        verbose_name_plural = "Рекорды"
        ordering = ['time']
    
    def __str__(self):
        return f"{self.user.username} - {self.time:.3f}с"