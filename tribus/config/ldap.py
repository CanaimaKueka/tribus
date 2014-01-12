#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldap://localhost"
AUTH_LDAP_BASE = "dc=tribus,dc=org"
AUTH_LDAP_BIND_DN = "cn=admin," + AUTH_LDAP_BASE
AUTH_LDAP_BIND_PASSWORD = "tribus"
AUTH_LDAP_USER_DN_TEMPLATE = 'uid=%(user)s,' + AUTH_LDAP_BASE

# Set up the basic group parameters.
# AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=django,ou=groups,dc=example,dc=com",
#    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
#)
# AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")

# Simple group restrictions
# AUTH_LDAP_REQUIRE_GROUP = "cn=enabled,ou=django,ou=groups,dc=example,dc=com"
# AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=django,ou=groups,dc=example,dc=com"

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "password": "userPassword",
    "email": "mail"
}

# AUTH_LDAP_PROFILE_ATTR_MAP = {
#    "employee_number": "employeeNumber"
#}

# AUTH_LDAP_USER_FLAGS_BY_GROUP = {
#    "is_active": "cn=active,ou=django,ou=groups,dc=example,dc=com",
#    "is_staff": "cn=staff,ou=django,ou=groups,dc=example,dc=com",
#    "is_superuser": "cn=superuser,ou=django,ou=groups,dc=example,dc=com"
#}

# AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
#    "is_awesome": "cn=awesome,ou=django,ou=groups,dc=example,dc=com",
#}

# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = False

# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600
