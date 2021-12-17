# WARNING
# THIS MODULE SHOULD ONLY BE RUN USING PYTHON 2.7

from fabric.api import env

# Many things are configured using the client and project code
env.client = 'zoyalab'
env.project_code = 'btsearch'

# This is the name of the folder within the repo which houses all code
# to be deployed.
env.web_dir = 'src'

# Environment-agnostic folders
env.project_dir = '/var/www/%(client)s/%(project_code)s' % env
env.static_dir = '/mnt/static/%(client)s/%(project_code)s' % env
env.builds_dir = '%(project_dir)s/builds' % env


def _configure(build_name):
    env.build = build_name
    env.virtualenv = '%(project_dir)s/virtualenvs/%(build)s/' % env
    env.code_dir = '%(project_dir)s/builds/%(build)s/' % env
    env.data_dir = '%(project_dir)s/data/%(build)s/' % env
    env.app_conf = 'conf/%(build)s.py' % env
    env.nginx_conf = 'deploy/nginx/%(build)s.conf' % env
    env.supervisord_conf = 'deploy/supervisord/%(build)s.conf' % env
    env.wsgi = 'deploy/wsgi/%(build)s.wsgi' % env


def test():
    _configure('test')
    env.hosts = ['192.168.2.51']


def stage():
    _configure('stage')
    env.hosts = ['stage-%(project_code)s-%(client)s.%(build)s' % env]


def prod():
    _configure('prod')
    env.hosts = ['146.185.177.44']
