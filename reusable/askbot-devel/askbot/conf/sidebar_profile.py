"""
Sidebar settings
"""
from askbot.conf.settings_wrapper import settings
from askbot.deps.livesettings import ConfigurationGroup
from askbot.deps.livesettings import values
from django.utils.translation import ugettext_lazy as _
from askbot.conf.super_groups import CONTENT_AND_UI

SIDEBAR_PROFILE = ConfigurationGroup(
                    'SIDEBAR_PROFILE',
                    _('User profile sidebar'),
                    super_group = CONTENT_AND_UI
                )

settings.register(
    values.LongStringValue(
        SIDEBAR_PROFILE,
        'SIDEBAR_PROFILE',
        description = _('Custom sidebar'),
        default = '',
        help_text = _(
                    'Use this area to enter content at the TOP of the sidebar'
                    'in HTML format.   When using this option '
                    '(as well as the sidebar footer), please '
                    'use the HTML validation service to make sure that '
                    'your input is valid and works well in all browsers.'
        )
    )
)


settings.register(
    values.BooleanValue(
        SIDEBAR_PROFILE,
        'SIDEBAR_PROFILE_ANON_ONLY',
        description=_('Show above only to anonymous users'),
        default=False
    )
)
