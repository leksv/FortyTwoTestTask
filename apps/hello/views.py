# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .models import Contact


def home_page(request):
    context = {}
    contact = Contact.objects.first()
    context['contact'] = contact
    return render(request, 'home.html', context)
