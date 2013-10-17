#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tastypie.authentication import SessionAuthentication
from tastypie.cache import NoCache
from tastypie_mongoengine.resources import MongoEngineResource
from tastypie.resources import ModelResource



from tribus.web.api.authorization import (TimelineAuthorization, TribAuthorization, UserAuthorization)
from tribus.web.documents import Trib
from django.contrib.auth.models import User


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user/follows'
        allowed_methods = ['get']
        authorization = UserAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()        



class TribResource(MongoEngineResource):
    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'user/tribs'
        ordering = ['trib_pub_date']
        allowed_methods = ['get', 'post', 'delete']
        authorization = TribAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()

    '''
    {
    "author_first_name": "Luis Alejandro",
    "author_id": 2,
    "author_last_name": "Martínez Faneyth",
    "author_username": "luis",
    "retribs": [],
    "trib_content": "hola",
    "trib_pub_date": "2013-09-25T00:03:55.804000"
    }

    curl --dump-data -X POST --data '{"author_first_name": "Luis Alejandro", "author_id": 2, "author_last_name": "Martínez Faneyth", "author_username": "luis", "retribs": [], "trib_content": "hola", "trib_pub_date": "2013-09-25T00:03:55.804000"}'
    '''

class TimelineResource(MongoEngineResource):
    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'user/timeline'
        ordering = ['trib_pub_date']
        allowed_methods = ['get']
        authorization = TimelineAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()