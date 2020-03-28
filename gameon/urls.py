from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-user', views.register_user, name='register-user'),
    path('logout', views.logout_user, name='logout'),
    path('login', views.login_user, name='login'),
    path('create-new-game', views.create_new_game, name='create-new-game'),
    path('save-new-game', views.save_new_game, name='save-new-game'),
    path('add-question', views.add_question, name='add-question'),
    path('save-question', views.save_question, name='save-question'),
]
