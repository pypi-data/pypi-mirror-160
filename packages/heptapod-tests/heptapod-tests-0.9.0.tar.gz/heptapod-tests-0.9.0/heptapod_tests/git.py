import logging
import os
import subprocess

GIT_EXECUTABLE = 'git'

logger = logging.getLogger(__name__)


def git_call(cwd, cmd,
             env=None,
             ssh_cmd=None,
             check_return_code=True,
             expected_return_code=0):
    """Wrapper to run git, allowing process error or not.


    :param check_status_code:
        if ``True``, and hg status code isn't 0, raises like an stderr variant
        of ``subprocess.check_output()``.
    :param encoding: if `None`, the default encoding is used
    """
    gitcmd = [GIT_EXECUTABLE]
    gitcmd.extend(str(s) if not isinstance(s, bytes) else s for s in cmd)
    if env is None:
        env = os.environ.copy()

    if ssh_cmd is not None:
        env['GIT_SSH_COMMAND'] = ssh_cmd

    proc = subprocess.Popen(gitcmd,
                            cwd=str(cwd),
                            env=env,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = [b.decode('utf-8', 'replace') for b in proc.communicate()]
    retcode = proc.poll()
    if check_return_code and retcode != expected_return_code:
        # logging at ERROR level because if it had been expected
        # call would have used `check_return_code=False`
        logger.error("Failed git_call (code %d, expected %d), "
                     "stdout=%r, stderr=%r",
                     retcode, expected_return_code, out, err)
        raise subprocess.CalledProcessError(retcode, cmd, output=err)
    return retcode, out, err


class LocalRepo(object):
    """Represent a repository on the system where the tests are run."""

    def __init__(self, path):
        self.path = path

    @classmethod
    def init(cls, path, default_url=None):
        """Create a repository at the given path and attach it to the given URL.

        :param path: a pytest Path instance
        :param url: Optional Heptapod URL of the repo, will become the
                    default path for push/pull operations.
                    In most cases, one would want the URL to enclose
                    Basic Authentication credentials, but it's not necessary.


        """
        git_call('.', ['init', path])
        repo = cls(path)

        if default_url is not None:
            repo.git('remote', 'add', 'origin', default_url)

        repo.configure_default_user()
        return repo

    @classmethod
    def clone(cls, url, path, ssh_cmd=None, expected_return_code=0):
        """Clone the repository from given URL.

        :param path: a pytest Path instance
        """
        git_call('.', ['clone', url, path], ssh_cmd=ssh_cmd,
                 expected_return_code=expected_return_code)
        repo = cls.init(path)
        return repo

    def configure_default_user(self):
        self.git('config', 'user.name', 'Test Git')
        self.git('config', 'user.email', 'testgit@heptapod.test')

    def git(self, *args, **kwargs):
        """Invoke the `git` executable and return its stdout.

        This behaves as `subprocess.check_output` does.
        """
        return git_call(self.path, args, **kwargs)[1]

    def git_unchecked(self, *args, **kwargs):
        """Invoke the `git` executable without raising based on return code

        :returns: (process return code, stdout, stderr).
        """
        return git_call(self.path, args, check_return_code=False, **kwargs)

    def graphlog(self):
        return self.git('log', '--all', '--graph')

    def sha(self, ref):
        return self.git('log', '--pretty=%H', '-n1', ref).strip()
