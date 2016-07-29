# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django import forms

from ckeditor.widgets import CKEditorWidget


from hello.models import Contact, NoteModel, RequestStore


class ContactAdminForm(forms.ModelForm):

    class Meta:
        model = Contact

        fields = [
                'name', 'surname', 'date_of_birth', 'bio',
                'email', 'jabber', 'skype_id', 'other', 'image']
        widgets = {
            'bio': CKEditorWidget(),
            'other': CKEditorWidget(),
        }


class ContactAdmin(admin.ModelAdmin):
    form = ContactAdminForm


admin.site.register(Contact, ContactAdmin)
admin.site.register(RequestStore)
admin.site.register(NoteModel)
