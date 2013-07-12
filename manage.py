#!/usr/bin/env python
# -*- coding: utf-8 -*-

if __name__ == "__main__":

    import os
    import sys

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tribus.config.web")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
