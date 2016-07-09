# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from hello.models import Contact, NoteModel, RequestStore


admin.site.register(Contact)
admin.site.register(RequestStore)
admin.site.register(NoteModel)
