from django.shortcuts import render
from django.views import View

from .models import Image, UserProfile


class HomeView(View):
    def get(self, request):
        images = Image.objects.all()
        return render(request, 'home.html', {'images': images})


class UserProfileView(View):
    def get(self, request, username):
        user_profile = UserProfile.objects.get(user__username=username)
        images = Image.objects.filter(user=user_profile.user)
        return render(request, 'user_profile.html', {'user_profile': user_profile, 'images': images})

    
class ViewImageView(View):
    def get(self, request, image_id):
        image = Image.objects.get(pk=image_id)
        return render(request, 'view_image.html', {'image': image})