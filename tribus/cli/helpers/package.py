from tribus.common.commands import Helper


class Package(Helper):

    helper_name = 'buildpackage'
    helper_help = 'Helps build a package'
    helper_args = {
        'version': [['-v', '--version'], {
            'action': 'store_true',
            'dest': 'print_version',
            'default': False
        }],
    }

    helper_commands = {
        'create': '''


        ''',
        'download': ,
        'unpack': ,
        'upload': ,
        'describe': ,
        'download': ,
        'download': ,
        'download': ,
        'download': ,
    }
    package_dist = ['debian', 'fedora', 'python', 'ruby']
    package_types = ['source', 'binary']
    package_locations = ['local', 'remote']

    def __init__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        print self.subcommand_name
