from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import login, logout
from django.utils import timezone
from .models import User, Leaderboard, GameResult
from .serializers import (
    UserSerializer, RegisterSerializer, LeaderboardSerializer,
    GameResultSerializer, SaveScoreSerializer
)

ADMIN_USERNAME = "N3XUS_C0R3"

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Регистрация нового пользователя"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Проверяем, не админ ли это
        role = 'admin' if user.username == ADMIN_USERNAME else 'user'
        
        # Автоматически логиним пользователя
        login(request, user)
        
        return Response({
            'message': 'Регистрация успешна',
            'user': UserSerializer(user).data,
            'role': role,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Выход из системы"""
    logout(request)
    return Response({'message': 'Выход выполнен'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_logout(request):
    """Выход администратора"""
    if request.user.username != ADMIN_USERNAME:
        return Response({'error': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)
    
    logout(request)
    return Response({'message': 'Админ вышел'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def game_result(request):
    """Сохранение результата игры"""
    serializer = GameResultSerializer(data=request.data)
    if serializer.is_valid():
        # Создаём запись о результате
        game_result = GameResult.objects.create(
            user=request.user,
            result=serializer.validated_data['result'],
            mines=serializer.validated_data.get('mines', 10)
        )
        
        # Обновляем статистику пользователя
        request.user.total_games += 1
        if serializer.validated_data['result'] == 'win':
            request.user.wins += 1
        request.user.last_game_result = serializer.validated_data['result']
        request.user.save()
        
        return Response({
            'message': 'Результат сохранён',
            'stats': {
                'total_games': request.user.total_games,
                'wins': request.user.wins
            }
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_score(request):
    """Сохранение счёта в таблицу лидеров"""
    serializer = SaveScoreSerializer(data=request.data)
    if serializer.is_valid():
        # Создаём запись в лидерборде
        leaderboard_entry = Leaderboard.objects.create(
            user=request.user,
            mines=serializer.validated_data['mines'],
            time=serializer.validated_data['time']
        )
        
        return Response({
            'message': 'Счёт сохранён в таблицу лидеров',
            'entry': LeaderboardSerializer(leaderboard_entry).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    """Получение таблицы лидеров"""
    # Берём топ-10 результатов
    records = Leaderboard.objects.all().order_by('mines', 'time')[:10]
    serializer = LeaderboardSerializer(records, many=True)
    
    # Преобразуем в формат, ожидаемый фронтендом
    formatted_data = [
        {
            'name': record['username'],
            'mines': record['mines'],
            'time': record['time']
        }
        for record in serializer.data
    ]
    
    return Response(formatted_data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """Получение статистики пользователя"""
    # Получаем рекорды пользователя
    user_records = Leaderboard.objects.filter(user=request.user)
    records_serializer = LeaderboardSerializer(user_records, many=True)
    
    # Статистика игр
    games = GameResult.objects.filter(user=request.user)
    wins = games.filter(result='win').count()
    loses = games.filter(result='lose').count()
    
    return Response({
        'user': UserSerializer(request.user).data,
        'records': records_serializer.data,
        'stats': {
            'total_games': request.user.total_games,
            'wins': request.user.wins,
            'loses': loses,
            'win_rate': round((wins / games.count() * 100) if games.count() > 0 else 0, 1)
        }
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_leaderboard(request):
    """Сброс таблицы лидеров (только для админа)"""
    if request.user.username != ADMIN_USERNAME:
        return Response({'error': 'Только админ может сбрасывать таблицу'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    # Удаляем все записи в лидерборде
    Leaderboard.objects.all().delete()
    
    # Создаём начальные записи (как в script.js)
    initial_data = [
        {'name': 'SHADOW', 'mines': 9, 'time': '42с'},
        {'name': 'VIOLET_M', 'mines': 8, 'time': '55с'},
        {'name': 'NOX', 'mines': 7, 'time': '1:02'},
        {'name': 'FANTOM', 'mines': 6, 'time': '1:20'},
        {'name': 'LUNA', 'mines': 5, 'time': '1:47'}
    ]
    
    for data in initial_data:
        # Создаём временного пользователя для этих записей
        user, _ = User.objects.get_or_create(username=data['name'])
        Leaderboard.objects.create(
            user=user,
            mines=data['mines'],
            time=data['time']
        )
    
    return Response({'message': 'Таблица лидеров сброшена'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_player(request, username):
    """Удаление игрока из лидерборда (только для админа)"""
    if request.user.username != ADMIN_USERNAME:
        return Response({'error': 'Только админ может удалять игроков'}, 
                       status=status.HTTP_403_FORBIDDEN)
    
    try:
        user = User.objects.get(username=username)
        # Удаляем все записи пользователя в лидерборде
        Leaderboard.objects.filter(user=user).delete()
        return Response({'message': f'Игрок {username} удалён из лидерборда'})
    except User.DoesNotExist:
        return Response({'error': 'Игрок не найден'}, status=status.HTTP_404_NOT_FOUND)