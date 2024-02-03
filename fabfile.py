# WARNING
# THIS MODULE SHOULD ONLY BE RUN USING PYTHON 2.7

import datetime
import os

from fabric.decorators import runs_once
from fabric.operations import put, prompt
from fabric.colors import green, red
from fabric.api import local, cd, sudo
from fabric.contrib.files import exists

from fabconfig import env
from fabconfig import test, stage, prod


def _get_commit_id():
    """
    Return the commit ID for the branch about to be deployed
    """
    return local('git rev-parse HEAD', capture=True)[:20]


def notify(msg):
    bar = '+' + '-' * (len(msg) + 2) + '+'
    print green('')
    print green(bar)
    print green("| %s |" % msg)
    print green(bar)
    print green('')

# Deployment tasks


@runs_once
def update_codebase(branch, repo):
    """
    Update codebase from the Git repo
    """
    notify('Updating codebase from remote "%s", branch "%s"' % (repo, branch))
    local('git pull %s %s' % (repo, branch))
    notify('Push any local changes to remote %s' % branch)
    local('git push %s %s' % (repo, branch))


@runs_once
def set_reference_to_deploy_from(branch):
    """
    Determine the refspec (tag or commit ID) to build from

    The role of this task is simply to set the env.version variable
    which is used later on.
    """
    notify("Determine the git reference to deploy from")
    # Versioning - we either deploy from a tag or we create a new one
    local('git fetch --tags')

    if env.build == 'test':
        # Allow a new tag to be set, or generate on automatically
        print ''
        create_tag = prompt(red('Tag this release? [y/N] '))
        if create_tag.lower() == 'y':
            notify("Showing latest tags for reference")
            local('git tag | sort -V | tail -5')
            env.version = prompt(red('Tag name [in format x.x.x]? '))
            notify("Tagging version %s" % env.version)
            local('git tag %s -m "Tagging version %s in fabfile"' % (env.version, env.version))
            local('git push --tags')
        else:
            deploy_version = prompt(red('Build from a specific commit (useful for debugging)? [y/N] '))
            print ''
            if deploy_version.lower() == 'y':
                env.version = prompt(red('Choose commit to build from: '))
            else:
                env.version = local('git describe %s' % branch, capture=True).strip()
    else:
        # An existing tag must be specified to deploy to QE or PE
        local('git tag | sort -V | tail -5')
        env.version = prompt(red('Choose tag to build from: '))
        # Check this is valid
        notify("Checking chosen tag exists")
        local('git tag | grep "%s"' % env.version)

    if env.build == 'prod':
        # If a production build, then we ensure that the master branch
        # gets updated to include all work up to this tag
        notify("Merging tag into master")
        local('git checkout master')
        local('git merge %s' % env.version)
        local('git push origin master')
        local('git checkout develop')


def set_ssh_user():
    if 'DEPLOYMENT_USER' in os.environ:
        env.user = os.environ['DEPLOYMENT_USER']
    else:
        env.user = prompt(red('Username for remote host? [default is current user] '))
    if not env.user:
        env.user = os.environ['USER']


def deploy_codebase(archive_file, commit_id):
    """
    Push a tarball of the codebase up
    """
    upload(archive_file)
    unpack(archive_file)


def prepare(repo='origin'):
    notify('BUILDING TO %s' % env.build.upper())

    # Ensure we have latest code locally
    branch = local('git branch | grep "^*" | cut -d" " -f2', capture=True)
    update_codebase(branch, repo)
    set_reference_to_deploy_from(branch)

    # Create a build file ready to be pushed to the servers
    notify("Building from refspec %s" % env.version)
    env.build_file = '/tmp/build-%s.tar.gz' % str(env.version)
    local('git archive --format tar %s %s | gzip > %s' % (env.version, env.web_dir, env.build_file))

    # Set timestamp now so it is the same on all servers after deployment
    now = datetime.datetime.now()
    env.build_dir = '%s-%s' % (env.build, now.strftime('%Y-%m-%d-%H-%M'))
    env.code_dir = '%s/%s' % (env.builds_dir, env.build_dir)


def deploy():
    """
    Deploys the codebase
    """
    # Set SSH user and upload codebase to all servers, both
    # app and proc.
    set_ssh_user()
    init()
    deploy_codebase(env.build_file, env.version)
    deploy_app_config()

    update_virtualenv()
    migrate()
    collect_static_files()
    deploy_nginx_config()
    deploy_supervisord_config()
    deploy_cronjobs()

    switch_symlink()
    reload_python_code()
    reload_nginx()
    reload_supervisord()
    delete_old_builds()


def init():
    """
    Create initial project/build folder structure on remote machine
    """
    notify('Setting up remote project structure for %(build)s build' % env)
    sudo('mkdir -p %(project_dir)s' % env)
    with cd(env.project_dir):
        sudo('mkdir -p builds')
        sudo('mkdir -p data/%(build)s' % env)
        sudo('mkdir -p logs/%(build)s' % env)
        sudo('mkdir -p media/%(build)s' % env)
        sudo('mkdir -p run/%(build)s' % env)

        # Change directory permissions so uwsgi and nginx don't trip over
        sudo('chown -R root.www-data logs/ media/ run/')
        sudo('chmod -R g+w logs/ media/ run/')

        # Check for virtualenv
        virtualenv_dir = 'virtualenvs/%(build)s' % env
        if not exists(virtualenv_dir):
            sudo('mkdir -p %s' % virtualenv_dir)
            with cd('%(project_dir)s/virtualenvs/' % env):
                sudo('`which virtualenv` --no-site-packages %(build)s/' % env)
                sudo('echo "export DJANGO_CONF=\"conf.%(build)s\"" >> %(build)s/bin/activate' % env)

    with cd('%(project_dir)s/builds/' % env):
        if not exists(env.build):
            # Create directory and symlink for "zero" build
            sudo('mkdir %(build)s-0' % env)
            sudo('ln -s %(build)s-0 %(build)s' % env)

    notify('Remote project structure created')


