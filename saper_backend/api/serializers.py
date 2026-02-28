from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Leaderboard, GameResult

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'total_games', 'wins', 
                 'best_time_beginner', 'best_time_intermediate', 'best_time_expert']

class RegisterSerializer(serializers.Serializer):
    """Сериализатор регистрации с паролем"""
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=1, style={'input_type': 'password'})
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким ником уже существует")
        return value
    
    def create(self, validated_data):
        # Создаём пользователя с паролем
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class LeaderboardSerializer(serializers.ModelSerializer):
    """Сериализатор таблицы лидеров"""
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Leaderboard
        fields = ['id', 'username', 'mines', 'time', 'difficulty', 'created_at']

class GameResultSerializer(serializers.ModelSerializer):
    """Сериализатор результата игры"""
    class Meta:
        model = GameResult
        fields = ['result', 'mines', 'timestamp']

class SaveScoreSerializer(serializers.Serializer):
    """Сериализатор сохранения счёта"""
    mines = serializers.IntegerField(min_value=1, max_value=10)
    time = serializers.CharField(max_length=10)