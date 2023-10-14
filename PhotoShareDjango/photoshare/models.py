from django.db import models
from django.contrib.auth.models import User
from os.path import join as path_join

def user_avatar_path(instance, filename):
    return path_join('avatars', f'{instance.user.id}', filename)

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
    tags = models.ManyToManyField(Tag, blank=True)
    topics = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"Image by {self.user.username} uploaded on {self.upload_date}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=user_avatar_path, default='avatars/default-avatar.png', blank=True, null=True)
    bio = models.TextField(blank=True)
    library = models.ManyToManyField(Image, related_name='user_profiles', blank=True,
                                     null=True)  # Sử dụng ManyToManyField có thể null
    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        if not self.avatar:
            self.avatar = 'avatars/default-avatar.png'
        super().save(*args, **kwargs)
