from uuid import uuid4

from social_auth.models import UserSocialAuth
from tribus.web.user.models import LdapUser

def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user:
        return {'user': user}
    if not username:
        return None

    # Avoid hitting field max length
    email = details.get('email')
    original_email = None
    if email and UserSocialAuth.email_max_length() < len(email):
        original_email = email
        email = ''

    user = UserSocialAuth.create_user(username=username, email=email)
    ldapuser = create_ldap_user(user)

    return {
        'user': user,
        'original_email': original_email,
        'is_new': True
    }


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
    l.description = 'Created by Tribus'
    l.save()

    return l


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

