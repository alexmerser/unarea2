# DEPLOY STAGE
# the user to use for the remote commands
#
# env.user = 'uadmin'
# the servers where the commands are executed
# env.hosts = ['172.127.0.50']
# env.password = "uadmin1pass"

from fabric.operations import run, sudo, require
from fabric.context_managers import cd, env
from fabric.contrib.files import exists


def stage():
    """
    Environment settings for stage.
    Usage:
         fab stage <task>
    """
    env.name = 'stage'
    env.project_root = '/home/unarea/'
    env.server_root = env.project_root+'unarea-server'
    env.repository = 'git@bitbucket.org:unarea/unarea-server.git'
    env.hosts = ['172.127.0.50']
    env.user = 'uadmin'
    env.branch = 'develop'

def deploy():
    """
    Usage:
    $>fab <env name> deploy
    """
    require('name')
    shutdown_apps()
    git_pull()
    build_server()
    configure_parts()
    start_apps()
    restart_nginx()

def git_pull():
    with cd(env.server_root):
        run('git fetch;' % env)
        run('git checkout %(branch)s; git pull origin %(branch)s;' % env)


def build_server():
    with cd(env.server_root):
        run('python bootstrap.py')
        run('bin/buildout')


def configure_parts():
    with cd(env.server_root):
        sudo('cp etc/nginx_unarea_server.conf /etc/nginx/sites-available/')
        sudo('rm -rf /etc/nginx/sites-enabled/unarea-server.conf')
        if not exists('/etc/nginx/sites-enabled/nginx_unarea_server.conf'):
            sudo('ln -s /etc/nginx/sites-available/nginx_unarea_server.conf /etc/nginx/sites-enabled/')

def restart_nginx():
    """Restart the web server"""
    sudo("/etc/init.d/nginx restart")

def shutdown_apps():
    with cd(env.server_root):
        run('bin/supervisorctl stop all')


def init():
    if not exists(env.server_root):
        run('git clone %(repository)s' % env)
    with cd(env.server_root):
        run('git checkout %(branch)s; git pull origin %(branch)s;' % env)
        run('python bootstrap.py')
        run('bin/buildout')
        start_supervisor()

def restart_apps():
    with cd(env.server_root):
        run('bin/supervisorctl stop all')
        run('bin/supervisorctl reload')
        run('bin/supervisorctl start all')

def start_apps():
    with cd(env.server_root):
        run('bin/supervisorctl reload')
        run('bin/supervisorctl start all')

def start_supervisor():
    with cd(env.server_root):
        run('bin/supervisord')


def status():
    with cd('unarea-server'):
        run('bin/supervisorctl status')


def destroy_server():
    if exists(env.server_root):
        run('rm -rf %(server_root)s' % env)
    sudo('rm -rf /etc/nginx/sites-enabled/nginx_unarea_server.conf')
    sudo('rm -rf /etc/nginx/sites-available/nginx_unarea_server.conf')