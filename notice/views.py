from django.shortcuts import render, get_object_or_404, redirect
from django import forms
from .models import Notice

def notice_main(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'notice/notice_main.html', {'notices': notices})

def notice_detail(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    return render(request, 'notice/notice_detail.html', {'notice': notice})

def notice_delete(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.delete()
    return redirect('notice_main')

class NoticeForm(forms.ModelForm):  # forms.py 대신 views.py에 직접 선언
    class Meta:
        model = Notice
        fields = ['title', 'content']

def notice_create(request):
    if request.method == "POST":
        form = NoticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notice_main')
    else:
        form = NoticeForm()
    return render(request, 'notice/notice_form.html', {'form': form})
