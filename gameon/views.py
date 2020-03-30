import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect
from gameon.dto import GameSetting, load_setting
from gameon.models import Game
from .const import *
from .validatior import new_game_validation


def home(request):
    return render(request, 'home.html', {})


def register_user(request):
    username = request.POST['reg-username']
    email = request.POST['reg-email']
    password = request.POST['reg-password']
    try:
        user = User.objects.create_user(username, email, password)
        user.save()
        login(request, user)
    except Exception as e:
        data = {
            'errors': [e],
            'reg_username': username,
            'reg_email': email,
            'reg_password': password,
            'is_registering': True,
        }
        return render(request, 'home.html', data)
    return redirect('/')


def logout_user(request):
    logout(request)
    return redirect('/')


def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        data = {
            'errors': ['Invalid username or password'],
            'username': username,
            'password': password
        }
        return render(request, 'home.html', data)


@login_required(login_url='/')
def create_new_game(request):
    data = {
        'title_len': GAME_TITLE_MIN_MAX_LEN,
        'time_limit_option': TIME_LIMIT_OPTION,
        'answer_count_option': ANSWER_COUNT_OPTION,
        'point_per_question_option': POINT_PER_QUESTION_OPTION,
        'top_rank_option': TOP_RANK_OPTION,
    }
    return render(request, 'new-game.html', data)


@login_required(login_url='/')
def save_new_game(request):
    validation = new_game_validation(request)
    if not validation['ok']:
        data = {
            'title_len': GAME_TITLE_MIN_MAX_LEN,
            'time_limit_option': TIME_LIMIT_OPTION,
            'answer_count_option': ANSWER_COUNT_OPTION,
            'point_per_question_option': POINT_PER_QUESTION_OPTION,
            'top_rank_option': TOP_RANK_OPTION,
            'errors': validation['errors'],
        }
        return render(request, 'new-game.html', data)

    game_title = request.POST['game_title']
    answer_count = int(request.POST['answer_count'])
    time_limit = int(request.POST['time_limit'])
    point_per_question = int(request.POST['point_per_question'])
    top_rank_count = int(request.POST['top_rank_count'])
    game_setting = GameSetting(time_limit, answer_count, point_per_question, top_rank_count)
    setting_json = str(game_setting.__dict__).replace('\'', '\"')

    game = Game()
    game.game_title = game_title
    game.game_setting = setting_json
    game.secret_code = random.randint(1000, 9999)
    game.status = GAME_CREATED
    game.owner = request.user

    game.save()

    return redirect('/')


@login_required(login_url='/')
def save_game(request):
    validation = new_game_validation(request)
    if not validation['ok']:
        return JsonResponse({'error': 'Something went wrong!'})

    game_id = request.POST['game_id']
    game_title = request.POST['game_title']
    answer_count = int(request.POST['answer_count'])
    time_limit = int(request.POST['time_limit'])
    point_per_question = int(request.POST['point_per_question'])
    top_rank_count = int(request.POST['top_rank_count'])
    game_setting = GameSetting(time_limit, answer_count, point_per_question, top_rank_count)
    setting_json = str(game_setting.__dict__).replace('\'', '\"')

    game = Game.objects.get(id=game_id, owner=request.user)
    game.game_title = game_title
    game.game_setting = setting_json

    game.save()

    return JsonResponse({})


@login_required(login_url='/')
def add_question(request):
    return


@login_required(login_url='/')
def edit_question(request):
    return


@login_required(login_url='/')
def your_game(request):
    games = Game.objects.filter(owner=request.user).order_by(F('id').desc())
    i = 1
    for game in games:
        game.index = i
        game.status = GAME_STATUS[game.status]
        i += 1

    return render(request, 'your-game.html', {'games': games})


@login_required(login_url='/')
def game_detail(request, game_id):
    game = Game.objects.get(id=game_id)
    setting = load_setting(game.game_setting)
    data = {
        'title_len': GAME_TITLE_MIN_MAX_LEN,
        'time_limit_option': TIME_LIMIT_OPTION,
        'answer_count_option': ANSWER_COUNT_OPTION,
        'point_per_question_option': POINT_PER_QUESTION_OPTION,
        'top_rank_option': TOP_RANK_OPTION,
        'game': game,
        'setting': setting
    }

    return render(request, 'game-detail.html', data)
