import json


def load_setting(setting):
    json_setting = json.loads(setting)
    time_limit = json_setting['time_limit']
    answer_count = json_setting['answer_count']
    point_per_question = json_setting['point_per_question']
    top_rank_count = json_setting['top_rank_count']

    return GameSetting(time_limit, answer_count, point_per_question, top_rank_count)


class GameSetting:
    def __init__(self, tl, ac, ppq, trc):
        self.time_limit = tl
        self.answer_count = ac
        self.point_per_question = ppq
        self.top_rank_count = trc
