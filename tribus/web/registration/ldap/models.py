from django.conf import settings

from ldapdb.models.base import Model
from ldapdb.models.fields import CharField, IntegerField, ListField


# This class comes from django-ldapdb's examples
# https://github.com/jlaine/django-ldapdb
class LdapUser(Model):
    """
    Class for representing an LDAP user entry.
    """

    class Meta:
        managed = False

    base_dn = settings.AUTH_LDAP_BASE
    object_classes = [
       'posixAccount', 'shadowAccount', 'inetOrgPerson',
       'top', 'person', 'organizationalPerson'
       ]

    first_name = CharField(db_column='givenName')
    last_name = CharField(db_column='sn')
    full_name = CharField(db_column='cn')
    email = CharField(db_column='mail')
    username = CharField(db_column='uid', primary_key=True)
    password = CharField(db_column='userPassword')
    uid = IntegerField(db_column='uidNumber', unique=True)
    group = IntegerField(db_column='gidNumber')
    home_directory = CharField(db_column='homeDirectory')
    login_shell = CharField(db_column='loginShell', default='/bin/bash')
    description = CharField(db_column='description')

    def __str__(self):
       return self.uid

    def __unicode__(self):
       return self.full_name


class LdapGroup(Model):
    """
    Class for representing an LDAP group entry.
    """
    # LDAP meta-data
    base_dn = "ou=groups,dc=nodomain"
    object_classes = ['posixGroup']

    # posixGroup attributes
    gid = IntegerField(db_column='gidNumber', unique=True)
    name = CharField(db_column='cn', max_length=200, primary_key=True)
    usernames = ListField(db_column='memberUid')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

