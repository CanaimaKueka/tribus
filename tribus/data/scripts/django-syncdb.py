#!/usr/bin/env python
import subprocess
from django.core import management
from django.contrib.auth.models import User
from tribus.web.registration.ldap.utils import create_ldap_user
subprocess.call(['service','mongodb', 'start'])
subprocess.call(['service','postgresql', 'start'])
subprocess.call(['service','redis-server', 'start'])
subprocess.call(['service','slapd', 'start'])
subprocess.call(['service','uwsgi', 'start'])
subprocess.call(['service','nginx', 'start'])
subprocess.call(['service','supervisor', 'start'])
management.call_command('syncdb', interactive=False)
management.call_command('migrate', interactive=False)
su_data = ['tribus', 'tribus@localhost.com', 'tribus']
su = User.objects.create_superuser(*su_data)
create_ldap_user(su)

