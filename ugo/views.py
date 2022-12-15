from django.shortcuts import render, redirect
from .models import *
from user.models import *
from .forms import *
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import View
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from datetime import datetime


# Create your views here.
@login_required
def home(request):
    user = request.user
    return render(request, 'home.html', {'user': user})

def logout(request):
    django_logout(request)
    return redirect('login')

class Login(LoginView):
    model = Usuario
    template_name = 'login/login.html'