# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.core import serializers
from django.conf import settings
from django.contrib.auth.decorators import login_required

from hello.models import Contact, RequestStore
from hello.forms import ContactForm


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
        if request.method == 'POST':
            path = request.POST['path']
            priority = request.POST['priority']
            if int(priority) >= 0:
                RequestStore.objects.filter(path=path)\
                                    .update(priority=priority)
            return HttpResponse(json.dumps({'response': 'ok'}),
                                content_type='application/json')

        viewed = request.GET.get('viewed')
        if viewed == 'yes':
            RequestStore.objects.filter(new_request=1).update(new_request=0)

        new_request = RequestStore.objects.filter(new_request=1).count()
        request_list = RequestStore.objects.order_by('-date')[:10]
        request_list = list(request_list)
        request_list.sort(key=lambda a: a.path)
        list_req = serializers.serialize("json", request_list)
        data = json.dumps((new_request, list_req))
        return HttpResponse(data, content_type="application/json")

    return HttpResponseBadRequest('Error request')


@login_required(login_url='/login/')
def form_page(request):
    contact = Contact.objects.first()

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)

        if form.is_valid():
            form.save()

            if request.is_ajax():
                if getattr(settings, 'DEBUG', False):
                    time.sleep(3)

                if contact:
                    list_pers = serializers.serialize("json", [contact])
                    return HttpResponse(json.dumps(list_pers),
                                        content_type="application/json")
            else:
                return redirect('hello:success')
        else:
            if request.is_ajax():
                if getattr(settings, 'DEBUG', False):
                    time.sleep(2)
                errors_dict = {}
                if form.errors:
                    for error in form.errors:
                        e = form.errors[error]
                        errors_dict[error] = unicode(e)

                return HttpResponseBadRequest(json.dumps(errors_dict),
                                              content_type="application/json")
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contact_form.html', {'form': form})
