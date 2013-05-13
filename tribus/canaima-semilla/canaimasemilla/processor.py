#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# ==============================================================================
# PAQUETE: canaima-semilla
# ARCHIVO: scripts/c-s.sh
# DESCRIPCIÓN: Script principal. Se encarga de invocar a los demás módulos y
#              funciones según los parámetros proporcionados.
# USO: ./c-s.sh [MÓDULO] [PARÁMETROS] [...]
# COPYRIGHT:
#       (C) 2010-2012 Luis Alejandro Martínez Faneyth <luis@huntingbears.com.ve>
#       (C) 2012 Niv Sardi <xaiki@debian.org>
# LICENCIA: GPL-3
# ==============================================================================
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# COPYING file for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# CODE IS POETRY

import gtk, sys, os, re, urllib2, fnmatch, threading, subprocess, random, gzip
import gobject, tempfile, Queue, hashlib, tempfile, subprocess, time, shutil
import aptsources.distinfo, ConfigParser

from canaimasemilla.constructor import ProgressWindow, UserMessage
from canaimasemilla.translator import *
from canaimasemilla.common import *
from canaimasemilla.config import *

def replace_all(text, dic):
    for i, j in dic.iteritems():
        text = text.replace(i, j)
    return text

def is_valid_url(url):
    regex = re.compile(
        r'^(http|ftp|file):///?'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|[a-zA-Z0-9-]*|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE
        )
    return regex.search(url)

class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"

def KillProcess(reference, shell = [], python = [], terminal = False):
    for s in shell:
        k = ProcessGenerator(['/usr/bin/pkill', s], terminal = terminal)
    for p in python:
        p.kill()
    return True

def GetArch(terminal = False):
    p = ProcessGenerator(['/usr/bin/arch'], terminal = terminal)
    a = p.stdout.read().split('\n')[0]
    return a

def ParseProfileConfig(profile, get):
    conffile = PROFILEDIR+'/'+profile+'/profile.conf'
    f = open(conffile, 'r')
    ask = []
    give = []
    for line in f.readlines():
        for variable in get:
            if line.find(variable+'=') != -1:
                value = replace_all(line, {variable+'=':'', '"':'', '\n':''})
                ask.append(variable)
                give.append(value)
    f.close()
    return dict(zip(ask, give))

def copy2destination(items):
    try:
        for what, where in items:
            if what and os.path.exists(what):
                if os.path.isdir(f):
                    if os.path.exists(where):
                        return False
                    shutil.copytree(os.path.realpath(f), where)
                else:
                    if not os.path.exists(where):
                        os.mkdir(where)
                    shutil.copy2(os.path.realpath(f), where)
    except Exception, msg:
        return False
    return True

def GetFreeDisk():
    return float(subprocess.Popen(
        'echo "scale=1;$( df '+SHAREDIR+' | grep "/" | awk \'{print $4}\' )/(10^6)" | bc',
        shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
    ).communicate()[0].split('\n')[0])

def GetFreeRam():
    return float(subprocess.Popen(
        'echo "scale=1;$( cat "/proc/meminfo" | grep "MemFree:" | awk \'{print $2}\' )/(10^3)" | bc',
        shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
    ).communicate()[0].split('\n')[0])

def GetProcessors():
    return float(subprocess.Popen(
        'echo "scale=1;$( cat "/proc/cpuinfo" | grep -c "processor" )" | bc',
        shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
    ).communicate()[0].split('\n')[0])

def GetWritableDrives():
    usb = subprocess.Popen(
        '/bin/sh '+BINDIR+'/'+CSBIN+' save -L',
        shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
    ).communicate()[0].split('\n')
    opt = subprocess.Popen(
        '/bin/sh '+BINDIR+'/'+CSBIN+' save -l',
        shell = True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT,
    ).communicate()[0].split('\n')
    return opt+usb

def ProfileList(c, profiledir):
    profilelist = []
    items = next(os.walk(profiledir))[1]
    for i in items:
        profilelist.append(i)
    return profilelist, 0

def LocaleList(c, supported, current):
    localecount = 0
    localeactive = 0
    localelist = []
    with open(supported, 'r') as supportedlocales:
        for item in supportedlocales:
            localecode = item.split()
            localelist.append(localecode[0])
            if localecode[0].upper().replace('-','') == current.upper().replace('-',''):
                localeactive = localecount
            localecount += 1

    return localelist, localeactive

