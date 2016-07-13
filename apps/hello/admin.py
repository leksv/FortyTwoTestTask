# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from hello.models import RequestStore

admin.site.register(RequestStore)
