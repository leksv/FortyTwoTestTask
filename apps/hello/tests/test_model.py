# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import date

from django.test import TestCase

from hello.models import Contact, RequestStore
from hello.tests.temp_files import get_temporary_image


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

    def test_contact_model_image(self):
        """
        Test check that overwritten save method maintaining aspect ratio
        and reduce image to <= 200*200.
        """

        # save image file
        contact = Contact.objects.get(id=self.contact.id)
        contact.image = get_temporary_image()
        contact.save()

        # check that height and width <= 200
        self.assertTrue(contact.height <= 200)
        self.assertTrue(contact.width <= 200)

    def test_contact_model_image_delete(self):
        """
        Test check that delete method deleting file.
        """
        # save image file
        contact = Contact.objects.get(id=self.contact.id)
        contact.image = get_temporary_image()
        contact.save()

        # check image file is on storage
        file = os.path.isfile(contact.image.path)
        self.assertTrue(file)

        # delete contact
        contact.delete()

        # check image file is not on storage
        rm_file = os.path.isfile(contact.image.path)
        self.assertFalse(rm_file)


class RequestStoreTest(TestCase):
    def test_request_store(self):
        """
        Check to create of model and save it to db
        """

        RequestStore.objects.create(
            path='/', method='GET', date=date(2016, 7, 4))

        # now check we can find it in the database again
        all_requests = RequestStore.objects.all()
        self.assertEquals(len(all_requests), 1)
        only_request = all_requests[0]
        self.assertEquals(unicode(only_request), '/ - GET')

        # and check that it's saved its two attributes: path and method
        self.assertEquals(only_request.path, '/')
        self.assertEquals(only_request.method, 'GET')
