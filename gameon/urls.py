from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-user', views.register_user, name='register-user'),
    path('logout', views.logout_user, name='logout'),
    path('login', views.login_user, name='login'),
]
