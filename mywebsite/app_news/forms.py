from django import forms
from app_news.models import Comment


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    to = forms.EmailField()
    comment = forms.CharField(widget=forms.Textarea, required=False)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
