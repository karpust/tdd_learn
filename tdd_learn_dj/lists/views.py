from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


# Create your views here.


def home_page(request):

    # if request.method == 'POST':
    #     new_item_text = request.POST['item_text']
    #     Item.objects.create(text=new_item_text)
    # else:
    #     new_item_text = ''
    #
    # return render(request, 'home.html', {
    #     'new_item_text': request.POST.get('item_text', ''),
    # })

    # больше не возвращаем страницу с заполеннными данными,
    # а перенаправляем на домашнюю страницу:
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        # return redirect('/')
    # return render(request, 'home.html')
    items = Item.objects.all()
    # return render(request, 'home.html', {'items': items})
    return redirect('/lists/one_list_in_the_world/')  # пока для одного


def view_list(request):
    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})