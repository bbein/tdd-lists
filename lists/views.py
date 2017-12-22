"""
Homepage Views for the list App
"""

from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from lists.models import Item, List

def home_page(request):
    """
    The main homepage view
    """
    return render(request, 'home.html')

def view_list(request, list_id):
    """
    View to look at a to-do list of one user
    """
    list_ = List.objects.get(id=list_id)
    if request.method == "POST":
        Item.objects.create(text=request.POST['item_text'], list=list_)
        return redirect(f'/lists/{list_.id}/')
    return render(request, 'list.html', {'list': list_})

def new_list(request):
    """
    View to create a new list
    """
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = "You can't have an empty list item"
        return render(request, 'home.html', {'error': error})
    return redirect(f'/lists/{list_.id}/')

    
