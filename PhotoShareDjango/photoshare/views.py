import os
from typing import Any

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, FileResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView, ListView

from rest_framework import viewsets, permissions
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from django.urls import reverse_lazy, reverse

from .forms import ImageUploadForm, TagForm, SearchForm, TopicForm

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
    images = Image.objects.order_by('-upload_date')
    topics = Topic.objects.all()
    context = {
        'images': images,
        'topics': topics,
    }
    return render(req, 'home.html', context)


class HomeView(ListView):
    model = Image  # Model bạn muốn hiển thị
    template_name = 'home.html'  # Template bạn muốn sử dụng
    context_object_name = 'images'  # Tên biến context cho danh sách dữ liệu
    ordering = ['-upload_date']  # Sắp xếp theo ngày tải lên (mặc định)

    # Số lượng hình ảnh trên mỗi trang
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context
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
# @login_required
# @csrf_exempt
# def upload_image(request):
#     if request.method == 'POST' and request.FILES:
#         uploaded_file = request.FILES['file']
#         user = request.user
#
#         # Đảm bảo thư mục lưu trữ tồn tại
#         storage_dir = os.path.join(settings.MEDIA_ROOT, 'uploads', str(user.id))
#         os.makedirs(storage_dir, exist_ok=True)
#
#         # Lưu tệp vào thư mục lưu trữ
#         file_path = os.path.join(storage_dir, uploaded_file.name)
#         with open(file_path, 'wb+') as destination:
#             for chunk in uploaded_file.chunks():
#                 destination.write(chunk)
#
#         # Trả về một JSON response cho client
#         response_data = {'message': 'Hình ảnh đã được tải lên thành công.'}
#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({'error': 'Yêu cầu không hợp lệ.'})
# @login_required
# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Gán người dùng hiện tại cho hình ảnh trước khi lưu vào cơ sở dữ liệu
#             image = form.save(commit=False)
#             image.user = request.user
#             image.save()
#             request.user.userprofile.library.add(image)
#             image_url = image.image.url
#
#             # Trả về đường dẫn ảnh bằng JsonResponse
#             response_data = {'image_url': image_url}
#             return JsonResponse(response_data)
#     else:
#         form = ImageUploadForm()
#     return render(request, 'upload_image.html', {'form': form})
@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user  # Gán người dùng hiện tại cho hình ảnh
            image.save()
            image.tags.set(form.cleaned_data['tags'])
            form.save_m2m()
            request.user.userprofile.library.add(image)  # Thêm hình ảnh vào thư viện của người dùng
            return redirect('home')  # Chuyển hướng người dùng sau khi tải lên thành công
    else:
        form = ImageUploadForm()

    return render(request, 'upload_image.html', {'form': form})
def topic_detail(request, topic_id):
    # Lấy thông tin chủ đề hoặc trả về 404 nếu không tìm thấy
    topic = get_object_or_404(Topic, pk=topic_id)

    # Lấy danh sách các ảnh thuộc chủ đề đó
    images = Image.objects.filter(topics=topic)

    return render(request, 'topic_detail.html', {'topic': topic, 'images': images})
def image_detail(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    tags = image.tags.all()
    try:
        topics = image.topics.all()
    except AttributeError:
        topics = []
    tag_names = [tag.name for tag in tags]
    topic_names = [topic.name for topic in topics]
    images_with_same_tag = Image.objects.filter(tags__name__in=tag_names).exclude(id=image_id)
    images_with_same_topic = Image.objects.filter(topics__name__in=topic_names).exclude(id=image_id)

    return render(request, 'image_detail.html', {
        'image': image,
        'tags': tags,
        'topics': topics,
        'images_with_same_tag': images_with_same_tag,
        'images_with_same_topic': images_with_same_topic
    })


@login_required  # Đảm bảo người dùng đã đăng nhập để sử dụng tính năng này
def save_image_to_library(request, image_id):
    # Lấy đối tượng ảnh từ cơ sở dữ liệu
    image = get_object_or_404(Image, pk=image_id)

    # Kiểm tra nếu ảnh đã tồn tại trong thư viện của người dùng thì không thêm nữa
    if not request.user.userprofile.library.filter(pk=image_id).exists():
        # Thêm ảnh vào thư viện của người dùng
        request.user.userprofile.library.add(image)

    return redirect('image_detail', image_id=image_id)
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
def create_topics(request):
    topics = Topic.objects.all()  # Lấy danh sách các topic hiện có
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('create_topics')  # Chuyển hướng trang sau khi tạo topic thành công
    else:
        form = TopicForm()

    return render(request, 'create_topics.html', {'topics': topics, 'form': form})
@method_decorator(login_required, name='dispatch')
class EditUserProfile(UpdateView):
    model = UserProfile
    fields = ['user', 'avatar', 'bio']
    template_name = 'edit_user_profile.html'
    success_url = reverse_lazy('user_profile_detail')
@login_required
def view_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        image_id = request.POST.get('image_id')
        image_to_add = Image.objects.get(pk=image_id)
        user_profile.library.add(image_to_add)
        return HttpResponse(status=200)
    images = user_profile.library.all().order_by('-upload_date')
    username = user_profile.user.username
    user = User.objects.get(username=username)
    image_upload = Image.objects.filter(user=user).order_by('-upload_date')

    return render(request, 'profile.html', {'user_profile': user_profile, 'images': images,'images_upload':image_upload})
class UpdateProfile(UpdateView):
    model = UserProfile
    fields = ['avatar']
    template_name = 'update_profile.html'
    success_url = reverse_lazy('view_profile')

    def form_valid(self, form):
        super(UpdateProfile, self).form_valid(form)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', reverse('view_profile')))
def search_images(request):
    form = SearchForm(request.GET)
    images = Image.objects.order_by('-upload_date')

    if form.is_valid():
        search_query = form.cleaned_data['search_query']
        tag = form.cleaned_data['tag']
        topic = form.cleaned_data['topic']

        if search_query:
            images = images.filter(caption__icontains=search_query)

        if tag:
            images = images.filter(tags__name__icontains=tag)

        if topic:
            images = images.filter(topics__name__icontains=topic)

    return render(request, 'search_results.html', {'form': form, 'images': images})
def download_image(request, image_id):
    image = get_object_or_404(Image, pk=image_id)
    image_file = image.image.file
    response = FileResponse(image_file, as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{image_file.name}"'
    return response

@login_required
def remove_image_from_library(request, image_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    image = get_object_or_404(Image, id=image_id)

    if image in user_profile.library.all():
        user_profile.library.remove(image)
        user_profile.save()
        return redirect('view_profile')

    else:
        return redirect('view_profile')
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    images = Image.objects.filter(topics=topic)
    if not images:
        return render(request, 'topic_detail.html',
                      {'message': 'Không có hình ảnh nào trong topic này.', 'topic': topic, 'images': []})

    return render(request, 'topic_detail.html', {'topic': topic, 'images': images})

