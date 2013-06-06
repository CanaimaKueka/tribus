from askbot.conf.settings_wrapper import settings
from askbot.conf.super_groups import LOGIN_USERS_COMMUNICATION
from askbot.deps import livesettings
from django.utils.translation import ugettext_lazy as _

ACCESS_CONTROL = livesettings.ConfigurationGroup(
                    'ACCESS_CONTROL',
                    _('Access control settings'),
                    super_group = LOGIN_USERS_COMMUNICATION
                )

settings.register(
    livesettings.BooleanValue(
        ACCESS_CONTROL,
        'ASKBOT_CLOSED_FORUM_MODE',
        default=False,
        description=_('Allow only registered user to access the forum'),
    )
)

EMAIL_VALIDATION_CASE_CHOICES = (
    ('nothing', _('nothing - not required')),
    ('see-content', _('access to content')),
    #'post-content', _('posting content'),
)

settings.register(
    livesettings.StringValue(
        ACCESS_CONTROL,
        'REQUIRE_VALID_EMAIL_FOR',
        default='nothing',
        choices=EMAIL_VALIDATION_CASE_CHOICES,
        description=_(
            'Require valid email for'
        )
    )
)

settings.register(
    livesettings.LongStringValue(
        ACCESS_CONTROL,
        'ALLOWED_EMAILS',
        default='',
        description=_('Allowed email addresses'),
        help_text=_('Please use space to separate the entries')
    )
)

settings.register(
    livesettings.LongStringValue(
        ACCESS_CONTROL,
        'ALLOWED_EMAIL_DOMAINS',
        default='',
        description=_('Allowed email domain names'),
        help_text=_('Please use space to separate the entries, do not use the @ symbol!')
    )
)
