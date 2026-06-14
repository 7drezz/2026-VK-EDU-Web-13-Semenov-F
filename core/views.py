from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
from .forms import LoginForm, RegisterForm, ProfileForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('questions:index')

    next_url = request.GET.get('next', '')

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request, username=username, password=password)

            if user:
                auth.login(request, user)
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('questions:index')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form, 'next': next_url})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('questions:index')

    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            return redirect('questions:index')
    else:
        form = RegisterForm()

    return render(request, 'core/signup.html', {'form': form})


def logout_view(request):
    next_url = request.GET.get('next', request.META.get('HTTP_REFERER', reverse('questions:index')))
    auth.logout(request)
    return redirect(next_url)


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('core:profile')
    else:
        form = ProfileForm(user=request.user)

    return render(request, 'core/profile.html', {'form': form})