#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform

def get_local_arch():

    arch = platform.architecture()

    if arch[0] == '64bit':
        return 'amd64'

    elif arch[0] == '32bit':
        return 'i386'

    else:
        return None
