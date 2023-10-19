from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from .forms import LoginForm, RegisterForm, ChangePasswordForm
from photoshare.models import UserProfile,Image



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
            user_profile = UserProfile.objects.create(user=user)

            default_image = Image.objects.get(name='default')  # Thay bằng truy vấn thích hợp
            user_profile.library.add(default_image)

            messages.success(request, 'You have signed up successfully.')
            login(request, user)
            return redirect('images')
        else:
            return render(request, 'register.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user = request.user
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)  # Đảm bảo phiên đăng nhập còn hiệu lực
                return redirect('view_profile')  # Chuyển hướng đến trang thông tin cá nhân
            else:
                form.add_error('old_password', 'Mật khẩu cũ không đúng')
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'form': form})