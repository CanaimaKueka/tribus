#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
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

# from tribus.config.base import CONTAINERS

from __future__ import with_statement, print_function

import os
import re
import sys
import shutil
from subprocess import Popen, PIPE
from distutils.spawn import find_executable

from tribus.config.base import CONTAINERS
from tribus.config.distributions import DISTRIBUTIONS
from tribus.common.errors import CannotIdentifyDistribution, UnsupportedDistribution
from tribus.common.utils import flatten_list
from tribus.common.logger import get_logger

log = get_logger()


class DependencySolver(object):

    def __init__(self, containers, distributions):
        self.distname = ''
        self.codename = ''
        self.release_data = {}
        self.dpkg_origins_data = {}
        self.apt_policy_data = []
        self.lsb = find_executable('lsb_release')
        self.os_release = '/etc/os-release'
        self.lsb_release = '/etc/lsb-release'
        self.arch_release = '/etc/arch-release'
        self.fedora_release = '/etc/fedora-release'
        self.centos_release = '/etc/centos-release'
        self.gentoo_release = '/etc/gentoo-release'
        self.redhat_release = '/etc/redhat-release'
        self.debian_release = '/etc/debian_version'
        self.dpkg_origins = '/etc/dpkg/origins/default'
        self.env = os.environ.copy()
        self.env['LC_ALL'] = 'C'

        self.longnames = {
            'v': 'version',
            'o': 'origin',
            'a': 'suite',
            'c': 'component',
            'l': 'label'
        }

        self.containers = containers
        self.distributions = distributions
        self.codenames = {}
        self.revcodenames = {}

    def codename_index(self, x):

        suite = x[1].get('suite')
        order = list(self.distributions[self.distname]['codenames'].items())
        order.sort()
        order = list(flatten_list(list(zip(*order))[1]))

        if suite:
            if suite in order:
                return int(len(order) - order.index(suite))
            else:
                return suite
        return 0

    def parse_release(self, release):

        try:
            with open(release) as contentlist:
                for j in contentlist.read().split('\n'):
                    if re.findall('=', j):
                        key = j.split('=')[0].strip().upper()
                        value = j.split('=')[1].strip('"').lower()
                        self.release_data[key] = value
                    elif j:
                        self.release_data['PRETTY_NAME'] = j.lower()

        except IOError as msg:
            print(msg)

        return self.release_data

    def parse_dpkg_origins(self, origins):

        try:
            with open(origins) as contentlist:
                for j in contentlist.read().split('\n'):
                    if re.findall(':', j):
                        key = j.split(':')[0].strip().upper()
                        value = j.split(':')[1].strip().lower()

                        self.dpkg_origins_data[key] = value
                    elif j:
                        self.dpkg_origins_data['PRETTY_NAME'] = j.lower()

        except IOError as msg:
            print(msg)

        return self.dpkg_origins_data

    def parse_apt_policy(self):

        retval = {}
        policy = Popen(args=['apt-cache', 'policy'],
                       stdout=PIPE, stderr=PIPE, env=self.env,
                       close_fds=True).communicate()[0].decode('utf-8')

        for line in policy.split('\n'):
            line = line.strip()
            m = re.match(r'(-?\d+)', line)

            if m:
                priority = int(m.group(1))

            if line.startswith('release'):
                bits = line.split(' ', 1)

                if len(bits) > 1:

                    for bit in bits[1].split(','):
                        kv = bit.split('=', 1)

                        if len(kv) > 1:
                            k, v = kv[:2]

                            if k in self.longnames:
                                retval[self.longnames[k]] = v

                    self.apt_policy_data.append((priority, retval))
        return self.apt_policy_data

    def get_codename_from_apt(self, origin, component='main'):

        releases = self.parse_apt_policy()
        releases = [x for x in releases if (
            x[1].get('origin', '').lower() == origin and
            x[1].get('component', '').lower() == component and
            x[1].get('label', '').lower() == origin)]

        releases.sort(key=lambda tuple: tuple[0], reverse=True)

        max_priority = releases[0][0]
        releases = [x for x in releases if x[0] == max_priority]
        releases.sort(key=self.codename_index)

        return releases[0][1]['suite']

    def get_distro_data(self):

        log.info('Attempting to identify your distribution ...')

        if (not self.distname) and self.lsb:

            self.distname = Popen(
                args=['%s' % self.lsb, '-is'], stdout=PIPE, stderr=PIPE,
                env=self.env, close_fds=True
                ).communicate()[0].decode('utf-8').split('\n')[0].lower()

            self.codename = Popen(
                args=['%s' % self.lsb, '-cs'], stdout=PIPE, stderr=PIPE,
                env=self.env, close_fds=True
                ).communicate()[0].decode('utf-8').split('\n')[0].lower()

        if (not self.distname) and os.path.exists(self.arch_release):
            self.distname = 'arch'
            self.codename = '0.0'

        if (not self.distname) and os.path.exists(self.gentoo_release):
            self.distname = 'gentoo'
            self.codename = '0.0'

        if (not self.distname) and os.path.exists(self.fedora_release):
            self.parse_release(self.fedora_release)
            self.distname = self.release_data['PRETTY_NAME'].split()[0]
            self.codename = re.search(
                r'(.*)\(.*\)',
                self.release_data['PRETTY_NAME']).group(1).split()[-1]

        if (not self.distname) and os.path.exists(self.centos_release):
            self.parse_release(self.centos_release)
            self.distname = self.release_data['PRETTY_NAME'].split()[0]
            self.codename = self.release_data['PRETTY_NAME'].split()[-2]

        if (not self.distname) and os.path.exists(self.redhat_release):
            self.parse_release(self.redhat_release)
            self.distname = self.release_data['PRETTY_NAME'].split()[0]
            self.codename = self.release_data['PRETTY_NAME'].split()[-2]

        if (not self.distname) and os.path.exists(self.lsb_release):
            self.parse_release(self.lsb_release)
            self.distname = self.release_data['DISTRIB_ID']
            self.codename = self.release_data['DISTRIB_CODENAME']

        if (not self.distname) and os.path.exists(self.os_release):
            self.parse_release(self.os_release)
            self.distname = self.release_data['ID']
            self.codename = self.release_data['PRETTY_NAME']

            if self.distname == 'debian':
                self.codename = ''

            elif self.distname == 'elementary-os':
                self.codename = self.codename.split()[-1]

            else:
                self.codename = self.codename.split()[-2].strip('()')

        if (not self.distname) and os.path.exists(self.dpkg_origins):
            self.parse_dpkg_origins(self.dpkg_origins)
            self.distname = self.dpkg_origins_data['VENDOR']

        if self.distname and (not self.codename) \
           and os.path.exists(self.debian_release):
            self.parse_release(self.debian_release)

            if re.findall(r'.*/.*', self.release_data['PRETTY_NAME']):
                self.codename = self.get_codename_from_apt(self.distname)

            else:
                self.codename = self.release_data['PRETTY_NAME']

        if not (self.distname and self.codename):
            raise CannotIdentifyDistribution()

        self.codenames = self.distributions[self.distname]['codenames']

        for k, v in self.codenames.items():
            if len(v) > 1:
                for j in v:
                    self.revcodenames[j] = k
            else:
                self.revcodenames[v[0]] = k

    def normalize_distro_data(self):

        regex = re.compile(r'^(\d+)\.(\d+)(\.(\d+))?([ab](\d+))?$', re.VERBOSE)
        codematch = regex.match(self.codename)

        if not codematch:
            self.version = self.revcodenames[self.codename]
        else:
            (major, minor, patch, pre, prenum) = codematch.group(1, 2, 4, 5, 6)
            self.version = '.'.join(list(filter(None, [major, minor, patch,
                                                       pre, prenum])))
        vermatch = regex.match(self.version)
        if self.distname == 'ubuntu':
            self.codename = self.codenames['.'.join(vermatch.group(1, 2))][0]

        else:
            self.codename = self.codenames[str(float(vermatch.group(1)))][0]

        if self.is_supported_codename():
            log.info('You are using %s (%s).' % (self.distname, self.codename))
            self.distribution = Distribution(self.distname,
                                             self.codename,
                                             self.containers,
                                             self.distributions)
        else:
            raise UnsupportedDistribution()

    def is_supported_distname(self):
        if self.distname in self.distributions:
            return True
        return False

    def is_supported_codename(self):
        if self.is_supported_distname():
            if (self.codename in
               self.distributions[self.distname]['dependencies']):
                return True
        return False

    def check_binaries(self):
        if not self.distribution.check_binaries():
            self.install_dependencies()

    def install_dependencies(self):

        log.info('Installing missing dependencies ...')

        for manager, metadata in self.distribution.get_managers().items():
            for dep in self.distribution.get_dependencies():
                if dep.get('containers') == self.containers \
                   and dep.get(manager):

                    metadata.update({'manager': manager})
                    metadata.update({'dependencies': dep.get(manager)})
                    metadata.update({'origin': dep.get('origin')})

                    if manager == 'custom':
                        pass
                        # self.custom(metadata)

                    else:
                        self.configure_mirrors(metadata)
                        self.update_package_db(metadata)
                        self.install(metadata)
                        self.deconfigure_mirrors(metadata)

    def configure_mirrors(self, metadata):

        shutil.move(metadata['mirrorconf'], '%s.bk' % metadata['mirrorconf'])
        shutil.move(metadata['mirrorlist'], '%s.bk' % metadata['mirrorlist'])

        with open(metadata['mirrorconf'], 'a') as mirrorconf:
            mirrorconf.write(metadata['mirrorboiler'])

            for o in metadata['origin']:
                mirrorconf.write(metadata['mirrortemplate'] % {
                    'origin': o,
                    'url': metadata['mirrors'][o],
                    'sections': ' '.join(metadata.get('sections', []))
                })

    def deconfigure_mirrors(self, metadata):

        shutil.move('%s.bk' % metadata['mirrorconf'], metadata['mirrorconf'])
        shutil.move('%s.bk' % metadata['mirrorlist'], metadata['mirrorlist'])

    def update_package_db(self, metadata):

        if 'env' in metadata:
            self.env.update(metadata['env'])

        args = []
        args.extend([metadata.get('command')])
        args.extend([metadata.get('update')])
        args.extend(metadata.get('args'))

        result = Popen(args=args, stdout=PIPE, stderr=PIPE,
                       env=self.env, close_fds=True)

        for line in iter(result.stdout.readline, ''):
            if line:
                log.info(str(line).strip('\n'))
            else:
                break

    def install(self, metadata):

        if 'env' in metadata:
            self.env.update(metadata['env'])

        if metadata['command'] == 'apt-get':
            metadata['args'].extend(['-t%s' % metadata['origin'][0]])

        args = []
        args.extend([metadata.get('command')])
        args.extend([metadata.get('install')])
        args.extend(metadata.get('args'))
        args.extend(metadata.get('dependencies'))

        result = Popen(args=args, stdout=PIPE, stderr=PIPE,
                       env=self.env, close_fds=True)

        for line in iter(result.stdout.readline, ''):
            if line:
                log.info(str(line).strip('\n'))
            else:
                break

    def custom(self, metadata):

        if 'env' in metadata:
            self.env.update(metadata['env'])

        for cmd in metadata.get('dependencies'):
            args = cmd.split()

            result = Popen(args=args, stdout=PIPE, stderr=PIPE,
                           env=self.env, close_fds=True)

            for line in iter(result.stdout.readline, ''):
                if line:
                    log.info(str(line).strip('\n'))
                else:
                    break


class Distribution(object):

    def __init__(self, distname, codename, containers, distributions):
        self.distributions = distributions
        self.distname = distname
        self.codename = codename
        self.containers = containers

    def get_binaries(self):
        binaries = []
        for dep in self.get_dependencies():
            if dep.get('containers') == self.containers \
               and dep.get('binaries'):
                binaries.extend(dep.get('binaries'))
        return binaries

    def get_managers(self):
        return self.distributions[self.distname]['managers']

    def get_dependencies(self):
        return self.distributions[self.distname]['dependencies'][self.codename]

    def check_binaries(self):
        log.info('Checking for dependencies ...')
        for b in self.get_binaries():
            if not find_executable(b):
                log.info('%s not found!' % b)
                return False
        log.info('Everything ok!')
        return True


if __name__ == '__main__':

    installer = DependencySolver(CONTAINERS, DISTRIBUTIONS)
    installer.get_distro_data()
    installer.normalize_distro_data()
    installer.check_binaries()
