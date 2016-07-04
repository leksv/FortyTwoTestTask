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

    def test_home_page_one_contact_in_db(self):
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

    def test_home_page_two_contact_in_db(self):
        """
        Test home page if contact table has more then one record.
        """
        models.Contact.objects.create(
            name='Ivan',
            surname='Ivanov',
            email='ivan.ivanov@yandex.ru',
            date_of_birth=date(2016, 4, 25),
            bio='I was born ...',
            jabber='ivan@42cc.co',
            skype_id='ivan_ivanov')

        response = self.client.get(reverse('hello:home'))

        self.assertContains(response, 'Aleksey')
        self.assertNotContains(response, 'Ivan')

    def test_home_page_no_contact_in_db(self):
        """
        Test home page if contact table is empty.
        """
        models.Contact.objects.all().delete()
        response = self.client.get(reverse('hello:home'))

        self.assertNotContains(response, 'Aleksey')
        self.assertContains(response, 'Contact data no yet')


class RequestViewTest(TestCase):
    def test_request_view(self):
        """
        Request view should return response that has "Requests",
        "Path", "Method", "Date".
        """
        response = self.client.get(reverse('hello:requests'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'requests.html')
        self.assertIn('Requests', response.content)
        self.assertIn('Path', response.content)
        self.assertIn('Method', response.content)
        self.assertIn('Date', response.content)


class RequestAjaxTest(TestCase):
    def test_request_ajax_view(self):
        """
        Test request ajax view
        """
        self.client.get(reverse('hello:home'))
        response = self.client.get(reverse('hello:requests_ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertIn('GET', response.content)
        self.assertIn('path', response.content)
        self.assertIn('/', response.content)
