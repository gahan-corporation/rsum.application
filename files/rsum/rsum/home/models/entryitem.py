#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module to define EntryItem objects."""
from __future__ import unicode_literals
from __future__ import print_function

from django.db import models


class EntryItem(models.Model):
    """Class that defines EntryItem objects."""
    #: Link to the parent Entry model object.
    entry = models.ForeignKey('home.Entry', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='entry item')
    content = models.TextField() 

    def get_list_item(self, entry):
        """Get an EntryItem object."""
        items = []
        for item in list(
            EntryItem.objects.filter(
                entry=entry
            ).values()
        ):
            items.append(item)
        return items

    def save_list_item(self, list_item, pe):
        """Save an EntryItem object."""
        if (
            isinstance(list_item, str) or
            isinstance(list_item, unicode)
        ):
            eli = EntryItem()
            eli.entry = pe
            eli.value = list_item
            eli.save()

        if isinstance(list_item, list):
            for i in list_item:
                eli = EntryItem()
                eli.entry = pe
                eli.value = str(i)
                eli.save()
        return EntryItem.objects.values() 

    class Meta:
        app_label = "home"
        managed = True
