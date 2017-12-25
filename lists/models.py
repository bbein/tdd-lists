"""
Seting up the ORM of the list APP
"""
from django.db import models
from django.core.urlresolvers import reverse

class List(models.Model):
    """
    defines one to-do list
    """
    def get_absolute_url(self):
        """
        returns the ubsolute url the list object should correspond to.
        """
        return reverse('view_list', args=[self.id])

class Item(models.Model):
    """
    defines the to-do list Item database schema
    """
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

