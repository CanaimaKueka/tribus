#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Desarrolladores de Tribus
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


from tastypie.api import Api

from tribus.web.api.resources import TribResource, TimelineResource, CommentResource,\
 UserResource, SearchResource, UserProfileResource, UserFollowsResource, UserFollowersResource

api_01 = Api(api_name='0.1')
api_01.register(UserFollowsResource())
api_01.register(UserFollowersResource())
api_01.register(TribResource())
api_01.register(CommentResource())
api_01.register(TimelineResource())
api_01.register(UserResource())
api_01.register(UserProfileResource())
api_01.register(SearchResource())
