from django import forms
from .models import Image, Topic
from .models import Tag

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image','caption','tags','topics']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

class SearchForm(forms.Form):
    search_query = forms.CharField(label='Tìm kiếm', max_length=100, required=False)
    tag = forms.CharField(max_length=50, required=False)
    topic = forms.CharField(max_length=100, required=False)