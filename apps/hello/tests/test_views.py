# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.test import TestCase
from django.core.urlresolvers import reverse

from hello.models import Contact
from hello.tests.temp_files import get_temporary_image
from hello.tests.temp_files import get_temporary_text_file


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


class FormPageTest(TestCase):
    fixtures = ['contact_data.json']

    def setUp(self):
        self.contact = Contact.objects.first()
        self.data = dict(name='Ivan', surname='Ivanov',
                         date_of_birth='2016-02-02',
                         bio='', email='ivanov@yandex.ru',
                         jabber='iv@jabb.com',
                         image=get_temporary_image())

    def test_form_page_edit_data(self):
        """
        Test check edit data at form page.
        """

        # send new data to server
        response = self.client.post(reverse('hello:contact_form'), self.data)

        response = self.client.get(reverse('hello:contact_form'))
        self.assertEqual(response.status_code, 200)

        # data are shown at form page according to changed data
        self.assertNotIn(self.contact.name, response.content)
        self.assertNotIn(self.contact.surname, response.content)
        self.assertNotIn(self.contact.date_of_birth.strftime('%Y-%m-%d'),
                         response.content)
        self.assertNotIn(self.contact.email, response.content)
        self.assertNotIn(self.contact.jabber, response.content)

        self.assertIn('Ivan', response.content)
        self.assertIn('Ivanov', response.content)
        self.assertIn('2016-02-02', response.content)
        self.assertIn('ivanov@yandex.ru', response.content)
        self.assertIn('iv@jabb.com', response.content)
        self.assertIn('test.jpg', response.content)

    def test_form_page_on_text_file(self):
        """
        Test check form_page return error if upload text file.
        """

        # add to data text file text.txt
        self.data.update({'image': get_temporary_text_file('text.txt')})

        response = self.client.post(reverse('hello:contact_form'), self.data)
        self.assertEqual(200, response.status_code)

        # add to data text file text.jpg
        self.data.update({'image': get_temporary_text_file('text.jpg')})

        response = self.client.post(reverse('hello:contact_form'), self.data)
        self.assertEqual(200, response.status_code)

    def test_form_page_edit_data_to_wrong(self):
        """
        Test check edit data at form page to wrong data.
        """

        # edit data with empty name and invalid data_of_birth, email
        self.data.update({'name': '',
                          'date_of_birth': 'date',
                          'email': 'ivanovyandex.ru'})

        # send new data to server
        response = self.client.post(reverse('hello:contact_form'), self.data)
        self.assertEqual(response.status_code, 200)

        # response errors
        self.assertIn('This field is required.', response.content)
        self.assertIn('Enter a valid date.', response.content)
        self.assertIn('Enter a valid email address.', response.content)

        # data in db did not change
        edit_contact = Contact.objects.first()
        self.assertEqual(self.contact.name, edit_contact.name)
