from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path("login/", auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.sign_up, name='sign_up'),
    path('change_password/', views.change_password, name='change_password'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]