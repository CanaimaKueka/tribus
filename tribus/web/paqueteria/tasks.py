from celery import task
from tribus.common.recorder import update_package_cache
  
@task
def update_cache(*args):
    update_package_cache()
