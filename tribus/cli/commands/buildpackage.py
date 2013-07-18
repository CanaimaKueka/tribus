from tribus.common.cmd import Helper


class BuildPackage(Helper):

    helper_name = 'buildpackage'
    helper_help = 'Helps build a package'
    helper_args = {
        'version': [['-v', '--version'], {
            'action': 'store_true',
            'dest': 'print_version',
            'default': False
        }],
    }

    def __init__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        print self.subcommand_name
