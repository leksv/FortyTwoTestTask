# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse


from apps.middleware.helloRequest import RequestMiddle
from .. import models
from ..decorators import not_record_request
from ..views import home_page


class RequestMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = RequestMiddle()
        self.request_store = RequestStore
        self.user = get_user_model().objects.get(id=1)

    def test_middleware_is_included(self):
        """
        Test for inclusion RequestMiddleware in project.
        """
        self.client.get(reverse('hello:home'))
        last_middleware_obj = models.RequestStore.objects.last()
        self.assertEqual(last_middleware_obj.method, 'GET')
        self.assertEqual(last_middleware_obj.path, reverse('hello:home'))

    def test_middleware_not_store_request_to_request_ajax_view(self):
        """
        Test middleware RequestMiddle don't store request
        to request_ajax view.
        """
        response = self.client.get(reverse('hello:requests_ajax'),
                                   HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        middleware_obj = models.RequestStore.objects.all()
        self.assertQuerysetEqual(middleware_obj, [])
