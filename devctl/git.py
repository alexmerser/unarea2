from fabric.decorators import task
from fabric.operations import local


@task
def feature_start(branch_name):
    """
    New feature. cmd >> fab git.feature_start:<branch_name>

    Start new feature branch ('git flow feature start <name>').
    Usage: fab git.feature_start:<branch_name>
    """
    local('git flow feature start %s' % branch_name)