from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from photoshare.models import UserProfile


def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('images')

        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {username.title()}, welcome back!')

                # Kiểm tra xem UserProfile đã tồn tại cho người dùng này chưa
                if not UserProfile.objects.filter(user=user).exists():
                    # Nếu không tồn tại, tạo mới UserProfile
                    UserProfile.objects.create(user=user, library='default')

                return redirect('images')

        # form is not valid or user is not authenticated
            return render(request, 'login.html', {'form': form})
def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login')
def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            # Tạo UserProfile cho người dùng mới đăng ký
            UserProfile.objects.create(user=user, library='default')

            messages.success(request, 'You have signed up successfully.')
            login(request, user)
            return redirect('images')
        else:
            return render(request, 'register.html', {'form': form})
