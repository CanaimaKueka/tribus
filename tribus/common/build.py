import os
import cairosvg
from distutils.cmd import Command
from distutils.command.build import build as base_build

from tribus.config.pkg import svg_file_list
from tribus.common.logger import get_logger

log = get_logger()


class build_img(Command):
    description = 'Compile SVG files into PNG images.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        log.debug("[%s.%s] Compiling PNG images from SVG sources." % (__name__,
                                                                      self.__class__.__name__))
        for svg_file in svg_file_list:
            try:
                svg_code = open(svg_file, 'r').read()
            except Exception, e:
                print e

            try:
                png_file = open(os.path.splitext(svg_file)[0]+'.png', 'w')
            except Exception, e:
                print e

            try:
                cairosvg.svg2png(bytestring=svg_code, write_to=png_file)
            except Exception, e:
                print e

            png_file.close()
            log.debug("[%s.%s] %s > %s." % (__name__, self.__class__.__name__, svg_file,
                                            os.path.splitext(os.path.basename(svg_file))[0]+'.png'))


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


class build(base_build):
    def run(self):
        self.run_command('clean')
        self.run_command('build_mo')
        self.run_command('build_img')
        self.run_command('build_html')
        self.run_command('build_man')
        base_build.run(self)
