#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 by the Babel Team, see COPYING for more information.
# All Rights Reserved.
#
# This file is part of Tribus.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#  3. The name of the author may not be used to endorse or promote
#     products derived from this software without specific prior
#     written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR "AS IS" AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
# IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

tribus.common.setup.message_extractors
======================================

This module contains message extractors that work with babel.

"""

from django.template import Lexer, TOKEN_TEXT, TOKEN_VAR, TOKEN_BLOCK
from django.utils.translation.trans_real import (inline_re, block_re,
                                                 endblock_re, plural_re,
                                                 constant_re)


def django(fileobj, keywords, comment_tags, options):
    """

    Extract messages from Django template files.

    :param fileobj: the file-like object the messages should be extracted from.
    :param keywords: a list of keywords (i.e. function names) that should
                     be recognized as translation functions.
    :param comment_tags: a list of translator tags to search for and
                         include in the results.
    :param options: a dictionary of additional options (optional)
    :return: an iterator over ``(lineno, funcname, message, comments)``
             tuples
    :rtype: ``iterator``

    """
    intrans = False
    inplural = False
    singular = []
    plural = []
    lineno = 1

    for t in Lexer(fileobj.read().decode('utf-8'), None).tokenize():
        lineno += t.contents.count('\n')
        if intrans:
            if t.token_type == TOKEN_BLOCK:
                endbmatch = endblock_re.match(t.contents)
                pluralmatch = plural_re.match(t.contents)
                if endbmatch:
                    if inplural:
                        yield lineno, 'ngettext', (unicode(''.join(singular)),
                                                   unicode(''.join(plural))), []
                    else:
                        yield lineno, None, unicode(''.join(singular)), []
                    intrans = False
                    inplural = False
                    singular = []
                    plural = []
                elif pluralmatch:
                    inplural = True
                else:
                    raise SyntaxError('Translation blocks must not include '
                                      'other block tags: %s' % t.contents)
            elif t.token_type == TOKEN_VAR:
                if inplural:
                    plural.append('%%(%s)s' % t.contents)
                else:
                    singular.append('%%(%s)s' % t.contents)
            elif t.token_type == TOKEN_TEXT:
                if inplural:
                    plural.append(t.contents)
                else:
                    singular.append(t.contents)
        else:
            if t.token_type == TOKEN_BLOCK:
                imatch = inline_re.match(t.contents)
                bmatch = block_re.match(t.contents)
                cmatches = constant_re.findall(t.contents)
                if imatch:
                    g = imatch.group(1)
                    if g[0] == '"':
                        g = g.strip('"')
                    elif g[0] == "'":
                        g = g.strip("'")
                    yield lineno, None, unicode(g), []
                elif bmatch:
                    for fmatch in constant_re.findall(t.contents):
                        yield lineno, None, unicode(fmatch), []
                    intrans = True
                    inplural = False
                    singular = []
                    plural = []
                elif cmatches:
                    for cmatch in cmatches:
                        yield lineno, None, unicode(cmatch), []
            elif t.token_type == TOKEN_VAR:
                parts = t.contents.split('|')
                cmatch = constant_re.match(parts[0])
                if cmatch:
                    yield lineno, None, unicode(cmatch.group(1)), []
                for p in parts[1:]:
                    if p.find(':_(') >= 0:
                        p1 = p.split(':', 1)[1]
                        if p1[0] == '_':
                            p1 = p1[1:]
                        if p1[0] == '(':
                            p1 = p1.strip('()')
                        if p1[0] == "'":
                            p1 = p1.strip("'")
                        elif p1[0] == '"':
                            p1 = p1.strip('"')
                        yield lineno, None, unicode(p1), []
