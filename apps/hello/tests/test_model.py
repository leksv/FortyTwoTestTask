# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import date

from django.test import TestCase

from hello.models import Contact, RequestStore, NoteModel
from hello.tests.temp_files import get_temporary_image


class ContactTest(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='Алексей',
            surname='Воронов',
            email='aleks.woronow@yandex.ru',
            date_of_birth=date(2016, 2, 25))

    def test_contact_model(self):
        """
        Check to create of model and save it to db,
        and __unicode__ method should return last name and name.
        """
        all_contact = Contact.objects.all()
        self.assertEquals(len(all_contact), 1)
        contact = all_contact[0]
        self.assertEquals(contact.id, self.contact.id)
        self.assertEquals(unicode(contact), 'Воронов Алексей')
        self.assertEquals(contact.name, 'Алексей')

    def test_contact_model_image(self):
        """
        Test check that overwritten save method maintaining aspect ratio
        and reduce image to <= 200*200.
        """

        # save image file
        contact = Contact.objects.get(id=self.contact.id)
        contact.image = get_temporary_image()
        contact.save()

        # check that height and width <= 200
        self.assertTrue(contact.height <= 200)
        self.assertTrue(contact.width <= 200)

    def test_contact_model_image_delete(self):
        """
        Test check that delete method deleting file.
        """
        # save image file
        contact = Contact.objects.get(id=self.contact.id)
        contact.image = get_temporary_image()
        contact.save()

        # check image file is on storage
        file = os.path.isfile(contact.image.path)
        self.assertTrue(file)

        # delete contact
        contact.delete()

        # check image file is not on storage
        rm_file = os.path.isfile(contact.image.path)
        self.assertFalse(rm_file)


class RequestStoreTest(TestCase):
    def test_request_store(self):
        """
        Check to create of model and save it to db
        """

        RequestStore.objects.create(
            path='/', method='GET', date=date(2016, 7, 4))

        # now check we can find it in the database again
        all_requests = RequestStore.objects.all()
        self.assertEquals(len(all_requests), 1)
        only_request = all_requests[0]
        self.assertEquals(unicode(only_request), '/ - GET')

        # and check that it's saved its two attributes: path and method
        self.assertEquals(only_request.path, '/')
        self.assertEquals(only_request.method, 'GET')


class NoteModelTestCase(TestCase):
    def setUp(self):
        self.contact = Contact.objects.create(
            name='Алексей',
            surname='Воронов',
            email='aleks.woronow@yandex.ru',
            date_of_birth=date(2016, 2, 25))
        self.data = dict(model='Contact', inst='contact', action_type=0)

    def test_notemodel(self):
        """
        Test creat, change and delete obbject notemodel.
        """
        # create note about contact
        note_contact = NoteModel.objects.create(**self.data)

        # take all objects of NoteModel
        all_note = NoteModel.objects.all()
        self.assertEqual(len(all_note), 1)
        only_note = all_note[0]

        self.assertEqual(only_note.model, note_contact.model)
        self.assertEqual(only_note.action_type, 0)
        self.assertEquals(unicode(only_note),
                          "%s  %s: %s " % (
                              only_note.model,
                              only_note.get_action_type_display(),
                              only_note.inst))

        # change note about person to requeststore
        contact_note = NoteModel.objects.get(id=note_contact.id)
        contact_note.model = 'RequestStore'
        contact_note.inst = 'requeststore'
        contact_note.action_type = 1
        contact_note.save()

        # now note about requeststore action = 1
        contact_note_change = NoteModel.objects.get(model='RequestStore')
        self.assertEqual(contact_note_change.action_type, 1)

        # delete note person
        NoteModel.objects.all().delete()
        all_note = NoteModel.objects.all()
        self.assertEqual(all_note.count(), 0)

    def test_signal_processor(self):
        """
        Test signal processor records create,
        change and delete object.
        """
        # check action_type after created object (loaded fixtures) is 0
        note = NoteModel.objects.get(model='Conact')
        self.assertEqual(note.action_type, 0)

        # check action_type after change object is 1
        contact = Contact.objects.first()
        contact.name = 'Change'
        contact.save()
        note = NoteModel.objects.filter(model='Contact').last()
        self.assertEqual(note.action_type, 1)

        # check record after delete object is 2
        contact = Contact.objects.first()
        contact.delete()
        note = NoteModel.objects.last()
        self.assertEqual(note.action_type, 2)
