from django import forms
from .models import Image
from .models import Tag

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['user','image','caption','tags','topics','image_path']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
