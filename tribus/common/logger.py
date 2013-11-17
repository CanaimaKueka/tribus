#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_logger():

    from logging import getLogger
    from tribus.config.logger import LOGGING

    try:
        from logging.config import dictConfig
    except ImportError:
        from tribus.common.dictconfig import dictConfig

    dictConfig(LOGGING)
    return getLogger('tribus')
