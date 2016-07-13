# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.test import TestCase
from django.core.urlresolvers import reverse

from hello.models import Contact, RequestStore


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
    def test_request_ajax_view_if_ajax_request(self):
        """
        Test request ajax view if ajax request.
        """
        self.client.get(reverse('hello:home'))
        response = self.client.get(reverse('hello:requests_ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertIn('/', response.content)
        self.assertIn('GET', response.content)

    def test_request_ajax_view_if_not_ajax_request(self):
        """
        Test request ajax view if not ajax request.
        """
        response = self.client.get(reverse('hello:requests_ajax'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('Error request', response.content)

    def test_request_ajax_return_10_last_request(self):
        """
        Test check that request_ajax view returns 10 last objects
        when in db more than 10 records.
        """

        # create 15 records to db
        for i in range(1, 15):
            path = '/test%s' % i
            method = 'GET'
            RequestStore.objects.create(path=path, method=method)

        # check number of objects in db
        req_list = RequestStore.objects.count()
        self.assertEqual(req_list, i)

        # check that 10 objects in response
        response = self.client.get(reverse('hello:requests_ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(10, response.content.count('pk'))
        self.assertEqual(10, response.content.count('GET'))
        self.assertNotIn('/test0', response.content)
        self.assertNotIn('"/test1"', response.content)
        self.assertNotIn('/test2', response.content)
        self.assertNotIn('/test3', response.content)
        self.assertNotIn('/test4', response.content)
        self.assertIn('/test5', response.content)
        self.assertIn('/test6', response.content)
        self.assertIn('/test7', response.content)
        self.assertIn('/test8', response.content)
        self.assertIn('/test9', response.content)
        self.assertIn('/test10', response.content)
        self.assertIn('/test11', response.content)
        self.assertIn('/test12', response.content)
        self.assertIn('/test13', response.content)
        self.assertIn('/test14', response.content)
