"""
Homepage Views for the list App
"""

from django.shortcuts import render, redirect

from lists.models import Item

def home_page(request):
    """
    The main homepage view
    """
    return render(request, 'home.html')

def view_list(request):
    """
    View to look at a to-do list of one user
    """
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')
