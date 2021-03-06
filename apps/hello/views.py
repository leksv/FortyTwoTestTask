# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import time
import logging

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.http.response import HttpResponseServerError
from django.core import serializers
from django.conf import settings
from django.contrib.auth.decorators import login_required

from hello.models import Contact, RequestStore
from hello.forms import ContactForm


logger = logging.getLogger("home_page")


def home_page(request):
    context = {}
    contact = None

    try:
        contact = Contact.objects.first()
        if contact:
            data = serializers.serialize('json', [contact])
            logger.info(data)
        else:
            logger.info('db is empty')

    except Exception as err:
        logger.error(err)
        return HttpResponseServerError('Server Error (500)')

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


@login_required(login_url='/login/')
def form_page(request):
    contact = Contact.objects.first()

    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)

        if form.is_valid():
            form.save()

            logger.info('Save from contact form: %s' % form.cleaned_data)

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

                    logger.info(
                        'Errors from contact form: %s' % form.errors.items())

                return HttpResponseBadRequest(json.dumps(errors_dict),
                                              content_type="application/json")
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contact_form.html', {'form': form})
