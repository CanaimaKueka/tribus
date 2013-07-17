import sys
import os
from optparse import OptionParser

path = os.path.join(os.path.dirname(__file__), '..')
base = os.path.realpath(os.path.abspath(os.path.normpath(path)))
os.environ['PATH'] = base + os.pathsep + os.environ['PATH']
sys.prefix = base
sys.path.insert(0, base)

DEFAULT_OPTIONS = {
    'version': [['-v', '--version'], {
        'action': 'store_true',
        'dest': 'print_version',
        'default': False
    }],
    'help': [['-h', '--help', '--ayuda'], {
        'action': 'store_true',
        'dest': 'print_help',
        'default': False
    }],
    'usage': [['-u', '--usage', '--uso'], {
        'action': 'store_true',
        'dest': 'print_usage',
        'default': False
    }],
}


def main():
    """
    Main command-line execution loop.
    """
    try:

        parser = OptionParser(usage=("tbs [COMMAND] [:arg1,arg2=val2,...] ..."))

        for _args, _kwargs in DEFAULT_OPTIONS.values():
            if parser.has_option(_args[0]):
                parser.remove_option(_args[0])
            parser.add_option(*_args, **_kwargs)

        # Parse command line options
        options, command = parser.parse_args()
        print options, command
        if not command:
            if options.print_help:
                parser.print_help()
            elif options.print_version:
                parser.print_version()
            else:
                parser.print_usage()
            parser.destroy()
        elif isinstance(command, list) and len(command) > 0:
            command = command[len(command) - 1]
        
            try:
                command_module = __import__('tribus.cli.commands.%s' % command)
                try:
                    if callable(command_module.execute):
                        command_module.execute(options=options)
                except Exception, e:
                    print e
            except ImportError:
                print 'The \'%s\' command does not exist. execute tbs --commands for an available command list.' % command
        
    except SystemExit:
        # a number of internal functions might raise this one.
        raise
    except KeyboardInterrupt:
        sys.stderr.write("\nStopped.\n")
        sys.exit(1)
    except:
        sys.excepthook(*sys.exc_info())
        # we might leave stale threads if we don't explicitly exit()
        sys.exit(1)
    finally:
        print 'end'
    sys.exit(0)


if __name__ == '__main__':
    main()