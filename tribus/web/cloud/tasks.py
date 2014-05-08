from celery import task
from tribus.config.web import DEBUG
from tribus.config.base import PACKAGECACHE
from tribus.config.pkgrecorder import CANAIMA_ROOT, LOCAL_ROOT
from tribus.common.recorder import sync_cache, update_db_from_cache


@task
def update_cache(*args):
    if DEBUG:
        changes = sync_cache(LOCAL_ROOT, PACKAGECACHE)
        if changes:
            update_db_from_cache(changes)
    else:
        changes = sync_cache(CANAIMA_ROOT, PACKAGECACHE)
        if changes:
            update_db_from_cache(changes)


@task
def update_switches(*args):
    return True