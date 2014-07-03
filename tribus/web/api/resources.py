#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import yaml

from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.paginator import InvalidPage
from django.http.response import Http404

from tastypie import fields
from tastypie.cache import NoCache
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.resources import ModelResource, Resource
from tastypie.fields import ManyToManyField, OneToOneField
from tastypie.authentication import SessionAuthentication
from tastypie.validation import CleanedDataFormValidation

from waffle import switch_is_active

from haystack.query import SearchQuerySet, EmptySearchQuerySet

from tribus.web.models import Trib, Comment
from tribus.web.cloud.models import Package
from tribus.web.profile.models import UserProfile
from tribus.web.forms import TribForm, CommentForm
from tribus.web.api.authorization import (
    TimelineAuthorization,
    TribAuthorization,
    CommentAuthorization,
    UserAuthorization,
    UserProfileAuthorization,
    UserFollowsAuthorization,
    UserFollowersAuthorization)

from tribus.config.base import CHARMSDIR
from tribus.common.utils import get_path
from tribus.common.charms.repository import LocalCharmRepository
from tribus.common.charms.url import CharmCollection


class UserResource(ModelResource):
    user_profile = OneToOneField(
        to='tribus.web.api.resources.UserProfileResource',
        attribute='user_profile',
        related_name='user')

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user/details'
        ordering = ['id']
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get', 'patch']
        filtering = {'id': ALL_WITH_RELATIONS}
        authorization = UserAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()


class UserProfileResource(ModelResource):
    user = OneToOneField(
        to='tribus.web.api.resources.UserResource',
        attribute='user',
        related_name='user_profile')
    follows = ManyToManyField(
        to='tribus.web.api.resources.UserResource',
        attribute='follows',
        related_name='user_profile',
        blank=True,
        null=True)
    followers = ManyToManyField(
        to='tribus.web.api.resources.UserResource',
        attribute='followers',
        related_name='user_profile',
        blank=True,
        null=True)

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user/profile'
        ordering = ['id']
        allowed_methods = ['get', 'patch']
        filtering = {'id': ALL_WITH_RELATIONS}
        authorization = UserProfileAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()


class UserFollowersResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user/followers'
        ordering = ['id']
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
        filtering = {'id': ALL_WITH_RELATIONS}
        authorization = UserFollowersAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()


class UserFollowsResource(ModelResource):

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user/follows'
        ordering = ['id']
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
        filtering = {'id': ALL_WITH_RELATIONS}
        authorization = UserFollowsAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()


class TimeLineResource(ModelResource):
    user_id = fields.ToOneField(UserResource, attribute='user_id', full=True)
    trib_pub_date = fields.DateTimeField(attribute='trib_pub_date')
    trib_content = fields.CharField(attribute='trib_content')

    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'user/timeline'
        ordering = ['trib_pub_date']
        allowed_methods = ['get']
        authorization = TimelineAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()


class TribResource(ModelResource):
    user_id = fields.ToOneField(UserResource, attribute='user_id', full=True)
    trib_pub_date = fields.DateTimeField(attribute='trib_pub_date')
    trib_content = fields.CharField(attribute='trib_content')

    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'user/tribs'
        ordering = ['trib_pub_date']
        allowed_methods = ['get', 'post', 'delete']
        filtering = {'user_id': ALL_WITH_RELATIONS}
        authorization = TribAuthorization()
        authentication = SessionAuthentication()
        validation = CleanedDataFormValidation(form_class=TribForm)
        cache = NoCache()


class CommentResource(ModelResource):
    user_id = fields.ToOneField(UserResource, attribute='user_id', full=True)
    trib_id = fields.ToOneField(TribResource, attribute='trib_id', full=True)
    comment_pub_date = fields.DateTimeField(attribute='comment_pub_date')
    comment_content = fields.CharField(attribute='comment_content')

    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'tribs/comments'
        ordering = ['comment_pub_date']
        allowed_methods = ['get', 'post', 'delete']
        filtering = {'trib_id': ALL_WITH_RELATIONS}
        authorization = CommentAuthorization()
        authentication = SessionAuthentication()
        validation = CleanedDataFormValidation(form_class=CommentForm)
        cache = NoCache()


