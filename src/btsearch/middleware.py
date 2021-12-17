# Orignal version taken from http://www.djangosnippets.org/snippets/186/
# Original author: udfalkso
# Modified by: Shwagroo Team and Gun.io

import os
import re
import tempfile

from django.conf import settings

import cProfile
import pstats
import io

words_re = re.compile(r'\s+')

group_prefix_re = [
    re.compile("^.*/django/[^/]+"),
    re.compile("^(.*)/[^/]+$"),  # extract module path
    re.compile(".*"),  # catch strange entries
]


class CProfileMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_view(self, request, callback, callback_args, callback_kwargs):
        if settings.DEBUG and 'prof' in request.GET:
            self.profiler = cProfile.Profile()
            args = (request,) + callback_args
            return self.profiler.runcall(callback, *args, **callback_kwargs)

    def process_response(self, request, response):
        if settings.DEBUG and 'prof' in request.GET:
            (fd, self.profiler_file) = tempfile.mkstemp()
            self.profiler.dump_stats(self.profiler_file)
            out = io.StringIO()
            stats = pstats.Stats(self.profiler_file, stream=out)
            stats.strip_dirs()          # Must happen prior to sort_stats
            if request.GET['prof']:
                stats.sort_stats(request.GET['prof'])
            stats.print_stats()
            os.unlink(self.profiler_file)
            response.content = '<pre>%s</pre>' % out.getvalue()
        return response
