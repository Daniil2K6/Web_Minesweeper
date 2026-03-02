from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import SimpleUser, Leaderboard

class SimpleUserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя (простая таблица)"""
    class Meta:
        model = SimpleUser
        fields = ['id', 'username', 'password', 'best_time', 'data_top_game']

class RegisterSerializer(serializers.ModelSerializer):
    """Сериализатор регистрации для SimpleUser"""
    class Meta:
        model = SimpleUser
        fields = ['username', 'password']

class LeaderboardSerializer(serializers.ModelSerializer):
    """Сериализатор таблицы лидеров"""
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Leaderboard
        fields = ['id', 'username', 'time', 'created_at']

class SaveScoreSerializer(serializers.Serializer):
    """Сериализатор сохранения счёта"""
    time = serializers.FloatField(min_value=0.001)
    username = serializers.CharField(max_length=150, required=True)
    created_at = serializers.DateTimeField(required=False)