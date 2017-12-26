"""
Form for the list app
"""

from django import forms

from lists.models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"

class ItemForm(forms.models.ModelForm):
    """
    Item form class for input validation
    """
    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text' : forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
