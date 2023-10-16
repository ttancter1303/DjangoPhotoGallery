from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views
from .views import UserProfileView, ViewImageView, UserViewSet, ImageViewSet, TagViewSet, TopicViewSet, \
    UserProfileViewSet, ImageUploadView, EditUserProfile, remove_image_from_library

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'images', ImageViewSet)
router.register(r'tags',TagViewSet)
router.register(r'topics',TopicViewSet)
router.register(r'userprofiles',UserProfileViewSet)


from django.urls import path
from .views import  UserProfileView, ViewImageView

urlpatterns = [
    path('', views.home, name='home'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('upload/', views.upload_image, name='upload_image'),
    path('success/', views.success_page, name='success_page'),
    path('create_tag/', views.create_tag, name='create_tag'),
    path('tag_list/', views.tag_list, name='tag_list'),
    path('remove_image/<int:image_id>/', remove_image_from_library, name='remove_image_from_library'),
    path('profile/update_avatar/', views.UpdateProfile.as_view(), name='update_avatar'),
    path('search/', views.search_images, name='search_images'),
    path('topics/', views.create_topics, name='create_topics'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
    path('download/<int:image_id>/', views.download_image, name='download_image'),
    path('profile/', views.view_profile, name='view_profile'),
    path('profile/edit_profile/<int:pk>/', EditUserProfile.as_view(), name='edit_user_profile'),
    path('save_image_to_library/<int:image_id>/', views.save_image_to_library, name='save_image_to_library'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

