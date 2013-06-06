# -*- coding: utf-8 -*-

from django_notify.decorators import json_view, login_required_ajax
from django_notify import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.utils.translation import ugettext as _

@login_required_ajax
@json_view
def get_notifications(request, latest_id=None, is_viewed=False, max_results=10):
    
    notifications = models.Notification.objects.filter(subscription__settings__user=request.user,)
    
    if not is_viewed is None:
        notifications = notifications.filter(is_viewed=is_viewed)
    
    if not latest_id is None:
        notifications = notifications.filter(id__gt=latest_id)
    
    notifications = notifications.order_by('-id')
    notifications = notifications.prefetch_related('subscription', 'subscription__notification_type')
    
    from django.contrib.humanize.templatetags.humanize import naturaltime
    
    return {'success': True,
            'total_count': notifications.count(),
            'objects': [{'pk': n.pk,
                         'message': n.message,
                         'url': n.url,
                         'occurrences': n.occurrences,
                         'occurrences_msg': _(u'%d times') % n.occurrences,
                         'type': n.subscription.notification_type.key,
                         'since': naturaltime(n.created)} for n in notifications[:max_results]]}

@login_required
def goto(request, notification_id=None):
    referer = request.META.get('HTTP_REFERER', '')
    if not notification_id:
        return redirect(referer)
    notification = get_object_or_404(models.Notification, 
                                     subscription__settings__user=request.user,
                                     id=notification_id)
    notification.is_viewed=True
    notification.save()
    if not notification.url is None:
        return redirect(notification.url)
    return redirect(referer)
    
@login_required_ajax
@json_view
def mark_read(request, id_lte, notification_type_id=None, id_gte=None):
    
    notifications = models.Notification.objects.filter(subscription__settings__user=request.user,
                                                       id__lte=id_lte)
    
    if notification_type_id:
        notifications = notifications.filter(notification_type__id=notification_type_id)
    
    if id_gte:
        notifications = notifications.filter(id__gte=id_gte)
    
    notifications.update(is_viewed=True)
    
    return {'success': True}