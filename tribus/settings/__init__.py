
import os

CURDIR = os.path.abspath(os.getcwd())

if CURDIR == '/usr/bin':
    GUIDIR = '/usr/share/pyshared/canaimasemilla'
    CONFDIR = '/etc/canaima-semilla/gui'
    BINDIR = '/usr/bin'
    CSBIN = 'c-s'
    SHAREDIR = '/usr/share/canaima-semilla'
    COREDIR = SHAREDIR+'/scripts'
    PROFILEDIR = SHAREDIR+'/profiles'
    DOCDIR = '/usr/share/doc/canaima-semilla/html'
    ICONDIR = '/usr/share/icons/hicolor'
    LOCALEDIR = '/usr/share/locale'
elif os.isfile(get_path([CURDIR, ])):
    SRCDIR = CURDIR
    GUIDIR = SRCDIR+'/canaimasemilla'
    CONFDIR = SRCDIR+'/config/gui'
    BINDIR = SRCDIR
    CSBIN = 'c-s-core.sh'
    SHAREDIR = SRCDIR
    COREDIR = SRCDIR+'/scripts'
    PROFILEDIR = SRCDIR+'/profiles'
    DOCDIR = SRCDIR+'/documentation/html'
    ICONDIR = SRCDIR+'/icons/hicolor'
    LOCALEDIR = SRCDIR+'/locale'
