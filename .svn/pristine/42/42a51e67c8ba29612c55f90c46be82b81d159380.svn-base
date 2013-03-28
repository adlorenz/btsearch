import os
import sys
import site

sys.stdout = sys.stderr

# Project root
root = '/var/www/btsearch/builds/dev'
sys.path.insert(0, root)

# Packages from virtualenv
activate_this = '/var/www/btsearch/environments/dev/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# Set environmental variable and fire WSGI handler
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['DJANGO_CONF'] = 'conf.dev'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
