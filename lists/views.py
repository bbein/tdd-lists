"""
Homepage Views for the list App
"""

from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.forms import ItemForm

def home_page(request):
    """
    The main homepage view
    """
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    """
    View to look at a to-do list of one user
    """
    list_ = List.objects.get(id=list_id)
    form = ItemForm()
    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            item = Item(text=request.POST['text'], list=list_)
            item.save()
            return redirect(list_)
    return render(request, 'list.html', {
        'list': list_, 'form': form
    })

def new_list(request):
    """
    View to create a new list
    """
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        Item.objects.create(text=request.POST['text'], list=list_)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})

