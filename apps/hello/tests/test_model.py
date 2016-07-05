# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.test import TestCase

from ..models import Contact


class ContactTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='Алексей',
            surname='Воронов',
            email='aleks.woronow@yandex.ru',
            date_of_birth=date(2016, 2, 25))

    def test_contact_model(self):
        """
        Check to create of model and save it to db,
        and __unicode__ method should return last name and name.
        """
        all_contact = Contact.objects.all()
        self.assertEquals(len(all_contact), 1)
        contact = all_contact[0]
        self.assertEquals(contact.id, self.contact.id)
        self.assertEquals(unicode(contact), 'Воронов Алексей')
        self.assertEquals(contact.name, 'Алексей')
