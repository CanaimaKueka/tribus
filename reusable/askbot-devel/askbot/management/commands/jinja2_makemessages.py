"""
Taken from Coffin
http://github.com/miracle2k/coffin/raw/master/coffin/management/commands/makemessages.py
added support for the pluralization

Jinja2's i18n functionality is not exactly the same as Django's.
In particular, the tags names and their syntax are different:

  1. The Django ``trans`` tag is replaced by a _() global.
  2. The Django ``blocktrans`` tag is called ``trans``.

(1) isn't an issue, since the whole ``makemessages`` process is based on
converting the template tags to ``_()`` calls. However, (2) means that
those Jinja2 ``trans`` tags will not be picked up my Django's
``makemessage`` command.

There aren't any nice solutions here. While Jinja2's i18n extension does
come with extraction capabilities built in, the code behind ``makemessages``
unfortunately isn't extensible, so we can:

  * Duplicate the command + code behind it.
  * Offer a separate command for Jinja2 extraction.
  * Try to get Django to offer hooks into makemessages().
  * Monkey-patch.

We are currently doing that last thing. It turns out there we are lucky
for once: It's simply a matter of extending two regular expressions.
Credit for the approach goes to:
http://stackoverflow.com/questions/2090717/getting-translation-strings-for-jinja2-templates-integrated-with-django-1-x
"""

import re
from django.core.management.commands import makemessages
from django.utils.translation import trans_real


class Command(makemessages.Command):

    def handle(self, *args, **options):
        old_endblock_re = trans_real.endblock_re
        old_block_re = trans_real.block_re
        old_plural_re = trans_real.plural_re
        # Extend the regular expressions that are used to detect
        # translation blocks with an "OR jinja-syntax" clause.
        trans_real.endblock_re = re.compile(
            trans_real.endblock_re.pattern + '|' + r"""^-?\s*endtrans\s*-?$""")
        trans_real.block_re = re.compile(
            trans_real.block_re.pattern + '|' + r"""^-?\s*trans(?:\s*|$)""")
        trans_real.plural_re = re.compile(
            trans_real.plural_re.pattern + '|' + r"""^-?\s*pluralize(\s+\w+)?\s*-?$""")

        try:
            super(Command, self).handle(*args, **options)
        finally:
            trans_real.endblock_re = old_endblock_re
            trans_real.block_re = old_block_re
            trans_real.plural_re = old_plural_re
