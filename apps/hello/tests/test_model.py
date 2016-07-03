# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.test import TestCase

from .. import models


class ContactTest(TestCase):
    def setUp(self):
        models.Contact.objects.create(
            name='Aleksey',
            surname='Voronov',
            email='aleks.woronow@yandex.ru',
            date_of_birth=date(2016, 2, 25))

    def test_contact_model(self):
        """
        Check to create of model and save it to db,
        and __unicode__ method should return last name and name.
        """
        all_contact = models.Contact.objects.all()
        self.assertEquals(len(all_contact), 1)
        contact = all_contact[0]
        self.assertEquals(contact.id, 1)
        self.assertEquals(str(contact), 'Voronov Aleksey')
