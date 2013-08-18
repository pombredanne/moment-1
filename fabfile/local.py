from fabric.api import task, local
from utilities import notify


@task
def flushall():
    notify('Flushing ALL Redis keys.')
    local('redis-cli FLUSHALL')
