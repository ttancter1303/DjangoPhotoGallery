from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from . import views
from .views import  UserProfileView, ViewImageView, UserViewSet, ImageViewSet, TagViewSet, TopicViewSet, \
    UserProfileViewSet, ImageUploadView, MyAccount, topic

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
    path('topics',views.topic,name = 'topics'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    # path('image/<int:image_id>/', ViewImageView.as_view(), name='view_image'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('upload/', views.upload_image, name='upload_image'),
    path('success/', views.success_page, name='success_page'),
    path('create_tag/', views.create_tag, name='create_tag'),
    path('tag_list/', views.tag_list, name='tag_list'),
    path('account/',MyAccount.as_view(),name = 'my_account'),
    path('search/', views.search_images, name='search_images'),
    path('topics/', views.create_topics, name='create_topics'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

