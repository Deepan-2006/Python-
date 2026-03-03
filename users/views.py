from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            messages.success(request, f'Account created for {user.username}! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Try to authenticate with the identifier as username
            user = authenticate(username=identifier, password=password)
            
            # If failed, try to find a user with this email and authenticate with their username
            if user is None and '@' in identifier:
                try:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user_obj = User.objects.get(email=identifier)
                    user = authenticate(username=user_obj.username, password=password)
                except (User.DoesNotExist, User.MultipleObjectsReturned):
                    pass


            if user is not None:
                if getattr(user, 'is_locked', False):
                    messages.error(request, 'Your account is locked due to multiple failed attempts.')
                else:
                    login(request, user)
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email/username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {
        'u_form': u_form,
        'p_form': p_form
    })

