"""
Q&A forum flatpages (about, etc.)
"""
from askbot.conf.settings_wrapper import settings
from askbot.deps.livesettings import ConfigurationGroup, LongStringValue
from askbot.conf.super_groups import CONTENT_AND_UI
from django.utils.translation import ugettext_lazy as _

FLATPAGES = ConfigurationGroup(
                'FLATPAGES',
                _('Messages and pages - about, privacy policy, etc.'),
                super_group = CONTENT_AND_UI
            )

settings.register(
    LongStringValue(
        FLATPAGES,
        'FORUM_ABOUT',
        description=_('Text of the Q&A forum About page (html format)'),
        help_text=\
        _(
            'Save, then <a href="http://validator.w3.org/">'
            'use HTML validator</a> on the "about" page to check your input.'
        )
    )
)

settings.register(
    LongStringValue(
        FLATPAGES,
        'FORUM_FAQ',
        description=_('Text of the Q&A forum FAQ page (html format)'),
        help_text=\
        _(
            'Save, then <a href="http://validator.w3.org/">'
            'use HTML validator</a> on the "faq" page to check your input.'
        )
    )
)

settings.register(
    LongStringValue(
        FLATPAGES,
        'QUESTION_INSTRUCTIONS',
        description=_('Instructions on how to ask questions'),
        help_text=\
        _(
            'HTML is allowed. Save, then <a href="http://validator.w3.org/">'
            'use HTML validator</a> on the "ask" page to check your input.'
        )

    )
)

settings.register(
    LongStringValue(
        FLATPAGES,
        'FORUM_PRIVACY',
        description=_('Text of the Q&A forum Privacy Policy (html format)'),
        help_text=\
        _(
            'Save, then <a href="http://validator.w3.org/">'
            'use HTML validator</a> on the "privacy" page to check your input.'
        )
    )
)

#todo: merge this with mandatory tags
settings.register(#this field is not editable manually
    LongStringValue(
        FLATPAGES,
        'CATEGORY_TREE',
        description = 'Category tree',#no need to translate
        default = '[["dummy",[]]]',#empty array of arrays in json
        help_text=_('Do not edit this field manually!!!')
        #hidden = True
    )
)
