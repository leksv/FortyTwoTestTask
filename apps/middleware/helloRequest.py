# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from apps.hello.models import RequestStore


logger = logging.getLogger(__name__)


class RequestMiddleware(object):
    def process_view(self, request, view_func, *view_args, **view_kwargs):
        log_msg = '%s %s' % (request.method, request.path)

        if not (view_func.func_name == 'request_ajax'):
            req = RequestStore()
            req.path = request.path
            req.method = request.method

            if request.user.is_authenticated():
                req.user = request.user

            req.save()
            logger.info(log_msg + ' was saved')
        else:
            logger.info(log_msg + ' wasn\'t saved')

        return None
