#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tastypie.authorization import Authorization
from tastypie.authentication import SessionAuthentication
from tastypie_mongoengine.resources import MongoEngineResource
from tastypie.resources import ModelResource, ALL
from django.contrib.auth.models import User
from tribus.web.models import Trib

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        # excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
        }


class TribResource(MongoEngineResource):
    
    class Meta:
        queryset = Trib.objects.all()
        excludes = ['id']
        resource_name = 'trib'
        include_resource_uri = False
        authorization = Authorization()
        authentication = SessionAuthentication()
        filtering = {
            'trib_id': ALL,
        }
    '''
    {
    'author_id': 1,
    'author_nick': 'luis',
    'author_first_name': 'Menganito',
    'author_last_name': 'Fulanito',
    'trib_id': 1,
    'trib_content': 'Hola, vengo a flotar.',
    'trib_pub_date': '2013-05-26T05:00:00.000Z',
    'retribs': [1, 2, 3]
    }
    '''
    '''
    curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"author_id": 1, "author_nick": "luis", "author_first_name": "Menganito", "author_last_name": "Fulanito", "trib_id": 1, "trib_content": "Hola, vengo a flotar.", "trib_pub_date": "2013-05-26T05:00:00.000Z", "retribs": [1, 2, 3]}' http://localhost:8000/api/0.1/trib/
    '''
    '''
    curl --dump-header - -H "Content-Type: application/json" -X DELETE  http://localhost:8000/api/0.1/trib/523f66e6ea10251a1b8664af/
    '''