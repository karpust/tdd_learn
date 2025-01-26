from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home_page(request):
    # return HttpResponse('<html lang="en"><head><meta charset="UTF-8"><title>To-Do lists</title><h1>To-Do</h1>inputbox</head></html>')
    return render(request, 'home.html')  # создаст HttpResponse