class SearchUserResource(Resource):
    name = fields.CharField(attribute='autoname')
    description = fields.CharField(attribute='description')

    class Meta:
        resource_name = 'search'
        object_class = User

    def obj_get_list(self, bundle, **kwargs):
        filters = {}
        if hasattr(bundle.request, 'GET'):
            filters = bundle.request.GET.copy()
        filters.update(kwargs)
        if 'q' in filters:
            sqs = SearchQuerySet().models(
                User).autocomplete(autoname=filters['q'])[:5]
        else:
            sqs = EmptySearchQuerySet()

        paginator = Paginator(filter(None, sqs), 5)

        try:
            page = paginator.page(1)
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        return page


class SearchPackageResource(Resource):
    name = fields.CharField(attribute='autoname')
    description = fields.CharField(attribute='description')

    class Meta:
        resource_name = 'search'
        object_class = Package

    def obj_get_list(self, bundle, **kwargs):
        filters = {}
        if hasattr(bundle.request, 'GET'):
            filters = bundle.request.GET.copy()
        filters.update(kwargs)
        if 'q' in filters:
            sqs = SearchQuerySet().models(
                Package).autocomplete(autoname=filters['q'])[:5]
        else:
            sqs = EmptySearchQuerySet()

        paginator = Paginator(filter(None, sqs), 5)

        try:
            page = paginator.page(int(bundle.request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        return page


class SearchResource(Resource):
    users = fields.ListField()
    packages = fields.ListField()

    class Meta:
        resource_name = 'search'
        allowed_methods = ['get']
        include_resource_uri = False

    def dehydrate_users(self, bundle):
        if switch_is_active('profile'):
            return [{'fullname': unicode(obj.fullname),
                     'username': unicode(obj.username)}
                     for obj in bundle.obj['users']]
        else:
            return []

    def dehydrate_packages(self, bundle):
        if switch_is_active('cloud'):
            return [{'name': str(obj.name)} for obj in bundle.obj['packages']]
        else:
            return []

    def get_object_list(self, bundle):
        d = {}
        if switch_is_active('cloud'):
            d['packages'] = SearchPackageResource().obj_get_list(bundle)
        if switch_is_active('profile'):
            d['users'] = SearchUserResource().obj_get_list(bundle)

        return [d]

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle)


class CharmObject(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data


class CharmListResource(Resource):
    charms = fields.CharField(attribute='charms')

    class Meta:
        resource_name = 'charms/list'
        object_class = CharmObject

    def get_object_list(self, bundle):

        CHARM = LocalCharmRepository(CHARMSDIR)

        charms = CHARM.list()

        l = []

        for ch in charms:
            l.append(ch.metadata.name)

        return [CharmObject({
                    'charms': l
                })]

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle)


class CharmMetadataResource(Resource):
    name = fields.CharField(attribute='name')
    summary = fields.CharField(attribute='summary')
    maintainer = fields.CharField(attribute='maintainer')
    description = fields.CharField(attribute='description')

    class Meta:
        resource_name = 'charms/metadata'
        object_class = CharmObject

    def get_object_list(self, bundle):

        if hasattr(bundle.request, 'GET'):
            charm_name = bundle.request.GET.get('name', None)

        CHARM = CharmDirectory(get_path([CHARMSDIR, charm_name]))

        return [CharmObject({
                    'name': CHARM.metadata.name,
                    'summary': CHARM.metadata.summary,
                    'maintainer': CHARM.metadata.maintainer,
                    'description': CHARM.metadata.description,
                })]

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle)


class CharmConfigResource(Resource):
    config = fields.CharField(attribute='config')

    class Meta:
        resource_name = 'charms/config'
        object_class = CharmObject

    def get_object_list(self, bundle):

        if hasattr(bundle.request, 'GET'):
            charm_name = bundle.request.GET.get('name', None)

        CHARM = CharmDirectory(get_path([CHARMSDIR, charm_name]))

        return [CharmObject({
                    'config': CHARM.config._data,
                })]

    def obj_get_list(self, bundle, **kwargs):
        return self.get_object_list(bundle)