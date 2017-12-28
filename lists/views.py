"""
Homepage Views for the list App
"""

from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from lists.models import Item, List
from lists.forms import ItemForm, ExistingListItemForm

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
    form = ExistingListItemForm(for_list=list_)
    if request.method == "POST":
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            form.save(list_)
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
        form.save(list_)
        return redirect(list_)
    return render(request, 'home.html', {'form': form})

