from django.db import models
from django.contrib.auth.models import User
from os.path import join as path_join

def user_avatar_path(instance, filename):
    # Tạo tên tệp hình ảnh dựa trên ID của người dùng
    return path_join('avatars', f'{instance.user.id}', filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_avatar_path, default='avatars/default-avatar.png', blank=True, null=True)
    bio = models.TextField(blank=True)
    library = models.CharField(max_length=255, unique=True) #đây là thư viện lưu trữ hình ảnh của user
    def __str__(self):
        return self.user.username

class Topic(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name
class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    caption = models.TextField(blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    topics = models.ManyToManyField(Topic)
    # Thêm trường để lưu đường dẫn tới hình ảnh trong thư viện của người dùng
    image_path = models.CharField(max_length=255)
    def __str__(self):
        return f"Image by {self.user.username} uploaded on {self.upload_date}"

