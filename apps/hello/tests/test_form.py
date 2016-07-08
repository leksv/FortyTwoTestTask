# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date

from django.test import TestCase

from hello.forms import ContactForm


class FormTest(TestCase):
    def test_form_blank_data(self):
        """
        Test form blank data.
        """
        form = ContactForm({})

        self.assertEqual(form.is_valid(), False)
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['surname'], ['This field is required.'])
        self.assertEqual(
            form.errors['date_of_birth'], ['This field is required.'])
        self.assertEqual(form.errors['email'], ['This field is required.'])

    def test_form_valid_data(self):
        """
        Test form valid data.
        """
        form_data = {
            'name': 'Aleks',
            'surname': 'Woronow',
            'date_of_birth': date(2016, 2, 29),
            'email': 'aleks.woronow@yandex.ru',
            'jabber': '42cc@khavr.com'}

        form = ContactForm(data=form_data)
        self.assertEqual(form.is_valid(), True)
