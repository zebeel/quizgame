from gameon.const import *


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