def switch_symlink():
    notify("Switching symlinks")
    with cd(env.builds_dir):
        # Create new symlink for build folder
        sudo('if [ -h %(build)s ]; then unlink %(build)s; fi' % env)
        sudo('ln -s %(build_dir)s %(build)s' % env)


def reload_python_code():
    notify('Touching WSGI file to reload python code')
    with cd(env.builds_dir):
        sudo('touch %(build)s/%(wsgi)s' % env)


def reload_nginx():
    notify('Reloading nginx configuration')
    sudo('/etc/init.d/nginx force-reload')


def reload_supervisord():
    notify('Reloading supervisord configuration')
    sudo('/usr/bin/supervisorctl reload')


def reload_tomcat():
    sudo('/etc/init.d/tomcat6 force-reload')


def upload(local_path, remote_path=None, use_sudo=False):
    """
    Uploads a file
    """
    if not remote_path:
        remote_path = local_path
    notify("Uploading %s to %s" % (local_path, remote_path))
    put(local_path, remote_path, use_sudo)


def unpack(archive_path):
    """
    Unpacks the tarball into the correct place but doesn't switch
    the symlink
    """
    # Ensure all folders are in place
    sudo('if [ ! -d "%(builds_dir)s" ]; then mkdir -p "%(builds_dir)s"; fi' % env)

    notify("Creating remote build folder")
    with cd(env.builds_dir):
        sudo('tar xzf %s' % archive_path)

        # Create new build folder
        sudo('if [ -d "%(build_dir)s" ]; then rm -rf "%(build_dir)s"; fi' % env)
        sudo('mv %(web_dir)s %(build_dir)s' % env)

        # Symlink in uploads folder
        sudo('ln -s ../../../media/%(build)s %(build_dir)s/public/media' % env)

        # Append release info to settings.py
        sudo("sed -i 's/UNVERSIONED/%(version)s/' %(build_dir)s/settings.py" % env)

        # Add file indicating Git commit
        sudo('echo -e "refspec: %s\nuser: %s" > %s/build-info' % (env.version, env.user, env.build_dir))

        # Remove archive
        sudo('rm %s' % archive_path)


def set_robots_and_sitemaps():
    notify("Setting robots.txt and sitemaps")
    with cd(env.builds_dir):
        # create the proper symlinks to sitemaps and robots.txt
        sudo("mkdir -p %(static_dir)s/%(build)s/sitemaps" % env)
        sudo("""if [ -d %(static_dir)s/%(client)s/%(build)s/robots.txt ]; then
                    cp %(build_dir)s/static/robots.txt %(static_dir)s/%(client)s/%(build)s/;
                fi;""" % env)
        with cd("%(build_dir)s/public/static/" % env):
            sudo("rm -rf sitemaps && ln -s %(static_dir)s/%(build)s/sitemaps sitemaps" % env)
            sudo("rm robots.txt && ln -s %(static_dir)s/%(/%(build)s/robots.txt robots.txt" % env)


def update_virtualenv():
    """
    Install the dependencies in the requirements file
    """
    with cd(env.code_dir):
        sudo('source %s/bin/activate && pip install -r deploy/requirements.txt' % env.virtualenv)


def collect_static_files():
    notify("Collecting static files")
    with cd(env.code_dir):
        sudo('source %s/bin/activate && ./manage.py collectstatic --noinput > /dev/null' % env.virtualenv)
        sudo('chmod -R g+w public' % env)


def migrate():
    """
    Apply any schema alterations
    """
    notify("Applying database migrations")
    with cd(env.code_dir):
        sudo('source %s/bin/activate && ./manage.py syncdb --noinput > /dev/null' % env.virtualenv)
        sudo('source %s/bin/activate && ./manage.py migrate --ignore-ghost-migrations' % env.virtualenv)


def deploy_app_config():
    notify("Deploying application's environment-specific config")
    local_path = '%(web_dir)s/%(app_conf)s' % env
    remote_path = '%(code_dir)s/%(app_conf)s' % env
    use_sudo = True
    upload(local_path, remote_path, use_sudo)


def deploy_nginx_config():
    notify('Moving nginx config into place')
    with cd(env.code_dir):
        sudo('mv %(nginx_conf)s /etc/nginx/sites-enabled/' % env)


def deploy_supervisord_config():
    notify('Moving supervisord config into place')
    with cd(env.code_dir):
        sudo('mv %(supervisord_conf)s /etc/supervisor/conf.d/' % env)


def deploy_cronjobs():
    """
    Deploy the app server cronjobs
    """
    notify('Deploying cronjobs')
    with cd(env.code_dir):
        # Replace variables in cron files
        sudo("rename 's#BUILD#%(build)s#' deploy/cron.d/*" % env)
        sudo("sed -i 's#VIRTUALENV_ROOT#%(virtualenv)s#g' deploy/cron.d/*" % env)
        sudo("sed -i 's#BUILD_ROOT#%(code_dir)s#g' deploy/cron.d/*" % env)
        sudo("mv deploy/cron.d/* /etc/cron.d" % env)


def delete_old_builds():
    notify('Deleting old builds')
    with cd(env.builds_dir):
        sudo('find . -maxdepth 1 -type d -name "%(build)s*" | sort -r | sed "1,9d" | xargs rm -rf' % env)
