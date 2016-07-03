# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.test import TestCase
from django.core.urlresolvers import reverse

from .. import models


class HomePageTest(TestCase):
    def setUp(self):
        models.Contact.objects.create(
            name='Aleksey',
            surname='Voronov',
            email='aleks.woronow@yandex.ru',
            date_of_birth=date(2016, 2, 25),
            bio='I was born ...',
            jabber='leksw@42cc.co',
            skype_id='aleksey_woronov')

    def test_home_page_response_and_template(self):
        """
        Test home page response and template.
        """
        response = self.client.get(reverse('hello:home'))

        self.assertTemplateUsed(response, 'home.html')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            '<h1>42 Coffee Cups Test Assignment</h1>',
                            html=True)

    def test_home_page_one_contact(self):
        """
        Test home page if contact table has one record.
        """
        response = self.client.get(reverse('hello:home'))

        self.assertContains(response, 'Aleksey')
        self.assertContains(response, 'Voronov')
        self.assertContains(response, 'Feb. 25, 2016')
        self.assertContains(response, 'aleks.woronow@yandex.ru')
        self.assertContains(response, 'leksw@42cc.co')
        self.assertContains(response, 'aleksey_woronov')
        self.assertContains(response, 'I was born ...')
