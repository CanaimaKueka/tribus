
from tribus.web.registration.ldap.models import LdapUser

def create_ldap_user(u):
    l = LdapUser()
    l.first_name = u.first_name or 'unknown'
    l.last_name = u.last_name or 'unknown'
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