def CodenameList(c, dist, db):
    codenamelist = []
    codenameactive = 0
    udist = dist.get_active_text().title()
    d = aptsources.distinfo.DistInfo(udist, db)

    for template in d.templates:
        if not template.name in codenamelist:
            codenamelist.append(template.name)

    return codenamelist, codenameactive

def SectionList(c, dist):
    text = dist.get_active_text()
    exec "sectionlist = "+text+"_sections"
    return sectionlist

def CleanTempDir(tempdir):
    if not os.path.exists(tempdir):
        mktempdir = os.mkdir(tempdir)
    else:
        for path in os.listdir(tempdir):
            if os.path.isfile(tempdir+path) and fnmatch.fnmatch(tempdir+path, '*.gz'):
                os.unlink(tempdir+path)
    return True

class ThreadGenerator(threading.Thread):
    def __init__(self, reference, function, params,
                    gtk = False, window = False, event = False):
        threading.Thread.__init__(self)
        self._gtk = gtk
        self._window = window
        self._function = function
        self._params = params
        self._event = event
        self.start()

    def run(self):
        if self._gtk:
            gtk.gdk.threads_enter()

        if self._event:
            self._event.wait()

        self._function(**self._params)

        if self._gtk:
            gtk.gdk.threads_leave()

        if self._window:
            self._window.hide()

def ProcessGenerator(command, terminal = False, bar = False):

    filename = '/tmp/cs-command-'+hashlib.sha1(
        str(random.getrandbits(random.getrandbits(10)))
        ).hexdigest()

    if isinstance(command, list):
        strcmd = ' '.join(command)
    elif isinstance(command, str):
        strcmd = command

    cmd = '{0} 1>{1} 2>&1'.format(strcmd, filename)

    try:
        os.mkfifo(filename)
        fifo = os.fdopen(os.open(filename, os.O_RDONLY | os.O_NONBLOCK))

        process = subprocess.Popen(
                cmd, shell = True, stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT
                )

        if bar:
            timer = gobject.timeout_add(100, ProgressPulse, bar)

        while process.returncode == None:
            process.poll()
            try:
                line = fifo.readline().strip()
                if terminal:
                    terminal.feed(line+'\r\n')
            except:
                continue

    finally:
        os.unlink(filename)
        if bar:
            gobject.source_remove(timer)

    return process

def TestIndexes(sourcestext, archlist, progressmessage, download,
                q_bar, q_msg, q_code, q_counter, event):

    bar = q_bar.get()
    message = q_msg.get()
    errorcounter = 0
    errorcode = ''
    sourceslist = []
    CleanTempDir(tempdir)

    if not download:
        timer = gobject.timeout_add(100, ProgressPulse, bar)

    for line in sourcestext.split('\n'):
        if line:
            parts = line.split(' ')
            parts = filter(None, parts)
            url = parts[1]
            branch = parts[2]
            sections = parts[3:]
            repo = [url, branch, sections]
            sourceslist.append(repo)

    for url, branch, sections in sourceslist:
        for section in sections:
            for arch in archlist:
                read = 0
                blocknum = 0
                contentheader = 0
                message.set_markup(progressmessage.format(section, branch, '\n', url, arch))
                requesturl = url+'/dists/'+branch+'/'+section+'/binary-'+arch+'/Packages.gz'
                time.sleep(1)

                if download:
                    urlname = replace_all(url, forbidden_filename_chars)
                    pkgcache = tempfile.NamedTemporaryFile(
                        prefix = urlname+'-'+branch+'-',
                        suffix = '-'+section+'_'+arch+'.gz',
                        dir = tempdir, delete = False
                        )

                try:
                    if download:
                        response = urllib2.urlopen(requesturl)
                    else:
                        response = urllib2.urlopen(HeadRequest(requesturl))
                except urllib2.HTTPError as e:
                    errorcode = str(e.code)
                    errorcounter += 1
                except urllib2.URLError as e:
                    errorcode = str(e.reason)
                    errorcounter += 1
                except IOError as e:
                    errorcode = str(e.errno)+': '+str(e.strerror)
                    errorcounter += 1
                except ValueError as e:
                    errorcode = str(e)
                    errorcounter += 1
                except TypeError as e:
                    errorcode = str(e)
                    errorcounter += 1
                except:
                    errorcode = str(sys.exc_info()[0])
                    errorcounter += 1
                else:
                    headers = response.info()
                    contentheader = int(headers["Content-Length"])

                if contentheader == 0:
                    errorcode = ''
                    errorcounter += 1

                if download:
                    if errorcounter == 0:
                        while True:
                            block = response.read(bs)
                            if not block:
                                break
                            pkgcache.write(block)
                            pkgcache.flush()
                            os.fsync(pkgcache.fileno())
                            read += len(block)
                            blocknum += 1
                            percent = float(blocknum*bs)/contentheader
                            if percent >= 1:
                                percent = 1
                            bar.set_fraction(percent)

                        pkgcache.close()
                        response.close()

                    if read < contentheader:
                        errorcode = ''
                        errorcounter += 1
    if not download:
        gobject.source_remove(timer)

    q_bar.put(bar)
    q_msg.put(message)
    q_code.put(errorcode)
    q_counter.put(errorcounter)
    event.set()

