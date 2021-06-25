from django.contrib.auth.models import Permission
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate

from expenses_app.settings import LOGIN_REDIRECT_URL
from .forms import UserRegisterForm, UserLoginForm
from django.contrib import messages, auth
from django.core.exceptions import ValidationError
from .models import User, Family, Profile, Role
import re


def register(request):
    families = Family.objects.all()
    roles = Role.objects.all()
    context = {}
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
            if email and not re.match(email_regex, email):
                raise ValidationError('Invalid email format')
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            messages.success(request, f'Account created for {username}!')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            profile = Profile.objects.create(user=request.user)
            profile.save()
            if user.role == "father" or user.role == "grandfather":
                permission = Permission.objects.get(codename="can_view_expenses")
                user.user_permissions.add(permission)
            user.save()
            messages.success(request, 'You are now logged in successfully')
            return redirect(LOGIN_REDIRECT_URL)
        else:
            print(form.errors)
    else:
        form = UserRegisterForm()
        context = {
            'form': form,
            'families': families,
            'roles': roles,
        }

    return render(request, 'account/register.html', context)


def login_view(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect(LOGIN_REDIRECT_URL)
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'You are now logged in successfully')
                return redirect(LOGIN_REDIRECT_URL)
    else:
        form = UserLoginForm()
    context['form'] = form
    return render(request, 'account/login.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect(LOGIN_REDIRECT_URL)

