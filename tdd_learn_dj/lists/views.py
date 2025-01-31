from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


# Create your views here.


def home_page(request):
    return render(request, 'home.html')


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    """новый список"""
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/one_list_in_the_world/')