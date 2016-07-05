# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory

from ..models import RequestStore
from ..views import home_page
from apps.middleware.helloRequest import RequestMiddle


class RequestMiddlewareTests(TestCase):
    def test_middleware_is_included(self):
        """
        Test for inclusion RequestMiddleware in project.
        """
        self.client.get(reverse('hello:home'))
        last_middleware_obj = RequestStore.objects.last()
        self.assertEqual(last_middleware_obj.method, 'GET')
        self.assertEqual(last_middleware_obj.path, reverse('hello:home'))

    def test_middleware_not_store_request_to_request_ajax_view(self):
        """
        Test middleware RequestMiddle don't store request
        to request_ajax view.
        """
        self.client.get(reverse('hello:requests_ajax'),
                        HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        middleware_obj = RequestStore.objects.all()
        self.assertQuerysetEqual(middleware_obj, [])

    def test_middleware_store_user(self):
        """
        Test middleware RequestMiddle store request user.
        """
        request = RequestFactory().get(reverse('hello:home'))

        # add user to request
        User = get_user_model()
        user = User.objects.create(
            username='test', email='test@i.ua', password='test')
        request.user = user

        # middleware store request
        RequestMiddle().process_view(request, home_page)
        middleware_obj = RequestStore.objects.all()[0]
        self.assertEqual(middleware_obj.user.username, 'test')
