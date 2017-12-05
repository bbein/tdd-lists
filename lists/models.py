"""
Seting up the ORM of the list APP
"""
from django.db import models

class List(models.Model):
    """
    defines one to-do list
    """
    pass

class Item(models.Model):
    """
    defines the to-do list Item database schema
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

