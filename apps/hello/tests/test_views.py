# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse


class HomePageTest(TestCase):
    def test_home_page(self):
        """
        Test home page
        """

        response = self.client.get(reverse('hello:home'))

        self.assertTemplateUsed(response, 'home.html')
        self.assertContains(response,
                            '<h1>42 Coffee Cups Test Assignment</h1>',
                            html=True)
        self.assertContains(response, 'Aleks')
        self.assertContains(response, 'Voronov')
        self.assertContains(response, '02.02.2016')
        self.assertContains(response, 'aleks.woronow@yandex.ru')
        self.assertContains(response, 'leksw@42cc.co')
        self.assertContains(response, 'aleksey_woronov')
        self.assertContains(response, 'I was born ...')
