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

DISTRIBUTIONS = {
    'arch': {
        'dependencies': {
            'rolling': [
                {
                    'packages': ['fabric', 'docker'],
                    'binaries': ['fab', 'docker'],
                    'origin': ['core', 'extra', 'community'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'vagrant', 'lxc'],
                    'binaries': ['fab', 'vagrant', 'lxc-create'],
                    'origin': ['core', 'extra', 'community'],
                    'containers': 'vagrant'
                },
                {
                    'custom': [
                        'vagrant plugin install vagrant-lxc'
                    ],
                    'test': [''],
                    'containers': 'vagrant'
                }
            ]
        },
        'codenames': {
            '0.0': ['rolling']
        },
        'managers': {
            'packages': {
                'command': 'pacman',
                'install': '-S',
                'update': '-S',
                'args': ['--refresh', '--noconfirm', '--noprogressbar',
                         '--quiet'],
                'mirrors': {
                    'core':
                        'http://mirrors.kernel.org/archlinux/$repo/os/$arch',
                    'extra':
                        'http://mirrors.kernel.org/archlinux/$repo/os/$arch',
                    'community':
                        'http://mirrors.kernel.org/archlinux/$repo/os/$arch',
                },
                'mirrorconf': '/etc/pacman.conf',
                'mirrorlist': '/etc/pacman.d',
                'mirrorboiler': ('[options]\n'
                                 'Architecture = auto\n'
                                 'SigLevel = Never\n\n'),
                'mirrortemplate': (
                    '[%(origin)s]\nServer = %(url)s\n\n'
                )
            },
            'custom': {
                'command': []
            }
        }
    },
    'debian': {
        'dependencies': {
            'wheezy': [
                {
                    'packages': ['iptables', 'perl', 'libapparmor1',
                                 'libsqlite3-0', 'libdevmapper1.02.1',
                                 'adduser', 'libc6'],
                    'binaries': [],
                    'origin': ['wheezy'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'init-system-helpers'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'docker'
                },
                {
                    'packages': ['docker.io'],
                    'binaries': ['docker.io'],
                    'origin': ['jessie'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'vagrant'
                },
                {
                    'packages': ['vagrant', 'lxc'],
                    'binaries': ['vagrant', 'lxc-create'],
                    'origin': ['wheezy'],
                    'containers': 'vagrant'
                }
            ],
            'jessie': [
                {
                    'packages': ['fabric', 'docker.io'],
                    'binaries': ['fab', 'docker.io'],
                    'origin': ['jessie'],
                    'containers': 'docker'
                },
                {
                    'packages': ['vagrant'],
                    'binaries': ['vagrant'],
                    'origin': ['wheezy'],
                    'containers': 'vagrant'
                },
                {
                    'packages': ['fabric', 'lxc'],
                    'binaries': ['fab', 'lxc-create'],
                    'origin': ['jessie'],
                    'containers': 'vagrant'
                }
            ],
            'sid': [
                {
                    'packages': ['fabric', 'docker.io'],
                    'binaries': ['fab', 'docker.io'],
                    'origin': ['sid'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'vagrant', 'lxc'],
                    'binaries': ['fab', 'vagrant', 'lxc-create'],
                    'origin': ['sid'],
                    'containers': 'vagrant'
                }
            ]
        },
        'codenames': {
            '1.1': ['buzz'],
            '1.2': ['rex'],
            '1.3': ['bo'],
            '2.0': ['hamm'],
            '2.1': ['slink'],
            '2.2': ['potato'],
            '3.0': ['woody'],
            '3.1': ['sarge'],
            '4.0': ['etch'],
            '5.0': ['lenny'],
            '6.0': ['squeeze', 'oldstable'],
            '7.0': ['wheezy', 'stable'],
            '8.0': ['jessie', 'testing'],
            '0.0': ['sid', 'unstable']
        },
        'managers': {
            'packages': {
                'env': {
                    'DEBIAN_FRONTEND': 'noninteractive'
                },
                'command': 'apt-get',
                'install': 'install',
                'update': 'update',
                'args': ['-qq', '-oApt::Install-Recommends=false',
                         '-oApt::Get::Assume-Yes=true',
                         '-oApt::Get::AllowUnauthenticated=true',
                         '-oDPkg::Options::=--force-confmiss',
                         '-oDPkg::Options::=--force-confnew',
                         '-oDPkg::Options::=--force-overwrite',
                         '-oDPkg::Options::=--force-unsafe-io'],
                'mirrors': {
                    'squeeze': 'http://http.us.debian.org/debian',
                    'wheezy': 'http://http.us.debian.org/debian',
                    'wheezy-backports': 'http://http.us.debian.org/debian',
                    'jessie': 'http://http.us.debian.org/debian',
                    'sid': 'http://http.us.debian.org/debian',
                },
                'sections': ['main', 'contrib', 'non-free'],
                'mirrorconf': '/etc/apt/sources.list',
                'mirrorlist': '/etc/apt/sources.list.d',
                'mirrorboiler': '',
                'mirrortemplate': (
                    'deb %(url)s %(origin)s %(sections)s\n'
                )
            }
        }
    },
    'ubuntu': {
        'dependencies': {
            'oneiric': [
                {
                    'packages': ['iptables', 'perl', 'libapparmor1',
                                 'libsqlite3-0', 'libdevmapper1.02.1',
                                 'adduser', 'libc6'],
                    'binaries': [],
                    'origin': ['oneiric'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'init-system-helpers'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'docker'
                },
                {
                    'packages': ['docker.io'],
                    'binaries': ['docker.io'],
                    'origin': ['jessie'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'vagrant'
                },
                {
                    'packages': ['vagrant', 'lxc'],
                    'binaries': ['vagrant', 'lxc-create'],
                    'origin': ['oneiric'],
                    'containers': 'vagrant'
                }
            ],
            'precise': [
                {
                    'packages': ['iptables', 'perl', 'libapparmor1',
                                 'libsqlite3-0', 'libdevmapper1.02.1',
                                 'adduser', 'libc6'],
                    'binaries': [],
                    'origin': ['precise'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'init-system-helpers'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'docker'
                },
                {
                    'packages': ['docker.io'],
                    'binaries': ['docker.io'],
                    'origin': ['jessie'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'vagrant'
                },
                {
                    'packages': ['vagrant', 'lxc'],
                    'binaries': ['vagrant', 'lxc-create'],
                    'origin': ['precise'],
                    'containers': 'vagrant'
                }
            ],
            'quantal': [
                {
                    'packages': ['iptables', 'perl', 'libapparmor1',
                                 'libsqlite3-0', 'libdevmapper1.02.1',
                                 'adduser', 'libc6'],
                    'binaries': [],
                    'origin': ['quantal'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'init-system-helpers'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'docker'
                },
                {
                    'packages': ['docker.io'],
                    'binaries': ['docker.io'],
                    'origin': ['jessie'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'vagrant'
                },
                {
                    'packages': ['vagrant', 'lxc'],
                    'binaries': ['vagrant', 'lxc-create'],
                    'origin': ['quantal'],
                    'containers': 'vagrant'
                }
            ],
            'raring': [
                {
                    'packages': ['iptables', 'perl', 'libapparmor1',
                                 'libsqlite3-0', 'libdevmapper1.02.1',
                                 'adduser', 'libc6'],
                    'binaries': [],
                    'origin': ['raring'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'init-system-helpers'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'docker'
                },
                {
                    'packages': ['docker.io'],
                    'binaries': ['docker.io'],
                    'origin': ['jessie'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'vagrant'
                },
                {
                    'packages': ['vagrant', 'lxc'],
                    'binaries': ['vagrant', 'lxc-create'],
                    'origin': ['raring'],
                    'containers': 'vagrant'
                }
            ],
            'saucy': [
                {
                    'packages': ['iptables', 'perl', 'libapparmor1',
                                 'libsqlite3-0', 'libdevmapper1.02.1',
                                 'adduser', 'libc6'],
                    'binaries': [],
                    'origin': ['saucy'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'init-system-helpers'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'docker'
                },
                {
                    'packages': ['docker.io'],
                    'binaries': ['docker.io'],
                    'origin': ['jessie'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'vagrant'
                },
                {
                    'packages': ['vagrant', 'lxc'],
                    'binaries': ['vagrant', 'lxc-create'],
                    'origin': ['saucy'],
                    'containers': 'vagrant'
                }
            ],
            'trusty': [
                {
                    'packages': ['fabric', 'docker.io'],
                    'binaries': ['fab', 'docker.io'],
                    'origin': ['trusty'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'vagrant', 'lxc'],
                    'binaries': ['fab', 'vagrant', 'lxc-create'],
                    'origin': ['trusty'],
                    'containers': 'vagrant'
                }
            ],
            'utopic': [
                {
                    'packages': ['fabric', 'docker.io'],
                    'binaries': ['fab', 'docker.io'],
                    'origin': ['utopic'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'vagrant', 'lxc'],
                    'binaries': ['fab', 'vagrant', 'lxc-create'],
                    'origin': ['utopic'],
                    'containers': 'vagrant'
                }
            ]
        },
        'codenames': {
            '4.10': ['warty'],
            '5.04': ['hoary'],
            '5.10': ['breezy'],
            '6.04': ['dapper'],
            '6.10': ['edgy'],
            '7.04': ['feisty'],
            '7.10': ['gutsy'],
            '8.04': ['hardy'],
            '8.10': ['intrepid'],
            '9.04': ['jaunty'],
            '9.10': ['karmic'],
            '10.04': ['lucid'],
            '10.10': ['maverick'],
            '11.04': ['natty'],
            '11.10': ['oneiric'],
            '12.04': ['precise'],
            '12.10': ['quantal'],
            '13.04': ['raring'],
            '13.10': ['saucy'],
            '14.04': ['trusty'],
            '14.10': ['utopic']
        },
        'managers': {
            'packages': {
                'env': {
                    'DEBIAN_FRONTEND': 'noninteractive'
                },
                'command': 'apt-get',
                'install': 'install',
                'update': 'update',
                'args': ['-qq', '-oApt::Install-Recommends=false',
                         '-oApt::Get::Assume-Yes=true',
                         '-oApt::Get::AllowUnauthenticated=true',
                         '-oDPkg::Options::=--force-confmiss',
                         '-oDPkg::Options::=--force-confnew',
                         '-oDPkg::Options::=--force-overwrite',
                         '-oDPkg::Options::=--force-unsafe-io'],
                'mirrors': {
                    'oneiric': 'http://archive.ubuntu.com/ubuntu',
                    'precise': 'http://archive.ubuntu.com/ubuntu',
                    'quantal': 'http://archive.ubuntu.com/ubuntu',
                    'raring': 'http://archive.ubuntu.com/ubuntu',
                    'saucy': 'http://archive.ubuntu.com/ubuntu',
                    'trusty': 'http://archive.ubuntu.com/ubuntu',
                    'utopic': 'http://archive.ubuntu.com/ubuntu',
                    'wheezy-backports': 'http://http.us.debian.org/debian',
                    'jessie': 'http://http.us.debian.org/debian',
                },
                'sections': ['main', 'universe', 'multiverse', 'restricted'],
                'mirrorconf': '/etc/apt/sources.list',
                'mirrorlist': '/etc/apt/sources.list.d',
                'mirrorboiler': '',
                'mirrortemplate': (
                    'deb %(url)s %(origin)s %(sections)s\n'
                )
            }
        }
    },
    'canaima': {
        'dependencies': {
            'kerepakupai': [
                {
                    'packages': ['iptables', 'perl', 'libapparmor1',
                                 'libsqlite3-0', 'libdevmapper1.02.1',
                                 'adduser', 'libc6'],
                    'binaries': [],
                    'origin': ['kerepakupai'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'init-system-helpers'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'docker'
                },
                {
                    'packages': ['docker.io'],
                    'binaries': ['docker.io'],
                    'origin': ['jessie'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'vagrant'
                },
                {
                    'packages': ['vagrant', 'lxc'],
                    'binaries': ['vagrant', 'lxc-create'],
                    'origin': ['kerepakupai'],
                    'containers': 'vagrant'
                }
            ],
            'kukenan': [
                {
                    'packages': ['iptables', 'perl', 'libapparmor1',
                                 'libsqlite3-0', 'libdevmapper1.02.1',
                                 'adduser', 'libc6'],
                    'binaries': [],
                    'origin': ['kukenan'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric', 'init-system-helpers'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'docker'
                },
                {
                    'packages': ['docker.io'],
                    'binaries': ['docker.io'],
                    'origin': ['jessie'],
                    'containers': 'docker'
                },
                {
                    'packages': ['fabric'],
                    'binaries': ['fab'],
                    'origin': ['wheezy-backports', 'wheezy'],
                    'containers': 'vagrant'
                },
                {
                    'packages': ['vagrant', 'lxc'],
                    'binaries': ['vagrant', 'lxc-create'],
                    'origin': ['kukenan'],
                    'containers': 'vagrant'
                }
            ]
        },
        'codenames': {
            '1.0': [''],
            '1.1': [''],
            '2.0': [''],
            '2.0.1': [''],
            '2.0.2': [''],
            '2.0.3': [''],
            '2.0.4': [''],
            '2.1': ['aponwao'],
            '3.0': ['roraima'],
            '3.1': ['auyantepui'],
            '4.0': ['kerepakupai'],
            '4.1': ['kukenan']
        },
        'managers': {
            'packages': {
                'env': {
                    'DEBIAN_FRONTEND': 'noninteractive'
                },
                'command': 'apt-get',
                'install': 'install',
                'update': 'update',
                'args': ['-qq', '-oApt::Install-Recommends=false',
                         '-oApt::Get::Assume-Yes=true',
                         '-oApt::Get::AllowUnauthenticated=true',
                         '-oDPkg::Options::=--force-confmiss',
                         '-oDPkg::Options::=--force-confnew',
                         '-oDPkg::Options::=--force-overwrite',
                         '-oDPkg::Options::=--force-unsafe-io'],
                'mirrors': {
                    'kerepakupai':
                        'http://paquetes.canaima.softwarelibre.gob.ve',
                    'kukenan':
                        'http://paquetes.canaima.softwarelibre.gob.ve',
                    'wheezy-backports':
                        'http://http.us.debian.org/debian',
                    'jessie':
                        'http://http.us.debian.org/debian'
                },
                'sections': ['main', 'contrib', 'non-free'],
                'mirrorconf': '/etc/apt/sources.list',
                'mirrorlist': '/etc/apt/sources.list.d',
                'mirrorboiler': '',
                'mirrortemplate': (
                    'deb %(url)s %(origin)s %(sections)s\n'
                )
            }
        }
    },
    'fedora': {
        'dependencies': {
            '17.0': [
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
        },
        'codenames': {
            '1.0': ['yarrow'],
            '2.0': ['tettnang'],
            '3.0': ['heidelberg'],
            '4.0': ['stentz'],
            '5.0': ['bordeaux'],
            '6.0': ['zod'],
            '7.0': ['moonshine'],
            '8.0': ['werewolf'],
            '9.0': ['sulphur'],
            '10.0': ['cambridge'],
            '11.0': ['leonidas'],
            '12.0': ['constantine'],
            '13.0': ['goddard'],
            '14.0': ['laughlin'],
            '15.0': ['lovelock'],
            '16.0': ['verne'],
            '17.0': ['beefy-miracle'],
            '18.0': ['spherical-cow'],
            '19.0': ['schrodingers-cat'],
            '20.0': ['heisenbug'],
            '0.0': ['rawhide'],
        },
        'managers': {
            'packages': {
                'command': 'yum',
                'install': 'install',
                'update': 'update',
                'args': '--assumeyes --nogpgcheck --quiet',
                'mirrors': [
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
    'centos': {
        'dependencies': {
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
            '1.0': ['1.0'],
            '2.0': ['2.0'],
            '3.0': ['3.0'],
            '4.0': ['4.0'],
            '5.0': ['5.0'],
            '6.0': ['6.0'],
            '7.0': ['7.0']
        },
        'managers': {
            'packages': {
                'command': 'yum',
                'install': 'install',
                'update': 'update',
                'args': '--assumeyes --nogpgcheck --quiet',
                'mirrors': [
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
    'gentoo': {
        'dependencies': {
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
            '1.0': ['1.0'],
            '2.0': ['2.0'],
            '3.0': ['3.0'],
            '4.0': ['4.0'],
            '5.0': ['5.0'],
            '6.0': ['6.0'],
            '7.0': ['7.0']
        },
        'managers': {
            'packages': {
                'command': 'yum',
                'install': 'install',
                'update': 'update',
                'args': '--assumeyes --nogpgcheck --quiet',
                'mirrors': [
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
    }
}
