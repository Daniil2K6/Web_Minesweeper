from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import authenticate as django_authenticate
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token
from .models import User, Leaderboard
from .serializers import (
    UserSerializer, RegisterSerializer, LeaderboardSerializer,
    SaveScoreSerializer
)

ADMIN_USERNAME = "N3XUS_C0R3"

@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    """Получить CSRF токен"""
    token = get_token(request)
    return Response({'csrfToken': token})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Вход пользователя в систему"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Требуется имя пользователя и пароль'}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    user = django_authenticate(username=username, password=password)
    
    if user is not None:
        login(request._request, user)
        role = 'admin' if user.username == ADMIN_USERNAME else 'user'
        
        return Response({
            'message': 'Вход выполнен',
            'user': UserSerializer(user).data,
            'role': role,
            'username': user.username
        }, status=status.HTTP_200_OK)
    
    return Response({'error': 'Неверное имя пользователя или пароль'}, 
                   status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def current_user(request):
    """Получить информацию о текущем пользователе"""
    try:
        user = request.user
        if user and user.id:
            role = 'admin' if user.username == ADMIN_USERNAME else 'user'
            return Response({
                'user': UserSerializer(user).data,
                'role': role,
                'username': user.username,
                'is_authenticated': True
            })
    except Exception as e:
        print(f'Ошибка в current_user: {e}')
    
    return Response({'is_authenticated': False})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Регистрация нового пользователя"""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        role = 'admin' if user.username == ADMIN_USERNAME else 'user'
        login(request._request, user)
        
        return Response({
            'message': 'Регистрация успешна',
            'user': UserSerializer(user).data,
            'role': role,
            'username': user.username
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Выход из системы"""
    logout(request._request)
    return Response({'message': 'Выход выполнен'})

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_logout(request):
    """Выход администратора"""
    if request.user.username != ADMIN_USERNAME:
        return Response({'error': 'Недостаточно прав'}, status=status.HTTP_403_FORBIDDEN)
    
    logout(request._request)
    return Response({'message': 'Админ вышел'})

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_score(request):
    """Сохранение счёта в таблицу лидеров (только если время улучшено)"""
    serializer = SaveScoreSerializer(data=request.data)
    if serializer.is_valid():
        new_time = serializer.validated_data['time']
        
        # Проверяем есть ли уже результат для этого пользователя
        existing = Leaderboard.objects.filter(user=request.user).order_by('time').first()
        
        if existing and existing.time < new_time:
            # Уже есть лучший результат, не сохраняем
            return Response({
                'message': 'Результат не сохранён (уже есть лучший)',
                'best_time': existing.time,
                'new_time': new_time
            }, status=status.HTTP_200_OK)
        
        # Создаём новую запись
        leaderboard_entry = Leaderboard.objects.create(
            user=request.user,
            time=new_time
        )
        
        # Обновляем статистику (только при сохранении нового результата)
        request.user.total_games += 1
        request.user.wins += 1
        request.user.save()
        
        return Response({
            'message': 'Счёт сохранён в таблицу лидеров',
            'entry': LeaderboardSerializer(leaderboard_entry).data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def leaderboard(request):
    """Получение таблицы лидеров (топ-100)"""
    records = Leaderboard.objects.all().order_by('time')[:100]
    serializer = LeaderboardSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    """Получение статистики пользователя"""
    user_records = Leaderboard.objects.filter(user=request.user).order_by('time')
    records_serializer = LeaderboardSerializer(user_records, many=True)
    
    return Response({
        'user': UserSerializer(request.user).data,
        'records': records_serializer.data,
        'stats': {
            'total_games': request.user.total_games,
            'wins': request.user.wins,
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
    
    # Создаём начальные записи
    initial_data = [
        {'name': 'SHADOW', 'time': 42.510},
        {'name': 'VIOLET_M', 'time': 55.320},
        {'name': 'NOX', 'time': 62.150},
        {'name': 'FANTOM', 'time': 80.450},
        {'name': 'LUNA', 'time': 107.890}
    ]
    
    for data in initial_data:
        user, _ = User.objects.get_or_create(username=data['name'])
        Leaderboard.objects.create(
            user=user,
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
        Leaderboard.objects.filter(user=user).delete()
        return Response({'message': f'Игрок {username} удалён из лидерборда'})
    except User.DoesNotExist:
        return Response({'error': 'Игрок не найден'}, status=status.HTTP_404_NOT_FOUND)