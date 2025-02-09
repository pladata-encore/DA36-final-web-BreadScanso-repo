from django.shortcuts import render
from datetime import datetime

from django.template.context_processors import request


def index(request):
    context = {'font_size': '20px'}
    return render(request, "main/index.html")

