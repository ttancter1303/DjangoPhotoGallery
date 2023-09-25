from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')
    bio = models.TextField(blank=True)
    library = models.CharField(max_length=255, unique=True) #đây là thư viện lưu trữ hình ảnh của user
    def __str__(self):
        return self.user.username

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
    # Thêm trường để lưu đường dẫn tới hình ảnh trong thư viện của người dùng
    image_path = models.CharField(max_length=255)
    def __str__(self):
        return f"Image by {self.user.username} uploaded on {self.upload_date}"


