import subprocess
import os
import signal

from tribus.common.logger import get_logger

log = get_logger()


class Helper(object):

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self):
        pass


# Command class from git-buildpackage: gbp.command_wrappers

class Command(object):

    """
    Wraps a shell command, so we don't have to store any kind of command
    line options in one of the git-buildpackage commands
    """

    def __init__(self, cmd, args=[], shell=False, extra_env=None, cwd=None):
        self.cmd = cmd
        self.args = args
        self.run_error = ("Couldn't run '%s'" %
                         (" ".join([self.cmd] + self.args)))
        self.shell = shell
        self.retcode = 1
        self.cwd = cwd
        if extra_env is not None:
            self.env = os.environ.copy()
            self.env.update(extra_env)
        else:
            self.env = None

    def __call(self, args):
        """wraps subprocess.call so we can be verbose and fix
           python's SIGPIPE handling"""
        def default_sigpipe():
            "restore default signal handler (http://bugs.python.org/issue1652)"
            signal.signal(signal.SIGPIPE, signal.SIG_DFL)

        log.debug("%s %s %s" % (self.cmd, self.args, args))
        cmd = [self.cmd] + self.args + args
        # subprocess.call only cares about
        # the first argument if shell=True
        if self.shell:
            cmd = " ".join(cmd)
        return subprocess.call(cmd, cwd=self.cwd, shell=self.shell,
                               env=self.env, preexec_fn=default_sigpipe)

    def __run(self, args):
        """
        run self.cmd adding args as additional arguments

        Be verbose about errors and encode them in the return value, don't pass
        on exceptions.
        """
        try:
            retcode = self.__call(args)
            if retcode < 0:
                err_detail = ("%s was terminated by signal %d" %
                             (self.cmd, -retcode))
            elif retcode > 0:
                err_detail = "%s returned %d" % (self.cmd, retcode)
        except OSError as e:
            err_detail = "Execution failed: " + e.__str__()
            retcode = 1
        if retcode:
            log.err("%s: %s" % (self.run_error, err_detail))
        self.retcode = retcode
        return retcode

    def __call__(self, args=[]):
        """Run the command, convert all errors into CommandExecFailed, assumes
        that the lower levels printed an error message - only useful if you
        only expect 0 as result
        >>> Command("/bin/true")(["foo", "bar"])
        >>> Command("/foo/bar")()
        Traceback (most recent call last):
        ...
        CommandExecFailed
        """
        if self.__run(args):
            raise CommandExecFailed

    def call(self, args):
        """like __call__ but don't use stderr and let the caller
        handle the return status
        >>> Command("/bin/true").call(["foo", "bar"])
        0
        >>> Command("/foo/bar").call(["foo", "bar"]) # doctest:+ELLIPSIS
        Traceback (most recent call last):
        ...
        CommandExecFailed: Execution failed: ...
        """
        try:
            ret = self.__call(args)
        except OSError as e:
            raise CommandExecFailed("Execution failed: %s" % e)
        return ret
