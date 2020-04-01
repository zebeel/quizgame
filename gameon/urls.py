from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-user', views.register_user, name='register-user'),
    path('logout', views.logout_user, name='logout'),
    path('login', views.login_user, name='login'),
    path('create-new-game', views.create_new_game, name='create-new-game'),
    path('save-new-game', views.save_new_game, name='save-new-game'),
    # path('save-game', views.save_game, name='save-game'),
    path('save-question', views.save_question, name='save-question'),
    path('get-question', views.get_question, name='get-question'),
    path('your-game', views.your_game, name='your-game'),
    path('game-detail/<int:game_id>', views.game_detail, name='game-detail'),
]
