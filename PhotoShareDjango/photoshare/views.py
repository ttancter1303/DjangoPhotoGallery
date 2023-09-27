from django.shortcuts import render
from django.views import View

from rest_framework import viewsets, permissions
from django.contrib.auth.models import User

from .models import Image, UserProfile, Topic, Tag
from .serializers import ImageSerializer, UserSerializer, TopicSerializer,UserProfileSerializer,TagSerializer


#
# class HomeView(View):
#     model = ChuDe
#     context_object_name = 'ccd'
#     template_name = 'cac_chu_de.html'
#     paginate_by = 10
#     def get(self, request):
#         images = Image.objects.all()
#         return render(request, 'home.html', {'images': images})

class HomeView(View):
    def get(self, request):
        # Lấy danh sách tất cả hình ảnh và chủ đề
        images = Image.objects.all()
        topics = Topic.objects.all()

        context = {
            'images': images,
            'topics': topics,
        }

        return render(request, 'home.html', context)

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

#     Class Viewset
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    
class ViewImageView(View):
    def get(self, request, image_id):
        image = Image.objects.get(pk=image_id)
        return render(request, 'view_image.html', {'image': image})
