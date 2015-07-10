from fabric.operations import run, sudo
from fabric.context_managers import cd, env
from fabric.contrib.files import exists

# the user to use for the remote commands

env.user = 'uadmin'
# the servers where the commands are executed
env.hosts = ['172.127.0.50']
env.password = "uadmin1pass"

def deploy():
    if not exists('unarea-server'):
        run('git clone git@bitbucket.org:unarea/unarea-server.git')
    else:
        run('ls -las')
    with cd('unarea-server'):
        run('git checkout develop')
        run('git branch')
        run('python bootstrap.py')
        run('bin/buildout')
        # sudo('cp etc/nginx_unarea_server.conf /etc/nginx/nginx.conf')
        # sudo('service nginx restart')


def start_app():
    with cd('unarea-server'):
        run('bin/supervisord')
        run('bin/supervisorctl start all')