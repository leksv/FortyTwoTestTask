# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def home_page(request):
    context = {
        'name': 'Aleksey',
        'surname': 'Voronov',
        'date': '02.02.2016',
        'bio': 'I was born ...',
        'email': 'aleks.woronow@yandex.ru',
        'jabber': 'leksw@42cc.co',
        'skype': 'aleksey_woronov'
    }
    return render(request, 'home.html', context)
