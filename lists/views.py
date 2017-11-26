"""
Homepage Views for the list App
"""

from django.shortcuts import render

def home_page(request):
    """
    The main homepage view
    """
    return render(request, 'home.html', {'new_item_text': request.POST.get('item_text', '')})
