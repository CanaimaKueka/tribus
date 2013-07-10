from distutils.cmd import Command
from distutils.command.build import build as base_build


class build_img(Command):
    description = 'Compile .po files into .mo files'
    def initialize_options(self):
        pass
 
    def finalize_options(self):
        pass
 
    def run(self):
        print 'Compiling images'


class build_html(Command):
    description = 'Compile .po files into .mo files'
    def initialize_options(self):
        pass
 
    def finalize_options(self):
        pass
 
    def run(self):
        print 'Compiling html'


class build_man(Command):
    description = 'Compile .po files into .mo files'
    def initialize_options(self):
        pass
 
    def finalize_options(self):
        pass
 
    def run(self):
        print 'Compiling man'


class build_mo(Command):
    description = 'Compile .po files into .mo files'
    def initialize_options(self):
        pass
 
    def finalize_options(self):
        pass
 
    def run(self):
        print 'Compiling mo'
        # po_dir = os.path.join(os.path.dirname(os.curdir), 'po')
        # for path, names, filenames in os.walk(po_dir):
        #     for f in filenames:
        #         if f.endswith('.po'):
        #             lang = f[:-3]
        #             src = os.path.join(path, f)
        #             dest_path = os.path.join('build', 'locale', lang, 'LC_MESSAGES')
        #             dest = os.path.join(dest_path, 'mussorgsky.mo')
        #             if not os.path.exists(dest_path):
        #                 os.makedirs(dest_path)
        #             if not os.path.exists(dest):
        #                 print 'Compiling %s' % src
        #                 msgfmt.make(src, dest)
        #             else:
        #                 src_mtime = os.stat(src)[8]
        #                 dest_mtime = os.stat(dest)[8]
        #                 if src_mtime > dest_mtime:
        #                     print 'Compiling %s' % src
        #                     msgfmt.make(src, dest)

class build(base_build):
    def run(self):
        self.run_command('clean')
        self.run_command('build_mo')
        self.run_command('build_img')
        self.run_command('build_html')
        self.run_command('build_man')
        base_build.run(self)

