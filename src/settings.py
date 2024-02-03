import os

# Use an env variable to determine which settings file to import.  Then copy
# all variables into the local namespace.

# If you want custom settings, create a new settings file (eg conf.barry) and
# import * from conf.local then apply your overrides.
conf_module = os.environ.get('DJANGO_CONF', 'conf.local')
try:
    module = __import__(conf_module, globals(), locals(), ['*'])
except ImportError:
    print("Unable to import %s" % conf_module)
else:
    for k in dir(module):
        if not k.startswith("__"):
            locals()[k] = getattr(module, k)

VERSION = 'UNVERSIONED'
