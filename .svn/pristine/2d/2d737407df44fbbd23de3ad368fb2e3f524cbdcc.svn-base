import os
from conf.default import *

# We use an environmental variable to indicate the, erm, environment
# This block writes all settings to the local namespace
DJANGO_CONF = os.environ.get('DJANGO_CONF', 'conf.local')
try:
    module = __import__(DJANGO_CONF, globals(), locals(), ['*'])
    for k in dir(module):
        if not k.startswith('__'):
            locals()[k] = getattr(module, k)
except ImportError, e:
    import sys
    sys.stderr.write("""An import error occurred when looking for your environment
                       settings (%s): %s""" % (DJANGO_CONF, e))

# Add extra apps that are only needed locally (eg pyzen)
if 'EXTRA_APPS' in locals():
    INSTALLED_APPS = INSTALLED_APPS + EXTRA_APPS

# Adjust settings based on the DISABLED_APPS setting
if 'DISABLED_APPS' in locals():
    INSTALLED_APPS = [k for k in INSTALLED_APPS if k not in DISABLED_APPS]

    MIDDLEWARE_CLASSES = list(MIDDLEWARE_CLASSES)
    for a in DISABLED_APPS:
        for x, m in enumerate(MIDDLEWARE_CLASSES):
            if m.startswith(a):
                MIDDLEWARE_CLASSES.pop(x)

    TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS)
    for x, m in enumerate(TEMPLATE_CONTEXT_PROCESSORS):
        if m.startswith(a):
            TEMPLATE_CONTEXT_PROCESSORS.pop(x)

    DATABASE_ROUTERS = list(DATABASE_ROUTERS)
    for x, m in enumerate(DATABASE_ROUTERS):
        if m.startswith(a):
            DATABASE_ROUTERS.pop(x)