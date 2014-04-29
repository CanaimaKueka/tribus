from celery import task
from tribus.config.web import DEBUG
from tribus.config.base import PACKAGECACHE
from tribus.config.pkgrecorder import CANAIMA_ROOT, LOCAL_ROOT
from tribus.common.recorder import update_cache


@task
def update_cache_folder(*args):
    if DEBUG: 
        update_cache(LOCAL_ROOT, PACKAGECACHE)
    else:
        update_cache(CANAIMA_ROOT, PACKAGECACHE)