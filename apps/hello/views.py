# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers

from hello.models import Contact, RequestStore


def home_page(request):
    context = {}
    contact = Contact.objects.first()
    context['contact'] = contact
    return render(request, 'home.html', context)


def request_view(request):
    RequestStore.objects.filter(new_request=1).update(new_request=0)
    return render(request, 'requests.html')


def request_ajax(request):
    if request.is_ajax():
        new_request = RequestStore.objects.filter(new_request=1).count()
        request_list = RequestStore.objects.order_by('-date')[:10]
        list_req = serializers.serialize("json", request_list)
        data = json.dumps((new_request, list_req))
        return HttpResponse(data, content_type="application/json")

    return HttpResponseBadRequest('Error request')
