from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, cd
from __future__ import with_statement
import random

env_hosts = ['159.203.234.119']
REPO_URL  = 'https://github.com/Diego-MX/superlists.git'

def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p %s/%s' % (site_folder, subfolder))

def _get_latest_source(source_folder):
    with cd(source_folder):
        if exists('/.git'):
            run('git fetch')
        else:
            run('git clone %s .' % REPO_URL)
        current_commit = local('git log -n 1 --format=%H', capture=True)
        run('git reset --hard %s' % current_commit)

def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/superlists/settings.py'
    sed(settings_path, "DEBUG = True",
                       "DEBUG = False")
    sed(settings_path, "ALLOWED_HOSTS =.+$",
                       "ALLOWED_HOSTS = ["%s"]" % site_name)
    # I'm not convinced about this key generating files.
    secret_key_file = source_folder + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'arbitrary_chars_for_randomness'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % key)
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    run('%s/bin/pip install -r %s/reqs.txt' %
        (virtualenv_folder, source_folder))

def _update_static_files(source_folder):
    with cd(source_folder + '../virtualenv/bin'):
        run('python3 manage.py collectstatic --noinput')

def _update_database(source_folder):
    with cd(source_folder + '../virtualenv/bin'):
        run('python3 manage.py migrate --noinput')

def deploy(site_name):
    site_folder = '/home/%s/sites/%s' % (env.user, site_name)
    source_folder = site_folder + '/source'

    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, site_name)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
