# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import date
from datetime import timedelta
from dateutil.relativedelta import relativedelta

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

    def test_form_data_of_birth_earlier_now(self):
        """
        Test that date of birth cannot be later then now or now.
        """
        delta = timedelta(days=2)
        birth_date = date.today() + delta
        form = ContactForm({'date_of_birth': birth_date})

        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['date_of_birth'],
            ['Date of birth cannot be later then now or now.'])

        form = ContactForm({'date_of_birth': date.today()})
        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['date_of_birth'],
            ['Date of birth cannot be later then now or now.'])

    def test_form_data_of_birth_later_then_100_years_ago(self):
        """
        Test that Date of birth cannot be earlier then 100 years ago.
        """
        delta = relativedelta(years=100)
        birth_date = date.today() - delta
        form = ContactForm({'date_of_birth': birth_date})

        self.assertEqual(form.is_valid(), False)
        self.assertEqual(
            form.errors['date_of_birth'],
            ['Date of birth cannot be later then now or now.'])
