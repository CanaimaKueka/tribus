
from distutils.cmd import Command
from distutils.command.install_data import install_data as base_install_data

class install_data(base_install_data):
 
    def run(self):
        # for lang in os.listdir('build/locale/'):
        #     lang_dir = os.path.join('share', 'locale', lang, 'LC_MESSAGES')
        #     lang_file = os.path.join('build', 'locale', lang, 'LC_MESSAGES', 'mussorgsky.mo')
        #     self.data_files.append( (lang_dir, [lang_file]) )
        base_install_data.run(self)