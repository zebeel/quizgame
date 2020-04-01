import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect
from gameon.dto import GameSetting, load_setting
from gameon.models import Game, GameQuestion, QuestionOption
from .const import *
from .validatior import new_game_validation, save_question_validation


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
def save_question(request):
    validator = save_question_validation(request)
    if not validator['ok']:
        return JsonResponse({'errors': validator['errors']})

    game_id = request.POST['game_id']

    game = Game.objects.get(id=game_id, owner=request.user)

    if game is None:
        return JsonResponse({'errors': ['No permission for this game']})

    if game.status not in EDITABLE_STATUS:
        return JsonResponse({'errors': ['Something went wrong!']})

    question = GameQuestion()
    question_id = request.POST.get('question-id', 0)
    if int(question_id) > 0:
        question = GameQuestion.objects.get(id=question_id, game_id=game_id)
        if question is None:
            return JsonResponse({'errors': ['No permission for this question']})
    question.game_id = game_id
    question.question = request.POST.get('question', '')
    question.true_answer_number = request.POST.get('true-answer', False)
    question.is_bonus = request.POST.get('bonus-question', False) is not False
    question.save()

    setting = load_setting(game.game_setting)
    for i in range(1, setting.answer_count+1):
        answer = request.POST.get('answer-' + str(i), '')
        question_option = QuestionOption()
        if int(question_id) > 0:
            question_option = QuestionOption.objects.get(question_id=question_id, answer_number=i)
        question_option.question_id = question.id
        question_option.answer_number = i
        question_option.answer_content = answer
        question_option.save()

    game.status = GAME_READY
    game.save()

    return JsonResponse({'id': question.id})


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
    game = Game.objects.get(id=game_id, owner=request.user)
    if game is None:
        return redirect('/')

    err = []
    if request.method == 'POST':
        err = save_game(request)

    setting = load_setting(game.game_setting)

    disabled = 'disabled'
    if game.status in EDITABLE_STATUS:
        disabled = ''

    questions = GameQuestion.objects.filter(game_id=game_id)

    data = {
        'title_len': GAME_TITLE_MIN_MAX_LEN,
        'time_limit_option': TIME_LIMIT_OPTION,
        'answer_count_option': ANSWER_COUNT_OPTION,
        'point_per_question_option': POINT_PER_QUESTION_OPTION,
        'top_rank_option': TOP_RANK_OPTION,
        'game': game,
        'setting': setting,
        'answer_count_range': range(1, setting.answer_count + 1),
        'disabled': disabled,
        'EDITABLE_STATUS': EDITABLE_STATUS,
        'errors': err,
        'questions': questions,
    }

    return render(request, 'game-detail.html', data)


def save_game(request):
    validation = new_game_validation(request)
    if not validation['ok']:
        return validation['errors']

    game_id = request.POST['game_id']

    game = Game.objects.get(id=game_id, owner=request.user)
    if game.status not in EDITABLE_STATUS:
        return ['Something went wrong!']

    setting = load_setting(game.game_setting)

    game_title = request.POST['game_title']
    time_limit = int(request.POST['time_limit'])
    point_per_question = int(request.POST['point_per_question'])
    top_rank_count = int(request.POST['top_rank_count'])

    game_setting = GameSetting(time_limit, setting.answer_count, point_per_question, top_rank_count)
    setting_json = str(game_setting.__dict__).replace('\'', '\"')

    game.game_title = game_title
    game.game_setting = setting_json

    game.save()

    return []


def get_question(request):
    game_id = request.POST['game_id']
    question_id = request.POST['question_id']
    game = Game.objects.get(id=game_id, owner=request.user)
    if game is None:
        return JsonResponse({'errors': ['No permission for this game']})

    question = GameQuestion.objects.get(game_id=game_id, pk=question_id)

    if question is None:
        return JsonResponse({'errors': ['No question exists']})

    answers = QuestionOption.objects.filter(question_id=question_id)

    data = {
        'question': question.question,
        'true_answer': question.true_answer_number,
        'is_bonus': question.is_bonus,
        'answers': serializers.serialize('python', answers),
    }

    return JsonResponse(data)
