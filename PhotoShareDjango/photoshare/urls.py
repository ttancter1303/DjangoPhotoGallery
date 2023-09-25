from django.urls import path
from .views import HomeView, UserProfileView, ViewImageView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('image/<int:image_id>/', ViewImageView.as_view(), name='view_image'),

]
