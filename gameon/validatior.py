from gameon.const import *
from gameon.dto import load_setting
from gameon.models import Game


def new_game_validation(request):
    ret = True
    err = []

    game_title = request.POST['game_title']
    if not GAME_TITLE_MIN_MAX_LEN['max'] > len(game_title) > GAME_TITLE_MIN_MAX_LEN['min']:
        err.append('Length of game title is invalid')
        ret = False
    answer_count = int(request.POST['answer_count'])
    if answer_count not in ANSWER_COUNT_OPTION['option']:
        err.append('Number of answer is out of scope')
        ret = False
    time_limit = int(request.POST['time_limit'])
    if time_limit not in TIME_LIMIT_OPTION['option']:
        err.append('Time limit is out of scope')
        ret = False
    point_per_question = int(request.POST['point_per_question'])
    if point_per_question not in POINT_PER_QUESTION_OPTION['option']:
        err.append('Point per question is out of scope')
        ret = False
    top_rank_count = int(request.POST['top_rank_count'])
    if top_rank_count not in TOP_RANK_OPTION['option']:
        err.append('Top rank is out of scope')
        ret = False

    return {'ok': ret, 'errors': err}


def save_question_validation(request):
    ret = True
    err = []

    game_id = request.POST['game_id']
    game = Game.objects.get(id=game_id, owner=request.user)
    if game is None:
        ret = False
        return {'ok': ret, 'errors': 'You don\'t have permission'}

    setting = load_setting(game.game_setting)

    question = request.POST.get('question', '')
    if len(question) < 1:
        ret = False
        err.append('Question is empty')

    for i in range(1, setting.answer_count+1):
        answer = request.POST.get('answer-' + str(i), '')
        if len(answer) < 1:
            ret = False
            err.append('Answer ' + str(i) + ' is empty')

    true_answer = request.POST.get('true-answer', False)
    if not true_answer:
        ret = False
        err.append('Check a true answer')

    return {'ok': ret, 'errors': err}
