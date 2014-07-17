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

import os
import re
from subprocess import Popen, PIPE
from distutils.spawn import find_executable
from distutils.version import StrictVersion

# from tribus.common.distributions import DISTRIBUTIONS

DISTRIBUTIONS = {
    'debian': {
        'dependencies': {
            'wheezy': [
                {
                    'packages': ('iptables perl libapparmor1 libsqlite3-0 '
                                 'libdevmapper1.02.1 adduser libc6'),
                    'origin': 'wheezy',
                    'containers': 'docker'
                },
                {
                    'packages': 'fabric init-system-helpers',
                    'origin': 'wheezy-backports',
                    'containers': 'docker'
                },
                {
                    'packages': 'docker.io',
                    'origin': 'jessie',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'wheezy',
                    'containers': 'vagrant'
                }
            ],
            'jessie': [
                {
                    'packages': 'docker.io fabric',
                    'origin': 'jessie',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant',
                    'origin': 'wheezy',
                    'containers': 'vagrant'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'jessie',
                    'containers': 'vagrant'
                }
            ],
            'sid': [
                {
                    'packages': 'docker.io fabric',
                    'origin': 'sid',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'sid',
                    'containers': 'vagrant'
                }
            ]
        },
        'codenames': {
            '7.0': 'wheezy',
            '8.0': 'jessie',
            'rolling': 'sid'
        },
        'managers': {
            'packages': {
                'command': ('env DEBIAN_FRONTEND=noninteractive'
                            ' %s') % find_executable('apt-get'),
                'install': 'install',
                'arguments': ('-qq -o Apt::Install-Recommends=false '
                              '-o Apt::Get::Assume-Yes=true '
                              '-o Apt::Get::AllowUnauthenticated=true '
                              '-o DPkg::Options::=--force-confmiss '
                              '-o DPkg::Options::=--force-confnew '
                              '-o DPkg::Options::=--force-overwrite '
                              '-o DPkg::Options::=--force-unsafe-io'),
                'mirror': 'http://http.us.debian.org/debian',
                'sections': 'main contrib non-free'
            }
        }
    },
    'ubuntu': {
        'dependencies': {
            'oneiric': [
                {
                    'packages': ('iptables perl libapparmor1 libsqlite3-0 '
                                 'libdevmapper1.02.1 adduser libc6'),
                    'origin': 'oneiric',
                    'containers': 'docker'
                },
                {
                    'packages': 'fabric init-system-helpers',
                    'origin': 'wheezy-backports',
                    'containers': 'docker'
                },
                {
                    'packages': 'docker.io',
                    'origin': 'jessie',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'oneiric',
                    'containers': 'vagrant'
                }
            ],
            'precise': [
                {
                    'packages': ('iptables perl libapparmor1 libsqlite3-0 '
                                 'libdevmapper1.02.1 adduser libc6'),
                    'origin': 'precise',
                    'containers': 'docker'
                },
                {
                    'packages': 'fabric init-system-helpers',
                    'origin': 'wheezy-backports',
                    'containers': 'docker'
                },
                {
                    'packages': 'docker.io',
                    'origin': 'jessie',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'precise',
                    'containers': 'vagrant'
                }
            ],
            'quantal': [
                {
                    'packages': ('iptables perl libapparmor1 libsqlite3-0 '
                                 'libdevmapper1.02.1 adduser libc6'),
                    'origin': 'quantal',
                    'containers': 'docker'
                },
                {
                    'packages': 'fabric init-system-helpers',
                    'origin': 'wheezy-backports',
                    'containers': 'docker'
                },
                {
                    'packages': 'docker.io',
                    'origin': 'jessie',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'quantal',
                    'containers': 'vagrant'
                }
            ],
            'raring': [
                {
                    'packages': ('iptables perl libapparmor1 libsqlite3-0 '
                                 'libdevmapper1.02.1 adduser libc6'),
                    'origin': 'raring',
                    'containers': 'docker'
                },
                {
                    'packages': 'fabric init-system-helpers',
                    'origin': 'wheezy-backports',
                    'containers': 'docker'
                },
                {
                    'packages': 'docker.io',
                    'origin': 'jessie',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'raring',
                    'containers': 'vagrant'
                }
            ],
            'saucy': [
                {
                    'packages': ('iptables perl libapparmor1 libsqlite3-0 '
                                 'libdevmapper1.02.1 adduser libc6'),
                    'origin': 'saucy',
                    'containers': 'docker'
                },
                {
                    'packages': 'fabric init-system-helpers',
                    'origin': 'wheezy-backports',
                    'containers': 'docker'
                },
                {
                    'packages': 'docker.io',
                    'origin': 'jessie',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'saucy',
                    'containers': 'vagrant'
                }
            ],
            'trusty': [
                {
                    'packages': 'fabric docker.io',
                    'origin': 'trusty',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'trusty',
                    'containers': 'vagrant'
                }
            ],
            'utopic': [
                {
                    'packages': 'fabric docker.io',
                    'origin': 'utopic',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'utopic',
                    'containers': 'vagrant'
                }
            ]
        },
        'codenames': {
            '': 'oneiric',
            '': 'precise',
            '': 'quantal',
            '': 'raring',
            '': 'saucy',
            '': 'trusty',
            '': 'utopic'
        },
        'managers': {
            'packages': {
                'command': ('env DEBIAN_FRONTEND=noninteractive'
                            ' %s') % find_executable('apt-get'),
                'install': 'install',
                'arguments': ('-qq -o Apt::Install-Recommends=false '
                              '-o Apt::Get::Assume-Yes=true '
                              '-o Apt::Get::AllowUnauthenticated=true '
                              '-o DPkg::Options::=--force-confmiss '
                              '-o DPkg::Options::=--force-confnew '
                              '-o DPkg::Options::=--force-overwrite '
                              '-o DPkg::Options::=--force-unsafe-io'),
                'mirror': 'http://archive.ubuntu.com/ubuntu',
                'sections': 'main universe multiverse restricted'
            }
        }
    },
    'canaima': {
        'dependencies': {
            'kerepakupai': [
                {
                    'packages': ('iptables perl libapparmor1 libsqlite3-0 '
                                 'libdevmapper1.02.1 adduser libc6'),
                    'origin': 'kerepakupai',
                    'containers': 'docker'
                },
                {
                    'packages': 'fabric init-system-helpers',
                    'origin': 'wheezy-backports',
                    'containers': 'docker'
                },
                {
                    'packages': 'docker.io',
                    'origin': 'jessie',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'kerepakupai',
                    'containers': 'vagrant'
                }
            ],
            'kukenan': [
                {
                    'packages': ('iptables perl libapparmor1 libsqlite3-0 '
                                 'libdevmapper1.02.1 adduser libc6'),
                    'origin': 'kukenan',
                    'containers': 'docker'
                },
                {
                    'packages': 'fabric init-system-helpers',
                    'origin': 'wheezy-backports',
                    'containers': 'docker'
                },
                {
                    'packages': 'docker.io',
                    'origin': 'jessie',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'origin': 'kukenan',
                    'containers': 'vagrant'
                }
            ]
        },
        'codenames': {
            '4.0': 'kerepakupai',
            '4.1': 'kukenan'
        },
        'managers': {
            'packages': {
                'command': ('env DEBIAN_FRONTEND=noninteractive'
                            ' %s') % find_executable('apt-get'),
                'install': 'install',
                'arguments': ('-qq -o Apt::Install-Recommends=false '
                              '-o Apt::Get::Assume-Yes=true '
                              '-o Apt::Get::AllowUnauthenticated=true '
                              '-o DPkg::Options::=--force-confmiss '
                              '-o DPkg::Options::=--force-confnew '
                              '-o DPkg::Options::=--force-overwrite '
                              '-o DPkg::Options::=--force-unsafe-io'),
                'mirror': 'http://paquetes.canaima.softwarelibre.gob.ve',
                'sections': 'main aportes no-libres'
            }
        }
    },
    # 'fedora': {
    #     'shrodinger': {
    #         'docker': [
    #             {

    #             }
    #         ],
    #         'vagrant': [
    #             {

    #             }
    #         ]
    #     },
    #     'heisenbug': {
    #         'docker': [
    #             {

    #             }
    #         ],
    #         'vagrant': [
    #             {

    #             }
    #         ]
    #     }
    # },
    # 'centos': {
    #     '': {
    #         'docker': [
    #             {

    #             }
    #         ],
    #         'vagrant': [
    #             {

    #             }
    #         ]
    #     }
    # },
    'arch': {
        'dependencies': {
            'rolling': [
                {
                    'packages': 'fabric docker',
                    'containers': 'docker'
                },
                {
                    'packages': 'vagrant virtualbox',
                    'containers': 'vagrant'
                }
            ]
        },
        'codenames': {
            'rolling': 'rolling'
        },
        'managers': {
            'packages': {
                'command': '%s' % find_executable('pacman'),
                'install': '-S',
                'arguments': '--refresh --noconfirm --noprogressbar --quiet',
                'mirror': 'http://mirrors.kernel.org/archlinux/$repo/os/$arch'
# Server = http://mirror.rit.edu/archlinux/$repo/os/$arch
            }
        }
    },
    'centos': {
        'dependencies': {
            '5.0': [
                {
                    'packages': 'gcc python-setuptools python-devel docker-io',
                    'containers': 'docker'
                },
                {
                    'setuptools': 'pip',
                    'containers': 'docker'
                },
                {
                    'pip': 'fabric',
                    'containers': 'docker'
                },
                {
                    'custom': '',
                    'containers': 'vagrant'
                }
            ],
            '6.0': [
                {
                    'packages': 'gcc python-setuptools python-devel docker-io',
                    'containers': 'docker'
                },
                {
                    'setuptools': 'pip',
                    'containers': 'docker'
                },
                {
                    'pip': 'fabric',
                    'containers': 'docker'
                },
                {
                    'custom': '',
                    'containers': 'vagrant'
                }
            ],
            '7.0': [
                {
                    'packages': 'gcc python-setuptools python-devel docker-io',
                    'containers': 'docker'
                },
                {
                    'setuptools': 'pip',
                    'containers': 'docker'
                },
                {
                    'pip': 'fabric',
                    'containers': 'docker'
                },
                {
                    'custom': '',
                    'containers': 'vagrant'
                }
            ]
        },
        'codenames': {
            '5.0': '5.0',
            '6.0': '6.0',
            '7.0': '7.0'
        },
        'managers': {
            'packages': {
                'command': '%s' % find_executable('yum'),
                'install': 'install',
                'update': 'update',
                'arguments': '--assumeyes --nogpgcheck --quiet',
                'mirror': [
                    'http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os',
                    'http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=updates',
                    'http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=extras',
                    'http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=centosplus',
                    'http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=contrib',
                    'https://mirrors.fedoraproject.org/metalink?repo=epel-$releasever&arch=$basearch'
                ]
# [epel]
# name=Extra Packages for Enterprise Linux 7 - $basearch
# #baseurl=http://download.fedoraproject.org/pub/epel/7/$basearch
# mirrorlist=https://mirrors.fedoraproject.org/metalink?repo=epel-7&arch=$basearch
# failovermethod=priority
# enabled=1
# gpgcheck=0
# gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-7
            }
        }
    },
    # 'gentoo': {
    #     '': {
    #         'docker': [
    #             {

    #             }
    #         ],
    #         'vagrant': [
    #             {

    #             }
    #         ]
    #     }
    # }
}

