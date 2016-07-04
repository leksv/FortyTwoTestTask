# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from . import models


def home_page(request):
    context = {}
    contact = models.Contact.objects.first()
    context['contact'] = contact
    return render(request, 'home.html', context)
