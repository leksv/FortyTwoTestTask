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

class RequestStoreTest(TestCase):
    def test_request_store(self):
        """
        Check to create of model and save it to db
        """

        models.RequestStore.objects.create(
            path='/', method='GET', date=date(2016, 7, 4))

        # now check we can find it in the database again
        all_requests = models.RequestStore.objects.all()
        self.assertEquals(len(all_requests), 1)
        only_request = all_requests[0]
        self.assertEquals(str(only_request), '/ - GET')

        # and check that it's saved its two attributes: path and method
        self.assertEquals(only_request.path, '/')
        self.assertEquals(only_request.method, 'GET')

