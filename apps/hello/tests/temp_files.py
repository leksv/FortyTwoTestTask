# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import StringIO

from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image as Img


# Function create image file for test.
def get_temporary_image():
        output = StringIO.StringIO()
        size = (1200, 700)
        color = (255, 0, 0, 0)
        image = Img.new("RGBA", size, color)
        image.save(output, format='JPEG')
        image_file = InMemoryUploadedFile(
            output, None, 'test.jpg', 'jpeg', output.len, None)
        image_file.seek(0)
        return image_file


# Function create text file for test.
def get_temporary_text_file(name):
    io = StringIO.StringIO()
    io.write('test')
    text_file = InMemoryUploadedFile(
        io, None, name, 'text', io.len, None)
    text_file.seek(0)
    return text_file
