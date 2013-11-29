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


from tribus.web.registration.ldap.models import LdapUser

def create_ldap_user(u):
    l = LdapUser()
    l.first_name = u.first_name
    l.last_name = u.last_name
    l.full_name = u.first_name+' '+u.last_name
    l.email = u.email
    l.username = u.username
    l.password = u.password
    l.uid = get_last_uid()
    l.group = 1234
    l.home_directory = '/home/'+u.username
    l.login_shell = '/bin/false'
    l.description = u.description
    l.save()

    return l


def edit_ldap_user(u):
    l = LdapUser.objects.get(username = u.username)
    l.email = u.email
    l.description = u.description
    l.save()
    print u.username ," Actualizado"

#def create_ldap_password(password, algorithm='SSHA', salt=None):
#    """
#    Encrypts a password as used for an ldap userPassword attribute.
#    """
#    s = hashlib.sha1()
#    s.update(password)

#    if algorithm == 'SSHA':
#        if salt is None:
#            salt = ''.join([random.choice(string.letters) for i in range(8)])

#        s.update(salt)
#        return '{SSHA}%s' % base64.encodestring(s.digest() + salt).rstrip()
#    else:
#        raise NotImplementedError


def get_last_uid():
    try:
        u = LdapUser.objects.get(username='maxUID')
    except LdapUser.DoesNotExist:
        return create_last_uid_entry()

    lastuid = int(u.uid)
    u.uid = int(u.uid)+1
    u.save()

    return lastuid


def create_last_uid_entry():
    maxuid = LdapUser()
    maxuid.first_name = 'max'
    maxuid.last_name = 'UID'
    maxuid.full_name = maxuid.first_name+maxuid.last_name
    maxuid.email = ''
    maxuid.username = 'maxUID'
    maxuid.password = ''
    maxuid.uid = 2001
    maxuid.group = 1234
    maxuid.home_directory = '/home/'+maxuid.username
    maxuid.login_shell = '/bin/false'
    maxuid.description = 'Created by Tribus'
    maxuid.save()

    return 2000

