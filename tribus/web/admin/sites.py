from functools import update_wrapper
from django.utils import six
from django.conf.urls import patterns, url, include
from django.contrib.admin.sites import AdminSite
from django.contrib.contenttypes import views as contenttype_views

from tribus.web.admin.views import (tribus_config, active_modules,
                                    logger_levels)
from tribus.web.registration.forms import LoginForm


class TribusAdmin(AdminSite):

    login_template = 'registration/login_form.html'
    login_form = LoginForm

    def get_urls(self):

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        urlpatterns = patterns(
            '',
            url(regex=r'^$',
                view=wrap(self.index),
                name='index'),
            url(regex=r'^config/$',
                view=wrap(tribus_config)),
            url(regex=r'^config/active-modules/$',
                view=wrap(active_modules)),
            url(regex=r'^config/logger-levels/$',
                view=wrap(logger_levels)),
            url(regex=r'^r/(?P<content_type_id>\d+)/(?P<object_id>.+)/$',
                view=wrap(contenttype_views.shortcut),
                name='view_on_site'),
            url(regex=r'^(?P<app_label>\w+)/$',
                view=wrap(self.app_index),
                name='app_list')
        )

        for model, model_admin in six.iteritems(self._registry):
            urlpatterns += patterns(
                '',
                url(regex=r'^%s/%s/' % (model._meta.app_label,
                                        model._meta.model_name),
                    view=include(model_admin.urls))
            )

        return urlpatterns

tribus_admin = TribusAdmin()
