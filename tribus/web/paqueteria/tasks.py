from celery import task
from tribus.common.recorder import verify_updates

@task
def verify_repository(*args):
    verify_updates()

    
    