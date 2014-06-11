#!/usr/bin/env python
import subprocess
from django.core import management
from django.contrib.auth.models import User
from tribus.web.registration.ldap.utils import create_ldap_user
subprocess.call(['service','mongodb', 'restart'])
subprocess.call(['service','postgresql', 'restart'])
subprocess.call(['service','redis-server', 'restart'])
subprocess.call(['service','slapd', 'restart'])
subprocess.call(['service','uwsgi', 'restart'])
subprocess.call(['service','supervisor', 'restart'])
management.call_command('syncdb', interactive=False)
management.call_command('migrate', interactive=False)
su_data = ['tribus', 'tribus@localhost.com', 'tribus']
su = User.objects.create_superuser(*su_data)
create_ldap_user(su)