RELEASE_CODENAME_LOOKUP = {
    '1.1' : 'buzz',
    '1.2' : 'rex',
    '1.3' : 'bo',
    '2.0' : 'hamm',
    '2.1' : 'slink',
    '2.2' : 'potato',
    '3.0' : 'woody',
    '3.1' : 'sarge',
    '4.0' : 'etch',
    '5.0' : 'lenny',
    '6.0' : 'squeeze',
    '7'   : 'wheezy',
    '8'   : 'jessie',
    }

TESTING_CODENAME = 'unknown.new.testing'

RELEASES_ORDER = list(RELEASE_CODENAME_LOOKUP.items())
RELEASES_ORDER.sort()
RELEASES_ORDER = list(list(zip(*RELEASES_ORDER))[1])
RELEASES_ORDER.extend(['stable', 'testing', 'unstable', 'sid'])

class PackageInstaller(object):

    def __init__(self,):
        self.distro_data = DISTRIBUTIONS
        self.release_data = {}
        self.dpkg_origins_data = {}
        self.distro = ''
        self.codename = ''
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
        self.longnames = {
            'v' : 'version',
            'o': 'origin',
            'a': 'suite',
            'c' : 'component',
            'l': 'label'
        }

    def release_index(self, x):
        suite = x[1].get('suite')
        if suite:
            if suite in RELEASES_ORDER:
                return int(len(RELEASES_ORDER) - RELEASES_ORDER.index(suite))
            else:
                return suite
        return 0

    def parse_release_file(self, releasefile):
        contentlist = open(releasefile).read().split('\n')
        for j in contentlist:
            if re.findall(r'=', j):
                key = j.split('=')[0].upper()
                value = j.split('=')[1].strip('"').lower()
                self.release_data[key] = value
            elif j:
                self.release_data['PRETTY_NAME'] = j.lower()
        return self.release_data

    def parse_policy_line(self, data):
        retval = {}
        bits = data.split(',')
        for bit in bits:
            kv = bit.split('=', 1)
            if len(kv) > 1:
                k, v = kv[:2]
                if k in self.longnames:
                    retval[self.longnames[k]] = v
        return retval


    def parse_apt_policy(self):
        data = []

        env = os.environ.copy()
        env['LC_ALL'] = 'C'

        policy = Popen(args=['apt-cache', 'policy'],
                       env=env,
                       stdout=PIPE,
                       stderr=PIPE,
                       close_fds=True).communicate()[0].decode('utf-8')

        for line in policy.split('\n'):
            line = line.strip()
            m = re.match(r'(-?\d+)', line)
            if m:
                priority = int(m.group(1))
            if line.startswith('release'):
                bits = line.split(' ', 1)
                if len(bits) > 1:
                    data.append((priority, self.parse_policy_line(bits[1])))

        return data

    def get_codename_from_apt(self, origin='Debian', component='main',
                               ignoresuites=('experimental'),
                               label='Debian',
                               alternate_olabels={'Debian Ports':'ftp.debian-ports.org'}):

        releases = self.parse_apt_policy()

        if not releases:
            return None

        # We only care about the specified origin, component, and label
        releases = [x for x in releases if (
            x[1].get('origin', '') == origin and
            x[1].get('component', '') == component and
            x[1].get('label', '') == label) or (
            x[1].get('origin', '') in alternate_olabels and
            x[1].get('label', '') == alternate_olabels.get(x[1].get('origin', '')))]

        # Check again to make sure we didn't wipe out all of the releases
        if not releases:
            return None

        releases.sort(key=lambda tuple: tuple[0], reverse=True)

        # We've sorted the list by descending priority, so the first entry should
        # be the "main" release in use on the system

        max_priority = releases[0][0]
        releases = [x for x in releases if x[0] == max_priority]
        releases.sort(key=self.release_index)

        return releases[0][1]

    def get_distro_data(self):

        if (not self.distro) and self.lsb:

            self.distro = Popen(
                args=['%s' % self.lsb, '-is'],
                stdout=PIPE,
                stderr=PIPE,
                close_fds=True).communicate()[0].split('\n')[0].lower()

            self.codename = Popen(
                args=['%s' % self.lsb, '-cs'],
                stdout=PIPE,
                stderr=PIPE,
                close_fds=True).communicate()[0].split('\n')[0].lower()

        if (not self.distro) and os.path.exists(self.arch_release):
            self.distro = 'arch'
            self.codename = 'rolling'

        if (not self.distro) and os.path.exists(self.gentoo_release):
            self.distro = 'gentoo'
            self.codename = 'rolling'

        if (not self.distro) and os.path.exists(self.fedora_release):
            self.parse_release_file(self.fedora_release)
            self.distro = self.release_data['PRETTY_NAME'].split()[0]
            self.codename = re.search(
                r'(.*)\(.*\)',
                self.release_data['PRETTY_NAME']).group(1).split()[-1]

        if (not self.distro) and os.path.exists(self.centos_release):
            self.parse_release_file(self.centos_release)
            self.distro = self.release_data['PRETTY_NAME'].split()[0]
            self.codename = self.release_data['PRETTY_NAME'].split()[-2]

        if (not self.distro) and os.path.exists(self.redhat_release):
            self.parse_release_file(self.redhat_release)
            self.distro = self.release_data['PRETTY_NAME'].split()[0]
            self.codename = self.release_data['PRETTY_NAME'].split()[-2]

        if (not self.distro) and os.path.exists(self.lsb_release):
            self.parse_release_file(self.lsb_release)
            self.distro = self.release_data['DISTRIB_ID']
            self.codename = self.release_data['DISTRIB_CODENAME']

        if (not self.distro) and os.path.exists(self.os_release):
            self.parse_release_file(self.os_release)
            self.distro = self.release_data['ID']
            self.codename = self.release_data['PRETTY_NAME']
            self.codename = self.codename.split()[-2].strip('()')

            if self.distro == 'debian':
                if os.path.exists(self.debian_release):
                    self.parse_release_file(self.debian_release)

                    if re.findall(r'[\d\.\d]+',
                                  self.release_data['PRETTY_NAME']):
                        self.codename = self.release_data['PRETTY_NAME']

                    elif re.findall(r'.*/.*',
                                    self.release_data['PRETTY_NAME']):
                        self.codename = self.get_codename_from_apt()['suite']

        print(self.distro, self.codename)


if __name__ == '__main__':

    installer = PackageInstaller()
    installer.get_distro_data()
    # installer.validate_distro()
    # installer.check_binaries()
