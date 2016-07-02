# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

from mixer.backend.django import mixer

from .. import models

class ContactTest(TestCase):
    def test_contact_model(self):
        """
        Check to create of model and save it to db.
        """
        contact = mixer.blend(models.Contact)
        self.assertEquals(contact.id, 1)

    def test_contact_method_unicode(self):
        """
        The method should return last name and name. 
        """
        contact = mixer.blend(
            models.Contact, name='Aleksey', surname='Voronov')
        self.assertEquals(str(contact), 'Voronov Aleksey')
