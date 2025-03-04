from django import forms
from django_summernote.widgets import SummernoteWidget
from django_summernote.fields import SummernoteTextField
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'pinned']
        widgets = {
            'content': SummernoteWidget(),
        }