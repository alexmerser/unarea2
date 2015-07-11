from fabric.operations import local
import subprocess
from fabric.api import task
import pprint
import time


@task
def state(guest, verbose=False):
    """Get the state of the specified machine."""
    vm_info = subprocess.Popen(['VBoxManage', '-q', 'showvminfo', guest,
                                '--machinereadable'], stdout=subprocess.PIPE)
    result = {item.split('=')[0].strip("\"\""): item.split('=')[1].strip("\"\"\n") for item in vm_info.stdout.readlines()}
    if verbose:
        pprint.pprint(result)
    return result['VMState']

@task
def start(guest):
    """ Run virtualbox machine """
    local('VBoxManage -q startvm %s' % guest)


@task
def stop(guest):
    """ Stop virtualbox machine """
    local('VBoxManage -q controlvm %s acpipowerbutton' % guest)
    while True:
        vm_state = state(guest=guest)

        if vm_state in ['stopped', 'poweroff', 'saved']:
            break

        time.sleep(3)