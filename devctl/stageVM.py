from fabric.api import task, run, sudo, env, cd
from fabric.colors import red
from fabric.context_managers import settings
from fabric.contrib.files import exists
from fabric.operations import error

"""
Stage VM tasks environment.
To create task-specific env just
create simple task with all env* definitions.

Example task:

@task
def stageVM():
    env.name = 'stage'
    env.hosts = ['172.127.0.50']

"""
env.name = 'stage'
env.type = 'STAGE'
env.project_root = '/home/unarea/'
env.server_root = env.project_root + 'unarea-server'
env.repository = 'git@bitbucket.org:unarea/unarea-server.git'
env.hosts = ['172.127.0.50']
env.user = 'uadmin'
env.password = 'uadmin1pass'
env.branch = 'develop'


@task
def init():
    if exists(env.server_root):
        error(red("%s exits! Aborting" % env.server_root))

    run('git clone %(repository)s' % env)
    setup_env()
    with cd(env.server_root):
        run('git checkout %(branch)s; git pull origin %(branch)s;' % env)
        run('python bootstrap.py')
        run('bin/buildout')
    configure_parts()
    with settings(warn_only=True):
        start_supervisor()
    start_apps()
    restart_network()
    restart_nginx()


@task
def setup_env():
    run('touch ~/.bash_profile')
    run('echo "export UNAREA_HOME=%(project_root)s" >> ~/.bash_profile' % env)
    run('echo "export UNAREA_APP_ID=SERVER-V2" >> ~/.bash_profile')
    run('echo "export UNAREA_ENV_TYPE=%(type)s" >> ~/.bash_profile' % env)
    run('echo "export UNAREA_APP_HOME=%(server_root)s" >> ~/.bash_profile' % env)
    run('source ~/.bash_profile')


@task
def configure_parts():
    with cd(env.server_root):
        sudo('rm -rf /etc/nginx/sites-enabled/unarea-server.conf')
        sudo('cp etc/nginx_unarea_server.conf /etc/nginx/sites-available/')
        if not exists('/etc/nginx/sites-enabled/nginx_unarea_server.conf'):
            sudo('ln -s /etc/nginx/sites-available/nginx_unarea_server.conf /etc/nginx/sites-enabled/')
        restart_nginx()

@task
def deploy():
    """
    Usage: $>fab <env_name> deploy
    """
    shutdown_apps()
    git_pull()
    build_server()
    configure_parts()
    start_apps()
    restart_nginx()


@task
def git_pull():
    with cd(env.server_root):
        run('git fetch;' % env)
        run('git checkout %(branch)s; git pull origin %(branch)s;' % env)


@task
def build_server():
    with cd(env.server_root):
        run('python bootstrap.py')
        run('bin/buildout')


@task
def restart_nginx():
    """Restart the web server"""
    sudo("/etc/init.d/nginx restart")


@task
def nginx_config_test():
    sudo("nginx -t")


@task
def restart_network():
    sudo("/etc/init.d/networking restart")


@task
def shutdown_apps():
    with cd(env.server_root):
        run('bin/supervisorctl stop all')


@task
def restart_apps():
    with cd(env.server_root):
        run('bin/supervisorctl stop all')
        run('bin/supervisorctl reload')
        run('bin/supervisorctl start all')


@task
def start_apps():
    with cd(env.server_root):
        run('bin/supervisorctl reload')
        run('bin/supervisorctl start all')


@task
def start_supervisor():
    with cd(env.server_root):
        run('bin/supervisord')


@task
def status():
    with cd('unarea-server'):
        results = run('bin/supervisorctl status')
        if 'FATAL' in results:
            print red(results)

@task
def destroy_server():
    if exists(env.server_root):
        run('rm -rf %(server_root)s' % env)
    sudo('rm -rf /etc/nginx/sites-enabled/nginx_unarea_server.conf')
    sudo('rm -rf /etc/nginx/sites-available/nginx_unarea_server.conf')
