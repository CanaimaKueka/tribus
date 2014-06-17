from celery import task
from tribus import BASEDIR
from tribus.config.switches import SWITCHES_CONFIGURATION
from fabric.api import local, cd

@task
def update_switches(*args):
    POST = args[0]
    for switch_name in SWITCHES_CONFIGURATION.keys():
        if switch_name in POST:
            print "SWITCH %s: %s" % (switch_name, POST.get(switch_name))
            with cd('%s' % BASEDIR):
                local('python manage.py switch %s on' % switch_name)
        else:
            print "SWITCH %s: off" % (switch_name)
            with cd('%s' % BASEDIR):
                local('python manage.py switch %s off' % switch_name)
