from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # django can create forms for us
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.
def home(request):
    return render(request, 'login/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'login/signupuser.html', {'form': UserCreationForm()})
    else:
        # Create new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentpage')
                
            except IntegrityError:
                return render(request, 'login/signupuser.html', {'form': UserCreationForm(), 'error': 'Username already taken'})

        else:
            return render(request, 'login/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords do not match'})
            # Tell user passwords dont match

def currentpage(request):
    return render(request, 'login/current.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'login/login.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        # if no user exist will be none
        if user is None:
            return render(request, 'login/login.html', {'form': AuthenticationForm(), 'error': 'Username and Password do not match'})
        else:
            login(request, user)
            return redirect('currentpage')


def logoutuser(request):
    # chrome preloads all links in background. <a> is a get request so check for only when post
    if request.method == 'POST':
        logout(request)
        return redirect('home')
