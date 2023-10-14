from django import forms
from .models import Image, Topic
from .models import Tag

class ImageUploadForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    caption = forms.CharField(
        max_length=255,
        required=True,
    )
    class Meta:
        model = Image
        fields = ['image','caption','tags','topics']
    def clean(self):
        cleaned_data = super().clean()
        tags = cleaned_data.get('tags')
        caption = cleaned_data.get('caption')
        if not tags:
            self.add_error('tags', 'Tag không được để trống.')
        if not caption:
            self.add_error('caption', 'Caption không được để trống.')
        return cleaned_data
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']
class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ['name']
class AvatarUploadForm(forms.Form):
    avatar = forms.ImageField()
class SearchForm(forms.Form):
    search_query = forms.CharField(label='Tìm kiếm', max_length=100, required=False)
    tag = forms.CharField(max_length=50, required=False)
    topic = forms.CharField(max_length=100, required=False)