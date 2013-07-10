import os
from distutils.cmd import Command
from distutils.command.clean import clean as base_clean

from tribus.config.pkg import png_file_list, mo_file_list
from tribus.common.logger import get_logger

log = get_logger()


class clean_img(Command):
    description = 'Remove compiled PNG files from source.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for png_file in png_file_list:
            os.remove(png_file)
            log.debug("[%s.%s] Removing \"%s\"." % (__name__, self.__class__.__name__, png_file))


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
        for mo_file in mo_file_list:
            os.remove(mo_file)
            log.debug("[%s.%s] Removing \"%s\"." % (__name__, self.__class__.__name__, mo_file))

class clean(base_clean):
    def run(self):
        self.run_command('clean_mo')
        self.run_command('clean_img')
        self.run_command('clean_html')
        self.run_command('clean_man')
        base_clean.run(self)