def Toggle(r, do, dont = False, children = False,
    morechildren = False, alwaysoff = False):

    if children:
        widgetlist = do.get_children()
        if morechildren:
            for widget in widgetlist:
                morewidgets = widget.get_children()
                widgetlist = widgetlist + morewidgets
    else:
        widgetlist = do

    for widget in widgetlist:
        if widget != dont:
            if widget.get_sensitive() or alwaysoff:
                setting = False
            else:
                setting = True
            widget.set_sensitive(setting)

def ChangeCodename(r, c, codenamecombo, db):
    codenamelist, codenameactive = CodenameList(c, r, db)
    codenamecombo.get_model().clear()
    for item in codenamelist:
        codenamecombo.append_text(item)
    codenamecombo.set_active(codenameactive)

def ChangeRepo(r, c, repoentry):
    dist = r.get_active_text()
    exec "newrepotext = "+dist+"_repo"
    repoentry.set_text(newrepotext)

def ChangeSections(r, c, sections):
    checklist = SectionList(c, r)
    checkdefault = section_default
    children = sections.get_children()
    for child in children:
        sections.remove(child)
    for item in checklist:
        check = gtk.CheckButton(item)
        if item == checkdefault:
            check.set_active(True)
            check.set_sensitive(False)
        check.show()
        sections.pack_start(check, expand, fill, padding)

def AddExtraRepos(c, url_entry, branch_entry, sections_entry, arch_container,
                repolistframe):

    archs = []
    errorcounter = 0
    url = url_entry.get_text()
    branch = branch_entry.get_text()
    sections = sections_entry.get_text()
    repolist = repolistframe.get_text(*repolistframe.get_bounds())
    q_window = Queue.Queue()
    q_bar = Queue.Queue()
    q_msg = Queue.Queue()
    q_code = Queue.Queue()
    q_counter = Queue.Queue()
    event = threading.Event()

    for child in arch_container.get_children():
        if child.get_active():
            archs.append(child.get_label())

    sourcestext = 'deb '+url+' '+branch+' '+sections+'\n'

    if is_valid_url(url):
        if archs:
            if repolist.find(sourcestext) == -1:
                window_thread = ThreadGenerator(
                    reference = c, function = ProgressWindow,
                    params = {
                        'text': PROFILE_OS_EXTRAREPOS_VALIDATE_MSG,
                        'title': PROFILE_OS_EXTRAREPOS_VALIDATE_TITLE,
                        'q_window': q_window,
                        'q_bar': q_bar,
                        'q_msg': q_msg
                        }
                    )

                index_thread = ThreadGenerator(
                    reference = c, function = TestIndexes,
                    params = {
                        'sourcestext': sourcestext,
                        'archlist': archs,
                        'progressmessage': PROFILE_OS_EXTRAREPOS_VALIDATE_MSG,
                        'download': False,
                        'q_bar': q_bar,
                        'q_msg': q_msg,
                        'q_code': q_code,
                        'q_counter': q_counter,
                        'event': event
                        }
                    )

                write_thread = ThreadGenerator(
                    reference = c, function = WriteExtraRepos,
                    params = {
                        'c': c,
                        'url': url,
                        'branch': branch,
                        'sections': sections,
                        'repolistframe': repolistframe,
                        'repolist': repolist,
                        'q_window': q_window,
                        'q_code': q_code,
                        'q_counter': q_counter
                        },
                    event = event
                    )
        else:
            msg_thread = ThreadGenerator(
                reference = c, gtk = True, window = False,
                function = UserMessage, params = {
                    'message': PROFILE_OS_EXTRAREPOS_VALIDATE_ARCH_ERROR_MSG.format('\n\n'),
                    'title': PROFILE_OS_EXTRAREPOS_VALIDATE_ARCH_ERROR_TITLE,
                    'type': gtk.MESSAGE_ERROR,
                    'buttons': gtk.BUTTONS_CLOSE
                    }
                )
    else:
        msg_thread = ThreadGenerator(
            reference = c, gtk = True, window = False,
            function = UserMessage, params = {
                'message': PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_MSG.format(url, '\n\n'),
                'title': PROFILE_OS_EXTRAREPOS_VALIDATE_URL_ERROR_TITLE,
                'type': gtk.MESSAGE_ERROR,
                'buttons': gtk.BUTTONS_CLOSE
                }
            )

