from distutils.cmd import Command
from distutils.command.clean import clean as base_clean


class clean_img(Command):
    description = 'Compile .po files into .mo files'
    def initialize_options(self):
        pass
 
    def finalize_options(self):
        pass
 
    def run(self):
        print 'Cleaning images'


class clean_html(Command):
    description = 'Compile .po files into .mo files'
    def initialize_options(self):
        pass
 
    def finalize_options(self):
        pass
 
    def run(self):
        print 'Cleaning html'


class clean_man(Command):
    description = 'Compile .po files into .mo files'
    def initialize_options(self):
        pass
 
    def finalize_options(self):
        pass
 
    def run(self):
        print 'Cleaning man'


class clean_mo(Command):
    description = 'Compile .po files into .mo files'
    def initialize_options(self):
        pass
 
    def finalize_options(self):
        pass
 
    def run(self):
        print 'Cleaning mo'
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

class clean(base_clean):
    def run(self):
        self.run_command('clean_mo')
        self.run_command('clean_img')
        self.run_command('clean_html')
        self.run_command('clean_man')
        base_clean.run(self)

