#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from tastypie.cache import NoCache
from tastypie.authentication import SessionAuthentication, Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
from tastypie.bundle import Bundle
from tastypie import fields
from tastypie_mongoengine.resources import MongoEngineResource
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404

from tastypie.resources import ModelResource, Resource
from tastypie.fields import ManyToManyField, OneToOneField
from tribus.web.api.authorization import (TimelineAuthorization, TribAuthorization, CommentAuthorization, UserAuthorization, UserProfileAuthorization)
from tribus.web.documents import Trib, Comment

from tastypie_mongoengine.fields import EmbeddedListField
from django.contrib.auth.models import User
from tribus.web.profile.models import UserProfile

from haystack.query import SearchQuerySet
from tribus.web.packages.models import Package

class UserResource(ModelResource):
    user_profile = OneToOneField(to='tribus.web.api.resources.UserProfileResource', attribute='user_profile', related_name='user')

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user/details'
        ordering = ['id']
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get', 'patch']
        filtering = { 'id': ALL_WITH_RELATIONS }
        authorization = UserAuthorization()
        authentication = Authentication()
        cache = NoCache()


class UserProfileResource(ModelResource):
    user = OneToOneField(to='tribus.web.api.resources.UserResource', attribute='user', related_name='user_profile')
    follows = ManyToManyField(to='tribus.web.api.resources.UserResource', attribute='follows', related_name='user_profile', blank=True, null=True)
    followers = ManyToManyField(to='tribus.web.api.resources.UserResource', attribute='followers', related_name='user_profile', blank=True, null=True)

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'user/profile'
        ordering = ['id']
        allowed_methods = ['get', 'patch']
        filtering = { 'id': ALL_WITH_RELATIONS }
        authorization = UserProfileAuthorization()
        authentication = Authentication()
        cache = NoCache()


class TimelineResource(MongoEngineResource):
    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'user/timeline'
        ordering = ['trib_pub_date']
        allowed_methods = ['get']
        authorization = TimelineAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()


class TribResource(MongoEngineResource):
    class Meta:
        queryset = Trib.objects.all()
        resource_name = 'user/tribs'
        ordering = ['trib_pub_date']
        allowed_methods = ['get', 'post', 'delete']
        filtering = { 'author_id': ALL_WITH_RELATIONS }
        authorization = TribAuthorization()

        
        #puedes ver los tribs asi no estes logueado =P
        authentication = Authentication()
        cache = NoCache()


class CommentResource(MongoEngineResource):
    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'tribs/comments'
        ordering = ['comment_pub_date']
        allowed_methods = ['get', 'post', 'delete']
        filtering = { 'trib_id': ALL_WITH_RELATIONS }
        authorization = CommentAuthorization()
        authentication = SessionAuthentication()
        cache = NoCache()

        '''
curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"author_id": 2, "author_username": "luis", "author_first_name": "Luis Alejandro", "author_last_name": "Martínez Faneyth", "author_email": "luis@huntingbears.com.ve", "comment_content": "hola", "comment_pub_date": "2013-09-25T00:03:55.804000", "trib_id": "525b5e4fea10251d9969b97e"}' http://localhost:8000/api/0.1/comments/525b5e4fea10251d9969b97e
        '''
        
class HayStackObject(object):
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

class SearchResource(Resource):
    dest = fields.CharField(attribute='destination')
    type = fields.CharField(attribute='model_name')
    auto_name = fields.CharField(attribute='auto_name')
    
    class Meta:
        resource_name = 'search'
        object_class = SearchQuerySet
        authorization = Authorization()
        
    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.pk
        else:
            kwargs['pk'] = bundle_or_obj.obj.pk
 
        return kwargs

    def obj_get_list(self, bundle, **kwargs):
        filters = {}
        if hasattr(bundle.request, 'GET'):
            # Grab a mutable copy.
            filters = bundle.request.GET.copy()
        
        filters.update(kwargs)
        if filters.has_key('q'):
            sqs = SearchQuerySet().models(User).autocomplete(auto_name = filters['q'])
        else:
            sqs = SearchQuerySet().models(User) 
        return sqs

'''
class PackageResource(ModelResource):
    class Meta:
        queryset = Package.objects.all()
        resource_name = 'search'
        ordering = ['Package']
        fields = ['Package']
        allowed_methods = ['get']
          
    def prepend_urls(self):
         
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
        ]
          
    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get']) 
        self.is_authenticated(request) 
        self.throttle_check(request)
        sqs = SearchQuerySet().models(Package, User).load_all().autocomplete(auto_name=request.GET.get('q', ''))
        paginator = Paginator(sqs, 10)
             
        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")
  
        objects = []
             
        for result in page.object_list:
            bundle = self.build_bundle(obj=result.object, request=request)
            print "1", bundle
            bundle = self.full_dehydrate(bundle)
            print "2", bundle
            bundle.data['type'] = result.model_name
            print "3", bundle
            objects.append(bundle)
  
        object_list = {
            'objects': objects,
        }
          
        print "Object list -> %s" % object_list
          
        self.log_throttled_access(request)
        return self.create_response(request, object_list)

'''