def WriteExtraRepos(c, url, branch, sections, repolistframe, repolist,
                    q_window, q_code, q_counter):

    window = q_window.get()
    errorcode = q_code.get()
    errorcounter = q_counter.get()

    if errorcounter != 0:
        msg_thread = ThreadGenerator(
            reference = c, gtk = True, window = False,
            function = UserMessage, params = {
                'message': PROFILE_OS_EXTRAREPOS_VALIDATE_REPO_ERROR_MSG.format(errorcode, '\n\n', '\n\n'),
                'title': PROFILE_OS_EXTRAREPOS_VALIDATE_REPO_ERROR_TITLE,
                'type': gtk.MESSAGE_ERROR,
                'buttons': gtk.BUTTONS_CLOSE
                }
            )
    else:
        repolistframe.set_text(repolist+'deb '+url+' '+branch+' '+sections+'\n')

    window.destroy()

def AddPackages(c, url_entry, branch_entry, section_container, arch_container,
                    extrareposframe, packages_entry, packageslistframe):

    archs = []
    sections = ''
    errorcounter = 0
    found = 0
    url = url_entry.get_text()
    branch = branch_entry.get_active_text()
    extrarepos = extrareposframe.get_text(*extrareposframe.get_bounds())
    packageslist = packageslistframe.get_text(*packageslistframe.get_bounds())
    packages = packages_entry.get_text()
    q_window = Queue.Queue()
    q_bar = Queue.Queue()
    q_msg = Queue.Queue()
    q_code = Queue.Queue()
    q_counter = Queue.Queue()
    event = threading.Event()

    for child in section_container.get_children():
        if child.get_active():
            sections = sections+child.get_label()+' '

    for child in arch_container.get_children():
        if child.get_active():
            archs.append(child.get_label())

    sourcestext = 'deb '+url+' '+branch+' '+sections+'\n'+extrarepos

    if archs:
        window_thread = ThreadGenerator(
            reference = c, function = ProgressWindow,
            params = {
                'text': PROFILE_OS_PACKAGES_VALIDATE_MSG,
                'title': PROFILE_OS_PACKAGES_VALIDATE_TITLE,
                'q_window': q_window,
                'q_bar': q_bar,
                'q_msg': q_msg
                }
            )

        index_thread = ThreadGenerator(
            reference = c, function = TestIndexes,
            params = {
                'sourcestext': sourcestext,
                'archlist': archs,
                'progressmessage': PROFILE_OS_PACKAGES_VALIDATE_MSG,
                'download': True,
                'q_bar': q_bar,
                'q_msg': q_msg,
                'q_code': q_code,
                'q_counter': q_counter,
                'event': event
                }
            )

        write_thread = ThreadGenerator(
            reference = c, function = WritePackages,
            params = {
                'c': c,
                'packages': packages,
                'packageslistframe': packageslistframe,
                'packageslist': packageslist,
                'q_window': q_window,
                'q_msg': q_msg,
                'q_bar': q_bar,
                'q_code': q_code,
                'q_counter': q_counter
                },
            event = event
            )
    else:
        msg_thread = ThreadGenerator(
            reference = c, gtk = True, window = False,
            function = UserMessage, params = {
                'message': PROFILE_OS_PACKAGES_VALIDATE_ARCH_ERROR_MSG.format('\n\n'),
                'title': PROFILE_OS_PACKAGES_VALIDATE_ARCH_ERROR_TITLE,
                'type': gtk.MESSAGE_ERROR,
                'buttons': gtk.BUTTONS_CLOSE
                }
            )

