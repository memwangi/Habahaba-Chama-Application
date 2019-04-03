from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Member
from .forms import RegisterForm
from django.conf import settings


def index(request):
    return render(request, '')


def homepage(request):
    return render(request, 'chama/home_view.html')


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=email, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'chama/register.html', {'form': form})
