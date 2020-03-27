from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# @login_required
def home(request):
    # user = User.objects.create_user('beel', 'beel@gmail.com', 'beel')
    # user.save()

    # user = authenticate(request, username='beel', password='beel')
    # login(request, user)
    # print(request.user.is_authenticated)
    # logout(request)

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
