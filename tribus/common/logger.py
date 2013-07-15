#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_logger():
    import logging
    import logging.config
    from tribus.config.logger import LOGGING
    logging.config.dictConfig(LOGGING)
    return logging.getLogger('tribus')
