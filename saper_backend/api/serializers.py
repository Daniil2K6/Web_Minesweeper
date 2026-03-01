from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Leaderboard

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'total_games', 'wins']

class RegisterSerializer(serializers.Serializer):
    """Сериализатор регистрации с паролем"""
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=1, style={'input_type': 'password'})
    
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким ником уже существует")
        return value
    
    def create(self, validated_data):
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
        fields = ['id', 'username', 'time', 'created_at']

class SaveScoreSerializer(serializers.Serializer):
    """Сериализатор сохранения счёта"""
    time = serializers.FloatField(min_value=0.001)