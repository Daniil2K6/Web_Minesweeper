from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """Модель пользователя"""
    # Убираем конфликт related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="api_user_set",  # Уникальное имя
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="api_user_set",  # Уникальное имя
        related_query_name="user",
    )
    
    # Дополнительные поля
    total_games = models.IntegerField(default=0, verbose_name="Всего игр")
    wins = models.IntegerField(default=0, verbose_name="Побед")
    best_time_beginner = models.IntegerField(null=True, blank=True, verbose_name="Лучшее время (новичок)")
    best_time_intermediate = models.IntegerField(null=True, blank=True, verbose_name="Лучшее время (любитель)")
    best_time_expert = models.IntegerField(null=True, blank=True, verbose_name="Лучшее время (профессионал)")
    last_game_result = models.CharField(max_length=10, null=True, blank=True, verbose_name="Последний результат")
    
    class Meta:
        verbose_name = "Игрок"
        verbose_name_plural = "Игроки"
    
    def __str__(self):
        return self.username

class Leaderboard(models.Model):
    """Таблица лидеров"""
    DIFFICULTY_CHOICES = [
        ('beginner', 'Новичок'),
        ('intermediate', 'Любитель'),
        ('expert', 'Профессионал'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='records')
    mines = models.IntegerField(default=10, verbose_name="Количество мин")
    time = models.CharField(max_length=10, verbose_name="Время")
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Рекорд"
        verbose_name_plural = "Рекорды"
        ordering = ['mines', 'time']
    
    def __str__(self):
        return f"{self.user.username} - {self.mines} мин - {self.time}"

class GameResult(models.Model):
    """Результаты игр"""
    RESULT_CHOICES = [
        ('win', 'Победа'),
        ('lose', 'Поражение'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_results')
    result = models.CharField(max_length=10, choices=RESULT_CHOICES)
    mines = models.IntegerField(default=10)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Результат игры"
        verbose_name_plural = "Результаты игр"
        ordering = ['-timestamp']