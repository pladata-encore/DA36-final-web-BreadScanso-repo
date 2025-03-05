from django import forms
from django_summernote.widgets import SummernoteWidget
from .models import Notice

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['pinned', 'title', 'content']
        widgets = {
            'content': SummernoteWidget(),
        }