def WritePackages(c, packages, packageslistframe, packageslist,
                    q_window, q_msg, q_bar, q_code, q_counter):

    window = q_window.get()
    bar = q_bar.get()
    message = q_msg.get()
    errorcode = q_code.get()
    errorcounter = q_counter.get()

    if errorcounter > 0:
        build_thread = ThreadGenerator(
            reference = c, gtk = True, window = False,
            function = UserMessage, params = {
                'message': PROFILE_OS_PACKAGES_VALIDATE_REPO_ERROR_MSG.format(errorcode, '\n\n', '\n\n'),
                'title': PROFILE_OS_PACKAGES_VALIDATE_REPO_ERROR_TITLE,
                'type': gtk.MESSAGE_ERROR,
                'buttons': gtk.BUTTONS_CLOSE
                }
            )
    else:
        timer = gobject.timeout_add(100, ProgressPulse, bar)
        for package in packages.split(' '):
            found = 0
            message.set_markup(PROFILE_OS_PACKAGES_VALIDATE_PKG_MSG.format(package, '\n'))
            for path in os.listdir(tempdir):
                if os.path.isfile(tempdir+path) and fnmatch.fnmatch(tempdir+path, '*.gz'):
                    zipfile = gzip.open(tempdir+path)
                    for line in zipfile.readlines():
                        if line == 'Package: '+package+'\n':
                            found += 1
                    zipfile.close()

            if found > 0:
                packageslist = packageslistframe.get_text(*packageslistframe.get_bounds())
                packageslistframe.set_text(packageslist+' '+package)
            else:
                build_thread = ThreadGenerator(
                    reference = c, gtk = True, window = False,
                    function = UserMessage, params = {
                        'message': PROFILE_OS_PACKAGES_VALIDATE_PKG_ERROR_MSG.format(package),
                        'title': PROFILE_OS_PACKAGES_VALIDATE_PKG_ERROR_TITLE,
                        'type': gtk.MESSAGE_ERROR,
                        'buttons': gtk.BUTTONS_CLOSE
                        }
                    )
        gobject.source_remove(timer)
    window.destroy()

def BuildImage(c, profile_container, arch_container, media_container,
                window_container):

    profile = profile_container.get_active_text()
    arch_children = arch_container.get_children()
    media_children = media_container.get_children()
    q_window = Queue.Queue()
    q_bar = Queue.Queue()
    q_msg = Queue.Queue()
    q_terminal = Queue.Queue()
    q_code = Queue.Queue()
    q_counter = Queue.Queue()
    event = threading.Event()

    Toggle(
        r = c, dont = None, do = window_container, children = False,
        morechildren = False, alwaysoff = True
        )

    for child in arch_children:
        if child.get_active():
            if child.get_label() == BUILD_PROFILE_ARCH_AMD64:
                arch = 'amd64'
            else:
                arch = 'i386'

    for child in media_children:
        if child.get_active():
            if child.get_label() == BUILD_PROFILE_MEDIA_ISO:
                media = 'iso'
            elif child.get_label() == BUILD_PROFILE_MEDIA_IMG:
                media = 'usb'
            else:
                media = 'iso-hybrid'

    if os.path.exists(PROFILEDIR+'/'+profile+'/profile.conf'):
        get = ['META_REPO', 'META_CODENAME', 'META_REPOSECTIONS']
        config = ParseProfileConfig(profile, get)

        meta_repo = config['META_REPO']
        meta_reposections = config['META_REPOSECTIONS']
        meta_codename = config['META_CODENAME']
        mainrepo = 'deb '+meta_repo+' '+meta_codename+' '+meta_reposections+'\n'
    else:
        mainrepo = ''

    if os.path.exists(PROFILEDIR+'/'+profile+'/extra-repos.list'):
        f = open(PROFILEDIR+'/'+profile+'/extra-repos.list', 'r')
        extrarepos = f.read()
    else:
        extrarepos = ''

    sourcestext = mainrepo+extrarepos

    window_thread = ThreadGenerator(
        reference = c, function = ProgressWindow,
        params = {
            'text': BUILD_VALIDATE_SOURCES_MSG,
            'title': BUILD_WINDOW_TITLE,
            'term': True,
            'fcancel': KillProcess,
            'pcancel': (['lb', 'live-build', 'c-s'],),
            'q_window': q_window,
            'q_bar': q_bar,
            'q_msg': q_msg,
            'q_terminal': q_terminal
            }
        )

    index_thread = ThreadGenerator(
        reference = c, function = TestIndexes,
        params = {
            'sourcestext': sourcestext,
            'archlist': [arch,],
            'progressmessage': BUILD_VALIDATE_SOURCES_MSG,
            'download': False,
            'q_bar': q_bar,
            'q_msg': q_msg,
            'q_code': q_code,
            'q_counter': q_counter,
            'event': event
            }
        )

    build_thread = ThreadGenerator(
        reference = c, function = StartCS,
        params = {
            'c': c,
            'arch': arch,
            'media': media,
            'profile': profile,
            'q_bar': q_bar,
            'q_msg': q_msg,
            'q_terminal': q_terminal,
            'q_code': q_code,
            'q_counter': q_counter,
            'window': window_container
            },
        event = event
        )

