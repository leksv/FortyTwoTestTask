# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Contact


class HomePageTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='Алексей',
            surname='Воронов',
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

    def test_home_page_one_contact_in_db(self):
        """
        Test home page if contact table has one record.
        """
        response = self.client.get(reverse('hello:home'))

        self.assertContains(response, 'Алексей')
        self.assertContains(response, 'Воронов')
        self.assertContains(response, 'Feb. 25, 2016')
        self.assertContains(response, 'aleks.woronow@yandex.ru')
        self.assertContains(response, 'leksw@42cc.co')
        self.assertContains(response, 'aleksey_woronov')
        self.assertContains(response, 'I was born ...')

    def test_home_page_two_contact_in_db(self):
        """
        Test home page if contact table has more then one record.
        """
        Contact.objects.create(
            name='Ivan',
            surname='Ivanov',
            email='ivan.ivanov@yandex.ru',
            date_of_birth=date(2016, 4, 25),
            bio='I was born ...',
            jabber='ivan@42cc.co',
            skype_id='ivan_ivanov')

        response = self.client.get(reverse('hello:home'))

        self.assertContains(response, 'Алексей')
        self.assertNotContains(response, 'Ivan')

    def test_home_page_no_contact_in_db(self):
        """
        Test home page if contact table is empty.
        """
        Contact.objects.all().delete()
        response = self.client.get(reverse('hello:home'))

        self.assertNotContains(response, 'Алексей')
        self.assertContains(response, 'Contact data no yet')
