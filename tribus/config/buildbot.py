import os
from buildbot.status.html import WebStatus
from buildbot.status.web.authz import Authz
from buildbot.status.web.auth import BasicAuth
from buildbot.schedulers import basic
from buildbot.schedulers.basic import SingleBranchScheduler
from buildbot.buildslave import BuildSlave
from buildbot.process.factory import BuildFactory
from buildbot.steps.source import Git
from buildbot.steps.shell import ShellCommand
from buildbot.changes.gitpoller import GitPoller
from buildbot.config import BuilderConfig
from buildbot.changes.filter import ChangeFilter

# Diccionario que contiene la configuracion de buildmaster

c = BuildmasterConfig = {}

# inicializacion de variables

c['status'] = []
c['slaves'] = []
c['change_source'] = []
c['schedulers'] = []
c['builders'] = []
c['buildbotURL'] = 'http://localhost:8010/'
c['protocols'] = {'pb': {'port': 9989}}

#Lista de los paquetes
packages = {}
packages['list'] = filter(None, open('gitrepos.list', 'r').read().split('\n'))

#Informacion sobre repositorio y controlador de versiones
# VCS info
vcs = {}
vcs['branch'] = 'master'
vcs['time'] = 60
vcs['pollinterval'] = 60

##### Configuracion de los esclavos
####### BUILD SLAVES CONFIGURATION

# Definicion de esclavos

slaves = {}
slaves['buildbot-i386'] = {'arch':'i386', 
                           'dist':'jessie',
                           'user':'buildbot-i386',
                           'passwd':'123'}
# slaves['buildbot-amd64'] = {'arch':'amd64', 
#                            'dist':'jessie',
#                            'user':'buildbot-amd64',
#                            'passwd':'123'}

####### CHANGE SOURCE CONFIGURATION
#Definicion de repositorio y revision de los cambio

for repo in packages['list']:
    package = os.path.basename(repo)
    c['change_source'].append(
        GitPoller(repourl=repo,
                  project=package,
                  branch=vcs['branch'],
                  pollinterval=vcs['pollinterval'])
        )

####### BUILDERS CONFIGURATION
# construir la lista de arquitecturas

arch = {}

for s in slaves.keys():
    vm = slaves[s]
    arch[vm['arch']] = 1

for a in arch.keys():
    e = []
    for s in slaves.keys():
        if slaves[s]['arch'] == a:
            e.append(s)
    arch[a] = e

for s in slaves.keys():
    c['slaves'].append(BuildSlave(slaves[s]['user'], slaves[s]['passwd']))

builders = {}

for repo in packages['list']:

    for a in arch.keys():

        package = os.path.basename(repo)
        n = package + '-' + a
        builders[n] = arch[a]
        f = BuildFactory()
        f.addStep(ShellCommand(command='rm -rf *'))
        f.addStep(ShellCommand(command=['git', 'clone', repo], workdir='build/'))
        f.addStep(ShellCommand(command=['git', 'checkout', vcs['branch']], workdir='build/'+package))
        f.addStep(ShellCommand(command=['git', 'buildpackage',
                                        '--git-pbuilder',
                                        '--git-dist=jessie',
                                        '--git-arch='+a,
                                        '-us', '-uc'],
                               workdir='build/'+package,
                               env={'DIST': 'jessie', 'ARCH': a, }))
        c['builders'].append(BuilderConfig(name=n, factory=f, slavenames=arch[a]))

####### SCHEDULERS CONFIGURATION
# define the periodic scheduler

for builder in builders.keys():
    project = '-'.join(builder.split('-')[:-1])
    sbched = SingleBranchScheduler(name=builder,
        change_filter=ChangeFilter(project=project, branch='master'),
        treeStableTimer=10,
        builderNames=[builder])
    # define the available schedulers
    c['schedulers'].append(sbched)


authz_cfg = Authz(
    # change any of these to True to enable; see the manual for more
    # options
    auth=BasicAuth([('pyflakes','pyflakes')]),
    gracefulShutdown = False,
    forceBuild = 'auth', # use this to test your slave once it is set up
    forceAllBuilds = False,
    pingBuilder = False,
    stopBuild = False,
    stopAllBuilds = False,
    cancelPendingBuild = False,
)

c['status'].append(WebStatus(http_port=8010, authz=authz_cfg))