def StartCS(c, arch, media, profile, q_bar, q_msg, q_terminal,
            q_code, q_counter, window):

    bar = q_bar.get()
    message = q_msg.get()
    terminal = q_terminal.get()
    errorcode = q_code.get()
    errorcounter = q_counter.get()

    if errorcounter != 0:
        build_thread = ThreadGenerator(
            reference = c, gtk = True, window = False,
            function = UserMessage, params = {
                'message': BUILD_VALIDATE_SOURCES_ERROR_MSG.format('\n\n'),
                'title': BUILD_VALIDATE_SOURCES_ERROR_TITLE,
                'type': gtk.MESSAGE_ERROR,
                'buttons': gtk.BUTTONS_CLOSE,
                'c_1': gtk.RESPONSE_CLOSE, 'f_1': Toggle,
                'p_1': (c, None, window, False, False, False)
                }
            )
    else:
        message.set_markup(BUILD_PROCESS_STATUS)
        process = ProcessGenerator(
            ['/bin/sh', BINDIR+'/'+CSBIN, 'build', '-a', arch, '-m', media, '-s', profile],
            terminal, bar
            )

        if process.returncode == 0:
            build_thread = ThreadGenerator(
                reference = c, gtk = True, window = False,
                function = UserMessage, params = {
                    'message': BUILD_SUCCESSFUL_MSG,
                    'title': BUILD_SUCCESSFUL_TITLE,
                    'type': gtk.MESSAGE_ERROR,
                    'buttons': gtk.BUTTONS_CLOSE,
                    'c_1': gtk.RESPONSE_CLOSE, 'f_1': Toggle,
                    'p_1': (c, None, window, False, False, False)
                    }
                )
        else:
            build_thread = ThreadGenerator(
                reference = c, gtk = True, window = False,
                function = UserMessage, params = {
                    'message': BUILD_FAILED_MSG,
                    'title': BUILD_FAILED_TITLE,
                    'type': gtk.MESSAGE_INFO,
                    'buttons': gtk.BUTTONS_OK,
                    'c_1': gtk.RESPONSE_OK, 'f_1': Toggle,
                    'p_1': (c, None, window, False, False, False)
                    }
                )

def ProgressPulse(bar):
    bar.pulse()
    return True

