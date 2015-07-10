from fabric.operations import run, sudo
from fabric.context_managers import cd, env
from fabric.contrib.files import exists

# the user to use for the remote commands

env.user = 'uadmin'
# the servers where the commands are executed
env.hosts = ['172.127.0.50']
env.password = "uadmin1pass"

def cleanup():
    if exists('unarea-server'):
        run('rm -rf unarea-server')
    sudo('rm -rf /etc/nginx/sites-enabled/unarea-server.conf')

def deploy():
    if not exists('unarea-server'):
        run('git clone git@bitbucket.org:unarea/unarea-server.git')
    else:
        run('ls -las')
    with cd('unarea-server'):

        if 'develop' not in run('git branch'):
            run('git checkout develop')
        run('python bootstrap.py')
        run('bin/buildout')

        sudo('cp etc/nginx_unarea_server.conf /etc/nginx/sites-available/')
        # sudo('rm -rf /etc/nginx/sites-enabled/unarea-server.conf')
        if not exists('/etc/nginx/sites-enabled/nginx_unarea_server.conf'):
            sudo('ln -s /etc/nginx/sites-available/nginx_unarea_server.conf /etc/nginx/sites-enabled/')
        #
        sudo('service nginx restart')

def shutdown_all():
    with cd('unarea-server'):
        run('bin/supervisorctl stop all')


def restart_all():
    with cd('unarea-server'):
        run('bin/supervisorctl stop all')
        run('bin/supervisorctl reload')
        run('bin/supervisorctl start all')

def start_app():
    with cd('unarea-server'):
        run('bin/supervisord')
        run('bin/supervisorctl start all')


def status():
    with cd('unarea-server'):
        run('bin/supervisorctl status')