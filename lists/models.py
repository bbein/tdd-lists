"""
Seting up the ORM of the list APP
"""
from django.db import models

class Item(models.Model):
    """
    defines the to-do list Item database schema
    """
    text = models.TextField(default='')
