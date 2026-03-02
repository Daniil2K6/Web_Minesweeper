from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class SimpleUser(models.Model):
    """Простая таблица пользователей для админки и вывода"""
    username = models.CharField(max_length=150, unique=True, verbose_name="Имя пользователя")
    password = models.CharField(max_length=128, verbose_name="Пароль")
    best_time = models.FloatField(null=True, blank=True, verbose_name="Лучшее время")
    data_top_game = models.DateTimeField(null=True, blank=True, verbose_name="Дата лучшей игры")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь (простая таблица)"
        verbose_name_plural = "Пользователи (простая таблица)"

class Leaderboard(models.Model):
    """Таблица лидеров"""
    user = models.ForeignKey('SimpleUser', on_delete=models.CASCADE, related_name='records')
    time = models.FloatField(verbose_name="Время (секунды)", help_text="Время в секундах с точностью 0.001")
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Рекорд"
        verbose_name_plural = "Рекорды"
        ordering = ['time']
    
    def __str__(self):
        return f"{self.user.username} - {self.time:.3f}с"