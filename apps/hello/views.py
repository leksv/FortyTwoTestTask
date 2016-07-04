# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest

from . import models


def home_page(request):
    context = {}
    contact = models.Contact.objects.first()
    context['contact'] = contact
    return render(request, 'home.html', context)


def request_ajax(request):
    if request.is_ajax():
        return HttpResponse(
            json.dumps([{'path': '/', 'method': 'GET', 'date': '2016-07-04'}]),
            content_type='application/json')

    return HttpResponseBadRequest('Error request')