def CreateProfile(c, profilename, profilearch, authorname, authoremail,
                    authorurl, oslocale, metadist, metacodename, metarepo,
                    metareposections, osextrarepos, ospackages, imgpoolpackages,
                    osincludes, imgincludes, oshooks, imghooks,
                    imgsyslinuxsplash, imgdebianinstaller,
                    imgdebianinstallerbanner, imgdebianinstallerpreseed,
                    imgdebianinstallergtk
                    ):

    _profilearch = ''
    for child in profilearch.get_children():
        if child.get_active():
            _profilearch = _profilearch+child.get_label()+' '

    _metareposections = ''
    for child in metareposections.get_children():
        if child.get_active():
            _metareposections = _metareposections+child.get_label()+' '

    _profilename = profilename.get_text()
    _authorname = authorname.get_text()
    _authoremail = authoremail.get_text()
    _authorurl = authorurl.get_text()
    _oslocale = oslocale.get_active_text()
    _metadist = metadist.get_active_text()
    _metacodename = metacodename.get_active_text()
    _metarepo = metarepo.get_text()
    _ospackages = ospackages.get_text(*ospackages.get_bounds())
    _osextrarepos = osextrarepos.get_text(*osextrarepos.get_bounds())
    _imgpoolpackages = imgpoolpackages.get_text(*imgpoolpackages.get_bounds())
    _osincludes = osincludes.get_text()
    _imgincludes = imgincludes.get_text()
    _oshooks = oshooks.get_text()
    _imghooks = imghooks.get_text()
    _imgsyslinuxsplash = imgsyslinuxsplash.get_text()
    _imgdebianinstaller = str(imgdebianinstaller.get_active()).lower()
    _imgdebianinstallerbanner = imgdebianinstallerbanner.get_text()
    _imgdebianinstallerpreseed = imgdebianinstallerpreseed.get_text()
    _imgdebianinstallergtk = imgdebianinstallergtk.get_text()

    profile_name = 'PROFILE_NAME="'+_profilename+'"\n'
    profile_arch = 'PROFILE_ARCH="'+_profilearch+'"\n'
    author_name = 'AUTHOR_NAME="'+_authorname+'"\n'
    author_email = 'AUTHOR_EMAIL="'+_authoremail+'"\n'
    author_url = 'AUTHOR_URL="'+_authorurl+'"\n'
    os_locale = 'OS_LOCALE="'+_oslocale+'"\n'
    meta_dist = 'META_DIST="'+_metadist+'"\n'
    meta_codename = 'META_CODENAME="'+_metacodename+'"\n'
    meta_repo = 'META_REPO="'+_metarepo+'"\n'
    meta_reposections = 'META_REPOSECTIONS="'+_metareposections+'"\n'
    os_packages = 'OS_PACKAGES="'+_ospackages+'"\n'
    os_extrarepos = 'OS_EXTRAREPOS="profile"\n'
    img_pool_packages = 'IMG_POOL_PACKAGES="'+_imgpoolpackages+'"\n'
    os_includes = 'OS_INCLUDES="profile"\n'
    img_includes = 'IMG_INCLUDES="profile"\n'
    os_hooks = 'OS_HOOKS="profile"\n'
    img_hooks = 'IMG_HOOKS="profile"\n'
    img_syslinux_splash = 'IMG_SYSLINUX_SPLASH="profile"\n'
    img_debian_installer = 'IMG_DEBIAN_INSTALLER="'+_imgdebianinstaller+'"\n'
    img_debian_installer_banner = 'IMG_DEBIAN_INSTALLER_BANNER="profile"\n'
    img_debian_installer_preseed = 'IMG_DEBIAN_INSTALLER_PRESEED="profile"\n'
    img_debian_installer_gtk = 'IMG_DEBIAN_INSTALLER_GTK="profile"\n'

    content = profile_name+profile_arch+author_name+author_email+author_url+os_locale+meta_dist+meta_codename+meta_repo+meta_reposections+os_extrarepos+os_packages+img_pool_packages+os_includes+img_includes+os_hooks+img_hooks+img_syslinux_splash+img_debian_installer+img_debian_installer_banner+img_debian_installer_preseed+img_debian_installer_gtk

    if not os.path.exists(PROFILEDIR+'/'+_profilename):
        os.mkdir(PROFILEDIR+'/'+_profilename)
        f = open(PROFILEDIR+'/'+_profilename+'/profile.conf', 'wb')
        f.write(content)
        f.close()
        
        if _osextrarepos:
            e = open(PROFILEDIR+'/'+_profilename+'/extra-repos.list', 'wb')
            e.write(_osextrarepos)
            e.close()

        copythis = [
            [ _osincludes, PROFILEDIR+'/'+_profilename+'/OS_INCLUDES'],
            [ _oshooks, PROFILEDIR+'/'+_profilename+'/OS_HOOKS'],
            [ _imgincludes, PROFILEDIR+'/'+_profilename+'/IMG_INCLUDES'],
            [ _imghooks, PROFILEDIR+'/'+_profilename+'/IMG_HOOKS'],
            [ _imgsyslinuxsplash, PROFILEDIR+'/'+_profilename],
            [ _imgdebianinstallerbanner, PROFILEDIR+'/'+_profilename+'/DEBIAN_INSTALLER'],
            [ _imgdebianinstallerpreseed, PROFILEDIR+'/'+_profilename+'/DEBIAN_INSTALLER'],
            [ _imgdebianinstallergtk, PROFILEDIR+'/'+_profilename+'/DEBIAN_INSTALLER'],
        ]

        if copy2destination(copythis):
            success_thread = ThreadGenerator(
                reference = c, gtk = True, window = False,
                function = UserMessage, params = {
                    'message': PROFILE_CREATING_SUCCESS_MSG,
                    'title': PROFILE_CREATING_SUCCESS_TITLE,
                    'type': gtk.MESSAGE_INFO,
                    'buttons': gtk.BUTTONS_OK
                    }
                )
        else:
            error_thread = ThreadGenerator(
                reference = c, gtk = True, window = False,
                function = UserMessage, params = {
                    'message': PROFILE_CREATING_UNKNOWN_ERROR_MSG,
                    'title': PROFILE_CREATING_UNKNOWN_ERROR_TITLE,
                    'type': gtk.MESSAGE_ERROR,
                    'buttons': gtk.BUTTONS_OK
                    }
                )
    else:
        error_thread = ThreadGenerator(
            reference = c, gtk = True, window = False,
            function = UserMessage, params = {
                'message': PROFILE_CREATING_EXISTS_ERROR_MSG,
                'title': PROFILE_CREATING_EXISTS_ERROR_TITLE,
                'type': gtk.MESSAGE_ERROR,
                'buttons': gtk.BUTTONS_OK
                }
            )

