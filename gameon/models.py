from django.db import models


class Player(models.Model):
    player_name = models.CharField(max_length=20)
    secret_string = models.CharField(max_length=10)
    mac_add = models.CharField(max_length=20)


class Game(models.Model):
    game_title = models.TextField()
    game_setting = models.TextField()
    secret_code = models.CharField(max_length=4)
    status = models.IntegerField()


class GameQuestion(models.Model):
    game_id = models.BigIntegerField()
    question = models.TextField()
    true_answer_number = models.IntegerField()
    start_timestamp = models.IntegerField()
    is_surprise = models.BooleanField()


class QuestionOption(models.Model):
    game_question_id = models.BigIntegerField()
    answer_number = models.IntegerField()
    answer_content = models.TextField()


class PlayerGame(models.Model):
    player_id = models.BigIntegerField()
    game_id = models.BigIntegerField()


class PlayerAnswer(models.Model):
    game_id = models.BigIntegerField()
    game_question_id = models.BigIntegerField()
    answer_number = models.IntegerField()
    thinking_time = models.IntegerField()
