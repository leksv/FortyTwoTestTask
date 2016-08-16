# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.shortcuts import render
from django.http.response import HttpResponseServerError
from django.core import serializers


from hello.models import Contact


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
