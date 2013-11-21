
from social_auth.models import UserSocialAuth

from tribus.web.registration.ldap.models import LdapUser
from tribus.web.registration.ldap.utils import create_ldap_user

def create_user(backend, details, response, uid, username, user=None, *args,
                **kwargs):
    """Create user. Depends on get_username pipeline."""
    if user:
        return {'user': user}
    if not username:
        return None
    print backend, details, response, uid, username, user
    # Avoid hitting field max length
    email = details.get('email')
    original_email = None

    if email and UserSocialAuth.email_max_length() < len(email):
        original_email = email
        email = ''

    if UserSocialAuth.username_max_length() < len(username):
        username = username[:UserSocialAuth.username_max_length()]

    user = UserSocialAuth.create_user(username=username, email=email)
    ldapuser = create_ldap_user(user)

    return {
        'user': user,
        'original_email': original_email,
        'is_new': True
    }