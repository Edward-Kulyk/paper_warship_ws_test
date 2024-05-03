from django.shortcuts import render, redirect
from django.conf import settings
import json
import redis
from django.http import HttpResponseBadRequest
import uuid
from datetime import datetime



def home(request):
    return render(request, 'home.html')


def new_game(request):
    if request.method == 'POST':
        player = request.POST.get('player_name', 'serega')
        if player:
            game_id = create_game(player)
            if game_id:
                response = redirect('game', game_id=game_id)
                response.set_cookie('player', player)  # Устанавливаем имя игрока в куки
                return response
            else:
                return HttpResponseBadRequest("Failed to create game.")
        else:
            return HttpResponseBadRequest("Player name is required.")
    else:
        return render(request, 'home.html', {})


def join_game(request):
    if request.method == 'POST':
        player = request.POST.get('player_name', "biba")
        game_id = request.POST.get('game_id', "d78e1428-3eca-4d27-88f2-ef5c93d0e56f")
        if player and game_id:
            game_data = get_game_from_redis(game_id)
            if game_data:
                if game_data['player1'] and not game_data['player2']:
                    success = set_player2(game_id, player)
                    if success:
                        response = redirect('game', game_id=game_id)
                        response.set_cookie('player', player)
                        return response
                    else:
                        return HttpResponseBadRequest("Failed to join game.")
                elif game_data['player2'] and not game_data['player1']:

                    return HttpResponseBadRequest("Failed to join game.")
                else:
                    return HttpResponseBadRequest("Game is full.")
            else:
                return HttpResponseBadRequest("Game not found.")
        else:
            return HttpResponseBadRequest("Player name and game ID are required.")
    else:
        return HttpResponseBadRequest("Invalid request method.")


def create_game(player_name):
    # Генерируем уникальный идентификатор для игры
    game_id = str(uuid.uuid4())

    # Сохраняем данные об игре в Redis
    redis_conn = redis.Redis(host=settings.GAME_REDIS_HOST, port=settings.GAME_REDIS_PORT, db=settings.GAME_REDIS_DB)
    game_data = {
        'game_id': game_id,
        'status': 'wait_for_second_player',
        'created_at': str(datetime.now()),
        'player1': player_name,
        'player2': None
    }
    redis_conn.set('game:' + game_id, json.dumps(game_data))

    return game_id


def get_game_from_redis(game_id):
    redis_conn = redis.Redis(host=settings.GAME_REDIS_HOST, port=settings.GAME_REDIS_PORT, db=settings.GAME_REDIS_DB)
    game_data = redis_conn.get('game:' + game_id)
    if game_data:
        return json.loads(game_data)
    else:
        return None


def set_player2(game_id, player_name):
    redis_conn = redis.Redis(host=settings.GAME_REDIS_HOST, port=settings.GAME_REDIS_PORT, db=settings.GAME_REDIS_DB)
    game_data = redis_conn.get('game:' + game_id)
    if game_data:
        game_data = json.loads(game_data)
        game_data['player2'] = player_name
        redis_conn.set('game:' + game_id, json.dumps(game_data))
        return True
    else:
        return False


def game(request, game_id):
    player = request.COOKIES.get('player', None)
    # Ваш код здесь для обработки страницы игры
    game_data = get_game_from_redis(game_id)
    if player == game_data["player1"]:
        opponent = game_data["player2"]
    else:
        opponent = game_data["player1"]
    return render(request, 'game.html', {'game_id': game_id, 'player': player, 'opponent':opponent})