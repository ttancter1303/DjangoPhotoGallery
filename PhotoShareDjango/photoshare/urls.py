from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from .views import HomeView, UserProfileView, ViewImageView, UserViewSet,ImageViewSet,TagViewSet,TopicViewSet,UserProfileViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'images', ImageViewSet)
router.register(r'tags',TagViewSet)
router.register(r'topics',TopicViewSet)
router.register(r'userprofiles',UserProfileViewSet)


from django.urls import path
from .views import HomeView, UserProfileView, ViewImageView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user_profile'),
    path('image/<int:image_id>/', ViewImageView.as_view(), name='view_image'),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

