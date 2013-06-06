"""
todo: remove this module - not needed any more

this is an unfortunate copy-paste (mostly)
from the avatar app - the reason is that django-avatar app
does not support jinja templates
"""
import urllib
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.shortcuts import render
from django.utils.translation import ugettext as _
from django.views.decorators import csrf
from django.conf import settings

from django.contrib.auth.decorators import login_required

from avatar.forms import PrimaryAvatarForm, DeleteAvatarForm, UploadAvatarForm
from avatar.models import Avatar
from avatar.settings import AVATAR_MAX_AVATARS_PER_USER, AVATAR_DEFAULT_SIZE
from avatar.util import get_primary_avatar, get_default_avatar_url
from avatar.views import render_primary as django_avatar_render_primary

from askbot import models

notification = False
if 'notification' in settings.INSTALLED_APPS:
    from notification import models as notification

friends = False
if 'friends' in settings.INSTALLED_APPS:
    friends = True
    from friends.models import Friendship

def _get_next(request):
    """
    The part that's the least straightforward about views in this module is how they 
    determine their redirects after they have finished computation.

    In short, they will try and determine the next place to go in the following order:

    1. If there is a variable named ``next`` in the *POST* parameters, the view will
    redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters, the view will
    redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers, the view will
    redirect to that previous page.
    """
    next = request.POST.get('next', request.GET.get('next',
        request.META.get('HTTP_REFERER', None)))
    if not next:
        next = request.path
    return next
    
def _notification_updated(request, avatar):
    notification.send([request.user], "avatar_updated",
        {"user": request.user, "avatar": avatar})
    if friends:
        notification.send((x['friend'] for x in
                Friendship.objects.friends_for_user(request.user)),
            "avatar_friend_updated",
            {"user": request.user, "avatar": avatar}
        )

def _get_avatars(user):
    # Default set. Needs to be sliced, but that's it. Keep the natural order.
    avatars = user.avatar_set.all()
    
    # Current avatar
    primary_avatar = avatars.order_by('-primary')[:1]
    if primary_avatar:
        avatar = primary_avatar[0]
    else:
        avatar = None
    
    if AVATAR_MAX_AVATARS_PER_USER == 1:
        avatars = primary_avatar
    else:
        # Slice the default set now that we used the queryset for the primary avatar
        avatars = avatars[:AVATAR_MAX_AVATARS_PER_USER]
    return (avatar, avatars)    

@login_required
@csrf.csrf_protect
def add(request, extra_context=None, next_override=None,
        upload_form=UploadAvatarForm, *args, **kwargs):
    if extra_context is None:
        extra_context = {}
    avatar, avatars = _get_avatars(request.user)
    upload_avatar_form = upload_form(request.POST or None,
        request.FILES or None, user=request.user)
    if request.method == "POST" and 'avatar' in request.FILES:
        if upload_avatar_form.is_valid():
            avatar = Avatar(
                user = request.user,
                primary = True,
            )
            image_file = request.FILES['avatar']
            avatar.avatar.save(image_file.name, image_file)
            avatar.save()
            request.user.message_set.create(
                message=_("Successfully uploaded a new avatar."))
            if notification:
                _notification_updated(request, avatar)
            return HttpResponseRedirect(next_override or _get_next(request))
    data = { 
        'avatar': avatar, 
        'avatars': avatars, 
        'upload_avatar_form': upload_avatar_form,
        'next': next_override or _get_next(request),
        'view_user': request.user,
        'page_class': 'avatar-page',
    }
    if extra_context:
        data.update(extra_context)

    return render(request, 'avatar/add.html', data)

@login_required
@csrf.csrf_protect
def change(request, extra_context=None, next_override=None,
        upload_form=UploadAvatarForm, primary_form=PrimaryAvatarForm,
        *args, **kwargs):
    if extra_context is None:
        extra_context = {}
    avatar, avatars = _get_avatars(request.user)
    if avatar:
        kwargs = {'initial': {'choice': avatar.id}}
    else:
        kwargs = {}
    upload_avatar_form = upload_form(user=request.user, **kwargs)
    primary_avatar_form = primary_form(request.POST or None,
        user=request.user, avatars=avatars, **kwargs)
    if request.method == "POST":
        updated = False
        if 'choice' in request.POST and primary_avatar_form.is_valid():
            avatar = Avatar.objects.get(id=
                primary_avatar_form.cleaned_data['choice'])
            avatar.primary = True
            avatar.save()
            updated = True
            request.user.message_set.create(
                message=_("Successfully updated your avatar."))
        if updated and notification:
            _notification_updated(request, avatar)
        return HttpResponseRedirect(next_override or _get_next(request))
    data = {
        'avatar': avatar, 
        'avatars': avatars,
        'upload_avatar_form': upload_avatar_form,
        'primary_avatar_form': primary_avatar_form,
        'next': next_override or _get_next(request), 
        'view_user': request.user,
        'page_class': 'avatar-page',
    }
    if extra_context:
        data.update(extra_context)

    return render(request, 'avatar/change.html', data)

@login_required
@csrf.csrf_protect
def delete(request, extra_context=None, next_override=None, *args, **kwargs):
    if extra_context is None:
        extra_context = {}
    avatar, avatars = _get_avatars(request.user)
    delete_avatar_form = DeleteAvatarForm(request.POST or None,
        user=request.user, avatars=avatars)
    if request.method == 'POST':
        if delete_avatar_form.is_valid():
            ids = delete_avatar_form.cleaned_data['choices']
            if unicode(avatar.id) in ids and avatars.count() > len(ids):
                # Find the next best avatar, and set it as the new primary
                for a in avatars:
                    if unicode(a.id) not in ids:
                        a.primary = True
                        a.save()
                        if notification:
                            _notification_updated(request, a)
                        break
            Avatar.objects.filter(id__in=ids).delete()
            request.user.message_set.create(
                message=_("Successfully deleted the requested avatars."))
            return HttpResponseRedirect(next_override or _get_next(request))
    data = {
        'avatar': avatar, 
        'avatars': avatars,
        'delete_avatar_form': delete_avatar_form,
        'next': next_override or _get_next(request),
        'view_user': request.user,
        'page_class': 'avatar-page',
    }
    if extra_context:
        data.update(extra_context)

    return render(request, 'avatar/confirm_delete.html', data)

def render_primary(request, user_id = None, *args, **kwargs):
    user = models.User.objects.get(id = user_id)
    kwargs['user'] = user.username
    return django_avatar_render_primary(request, *args, **kwargs)
