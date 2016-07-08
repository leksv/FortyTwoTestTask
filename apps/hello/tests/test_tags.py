# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission

from hello.templatetags.edit_link import edit_link
from hello.models import Contact


class TagAdminLinkTest(TestCase):
    fixtures = ['admin_data.json', 'contact_data.json']

    def test_edit_link_tag_is_at_home_page(self):
        """
        Test check tag is on home page
        """
        contact = Contact.objects.first()
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('hello:home'))
        link = '<a href="/admin/hello/contact/%s/">(admin)</a>' % contact.id
        self.assertIn(link, response.content)

    def test_edit_link_tag_recive_model_that_register_admin(self):
        """
        Test check tag if it recive model that register in admin
        """
        # test edit_link recive instance model that register admin
        contact = Contact.objects.first()
        link_contact_one = edit_link(contact)['edit_link']

        self.client.login(username='admin', password='admin')
        response = self.client.get(link_contact_one)

        self.assertIn('Django administration', response.content)
        self.assertIn(str(contact), response.content)

    def test_edit_link_tag_recive_model_that_not_register_admin(self):
        """
        Test check tag if it recive model that not register in admin
        """
        # test edit_link recive instance model that not register admin
        permission = Permission.objects.first()
        link_permission_one = edit_link(permission)

        self.assertEqual(link_permission_one, None)

    def test_edit_link_tag_recive_arg_that_not_instance_model(self):
        """
        Test check tag if it recive argument that not models.Model instance
        """
        # test edit_link recive invalid argument
        with self.assertRaises(TypeError) as err:
            edit_link(1)

        # now edit_link raise TypeError
        self.assertEquals(
            err.exception.args[0],
            'Invalide type arg for edit_link, shoud be models.Model instance')
