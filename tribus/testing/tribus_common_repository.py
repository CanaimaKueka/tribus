#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Desarrolladores de Tribus
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

tribus.tests.tribus_common_recorder
================================

These are the tests for the tribus.common.recorder module.

'''

import os
import gzip
import email.Utils
from fabric.api import env, lcd, local, settings
from debian import deb822
from django.test import TestCase
from doctest import DocTestSuite
from tribus.__init__ import BASEDIR
from tribus.common.utils import get_path
from tribus.web.cloud.models import Package

SAMPLESDIR = get_path([BASEDIR, "tribus", "testing", "samples" ])
FIXTURES = get_path([BASEDIR, "tribus", "testing", "fixtures" ])

class RepositoryFunctions(TestCase):
    
    def setUp(self):
        pass        


    def tearDown(self):
        pass
    
    def test_init_sample_packages(self):
        from tribus.common.repository import init_sample_packages
        from tribus.config.pkgrecorder import CANAIMA_ROOT, SAMPLES_DIR

        dist = 'kerepakupai'
        
        # 1) Hace falta un repositorio
        env.micro_repository_path = os.path.join('/', 'tmp', 'tmp_repo')
        env.micro_repository_conf = os.path.join('/', 'tmp', 'tmp_repo', 'conf')
        env.distributions_path = os.path.join(env.micro_repository_path, 'distributions')
        
        # 2) Hace falta descargar los samples desde un repositorio
        env.samples_dir = SAMPLESDIR
        env.packages_dir = os.path.join(SAMPLESDIR, 'package_lists')
        env.pcache = os.path.join('/', 'tmp', 'pcache')
        
        # Necesito un paquete por cada componente, arquitectura y rama =/ buff que trabajo tan ladilla es hacer pruebas
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    def test_download_sample_packages(self):
        pass
    
    
    
        
        
