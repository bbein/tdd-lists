"""
Homepage Views for the list App
"""

from django.shortcuts import render, redirect

from lists.models import Item

def home_page(request):
    """
    The main homepage view
    """
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})

def view_list(request):
    """
    View to look at a to-do list of one user
    """
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
