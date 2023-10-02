import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import UpdateView

from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from django.urls import reverse_lazy

from .forms import ImageUploadForm, TagForm, SearchForm

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
def home(req):
    images = Image.objects.all()
    topics = Topic.objects.all()
    context = {
        'images': images,
        'topics': topics,
    }
    return render(req, 'home.html', context)


class HomeView(View):
    template_name = 'home.html'
    def get(self, request):
        # Lấy danh sách tất cả hình ảnh và chủ đề
        images = Image.objects.all()
        topics = Topic.objects.all()

        context = {
            'images': images,
            'topics': topics,
        }

        return render(request, 'home.html', context)
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
class ImageUploadView(CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
class ViewImageView(View):
    def get(self, request, image_id):
        image = Image.objects.get(pk=image_id)
        return render(request, 'view_image.html', {'image': image})

# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('success_page')  # Chuyển hướng đến trang thành công sau khi tải lên
#     else:
#         form = ImageUploadForm()
#     return render(request, 'upload_image.html', {'form': form})
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save()  # Lưu dữ liệu vào cơ sở dữ liệu
            image_url = uploaded_image.image.url
            response_data = {'image_url': image_url}
            return JsonResponse(response_data)
    else:
        form = ImageUploadForm()
    return render(request, 'upload_image.html', {'form': form})
def get_image(request, image_name):
    # Xác định đường dẫn tới tệp ảnh trong thư mục media
    image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_name)

    try:
        # Mở tệp ảnh và đọc dữ liệu
        with open(image_path, 'rb') as image_file:
            response = HttpResponse(image_file.read(), content_type='image/jpeg')
            return response
    except FileNotFoundError:
        # Trả về 404 nếu tệp ảnh không tồn tại
        return HttpResponse(status=404)

def create_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'create_tag.html', {'form': form})
def success_page(request):
    return render(request, 'success_page.html')
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html', {'tags': tags})

@method_decorator(login_required, name='dispatch')
class MyAccount(UpdateView):
  model = User
  fields = ('first_name', 'last_name', 'email', )
  template_name = 'my_account.html'
  success_url = reverse_lazy('my_account')

  def get_object(self):
    return self.request.user


def search_images(request):
    form = SearchForm(request.GET)
    images = Image.objects.all()

    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        tag = form.cleaned_data['tag']
        topic = form.cleaned_data['topic']

        if search_query:
            images = images.filter(title__icontains=search_query)

        if tag:
            images = images.filter(tags__name__icontains=tag)

        if topic:
            images = images.filter(topics__name__icontains=topic)

    return render(request, 'search_results.html', {'form': form, 'images': images})
def topic():
    return None