def TestImage(c, image_entry, memory_entry, processors_entry, start_container):

    image = image_entry.get_text()
    memory = memory_entry.get_value()
    processors = processors_entry.get_value()

    for child in start_container.get_children():
        if child.get_active():
            if child.get_label() == TEST_START_CD_LABEL:
                start = '-c'
            else:
                start = '-d'

    build_thread = ThreadGenerator(
        reference = c, gtk = False, window = False,
        function = ProcessGenerator, params = {
            'command': [
                '/bin/sh', BINDIR+'/'+CSBIN, 'test', '-i', image,
                '-m', str(int(memory)), '-p', str(int(processors)), start, '-n',
                '-s', '10'
                ]
            }
        )

def SaveImage(c, device_combo, image_entry, window_container):

    device = device_combo.get_active_text()
    image = image_entry.get_text()
    q_window = Queue.Queue()
    q_bar = Queue.Queue()
    q_msg = Queue.Queue()
    q_terminal = Queue.Queue()

    window_thread = ThreadGenerator(
        reference = c, function = ProgressWindow,
        params = {
            'text': SAVE_WRITE_MSG,
            'title': SAVE_WRITE_TITLE,
            'term': True,
            'fcancel': KillProcess,
            'pcancel': (['wodim', 'c-s', 'dd'],),
            'q_window': q_window,
            'q_bar': q_bar,
            'q_msg': q_msg,
            'q_terminal': q_terminal
            }
        )

    window_thread = ThreadGenerator(
        reference = c, function = SaveImage2,
        params = {
            'c': c,
            'image': image,
            'device': device,
            'q_bar': q_bar,
            'q_msg': q_msg,
            'q_terminal': q_terminal,
            'window': window_container
            }
        )

def SaveImage2(c, image, device, q_bar, q_msg, q_terminal, window):

    bar = q_bar.get()
    message = q_msg.get()
    terminal = q_terminal.get()

    process = ProcessGenerator(
        ['/bin/sh', BINDIR+'/'+CSBIN, 'save', '-i', image, '-d', device, '-q'],
        terminal, bar
        )

    if process.returncode == 0:
        build_thread = ThreadGenerator(
            reference = c, gtk = True, window = False,
            function = UserMessage, params = {
                'message': SAVE_SUCCESSFUL_MSG,
                'title': SAVE_SUCCESSFUL_TITLE,
                'type': gtk.MESSAGE_ERROR,
                'buttons': gtk.BUTTONS_CLOSE,
                'c_1': gtk.RESPONSE_CLOSE, 'f_1': Toggle,
                'p_1': (c, window)
                }
            )
    else:
        build_thread = ThreadGenerator(
            reference = c, gtk = True, window = False,
            function = UserMessage, params = {
                'message': SAVE_FAILED_MSG,
                'title': SAVE_FAILED_TITLE,
                'type': gtk.MESSAGE_INFO,
                'buttons': gtk.BUTTONS_OK,
                'c_1': gtk.RESPONSE_OK, 'f_1': Toggle,
                'p_1': (c, window)
                }
            )
