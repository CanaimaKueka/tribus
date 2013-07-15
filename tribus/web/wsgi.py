import sys, os, site

os.environ['DJANGO_SETTINGS_MODULE'] = 'tribus.web.settings'

base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'virtualenv'))
os.environ['PATH'] = os.path.join(base, 'bin') + os.pathsep + os.environ['PATH']
site.addsitedir(os.path.join(base, 'lib', 'python%s' % sys.version[:3], 'site-packages'))
sys.prefix = base
sys.path.insert(0, base)

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()