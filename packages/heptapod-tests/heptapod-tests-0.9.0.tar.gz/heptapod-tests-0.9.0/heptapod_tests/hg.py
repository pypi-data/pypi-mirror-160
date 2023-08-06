# Copyright 2019-2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections import namedtuple
import json
import logging
import os
import subprocess

from .utils import (
    assert_message,
)
from .wait import (
    wait_assert,
)

SHORT_TEMPLATE = (
    '{rev}:{node|short} {desc|firstline} ({phase})\n'
    '{if (obsfate, "  obsolete:{obsfate}\n\n")}'
)
HG_EXECUTABLE = 'hg'
_hg_client_version = None  # a write-once constant

logger = logging.getLogger(__name__)


def hg_call(cwd, cmd, check_return_code=True, expected_return_code=0,
            encoding=None):
    """Wrapper to run hg, allowing process error or not.


    :param check_status_code:
        if ``True``, and hg status code isn't 0, raises like an stderr variant
        of ``subprocess.check_output()``.
    :param encoding: if `None`, the default encoding is used
    """
    hgcmd = [HG_EXECUTABLE]
    hgcmd.extend(str(s) if not isinstance(s, bytes) else s for s in cmd)
    if encoding is None:
        env = os.environ
    else:
        env = dict(os.environ)
        env['HGENCODING'] = encoding
    proc = subprocess.Popen(hgcmd,
                            cwd=str(cwd),  # -R not enough for hg init
                            env=env,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = [b.decode('utf-8', 'replace') for b in proc.communicate()]
    retcode = proc.poll()
    if check_return_code and retcode != expected_return_code:
        # logging at ERROR level because if it had been expected
        # call would have used `check_return_code=False`
        logger.error("Failed hg_call (code %d, expected %d), "
                     "stdout=%r, stderr=%r",
                     retcode, expected_return_code, out, err)
        raise subprocess.CalledProcessError(retcode, cmd, output=err)
    return retcode, out, err


def hg_client_version():
    global _hg_client_version

    if _hg_client_version is None:
        code, out, err = hg_call('.', ['debuginstall', '-T', '{hgver}'],
                                 check_return_code=False)
        assert code in (0, 1), err
        _hg_client_version = tuple(int(s) for s in out.split('.'))
        logger.info("Mercurial client executable %r, "
                    "version is %r", HG_EXECUTABLE, _hg_client_version)
    return _hg_client_version


class LocalRepo(object):
    """Represent a repository on the system where the tests are run."""

    hgrc_extensions_lines = ("[extensions]",
                             "evolve =",
                             "topic = ",
                             "rebase =",
                             "[ui]",
                             "username = Heptapod Tests <fonct@heptapod.test>"
                             )

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
        hg_call('.', ['init', path])
        repo = cls(path)

        hgrc_lines = list(cls.hgrc_extensions_lines)
        if default_url is not None:
            hgrc_lines.extend(("", "[paths]", "default = " + str(default_url)))
        repo.hgrc_append_lines(hgrc_lines)

        return repo

    @classmethod
    def clone(cls, url, path):
        """Clone the repository from given URL.

        :param path: a pytest Path instance
        """
        repo = cls.init(path, default_url=url)
        repo.hg('pull', '-u')
        return repo

    def hgrc_append_lines(self, lines):
        with self.path.join('.hg', 'hgrc').open('a') as fp:
            fp.writelines(l + '\n' for l in lines)

    def hg(self, *args, **kwargs):
        """Invoke the `hg` executable and return its stdout.

        This behaves as `subprocess.check_output` does.
        """
        return hg_call(self.path, args, **kwargs)[1]

    def hg_unchecked(self, *args, **kwargs):
        """Invoke the `hg` executable without raising if return code is nonzero.

        :returns: (process return code, stdout, stderr).
        """
        return hg_call(self.path, args, check_return_code=False, **kwargs)

    def assert_hg_failure(self, *args,
                          error_message_expectations='',
                          stdout_expectations='',
                          stderr_expectations='',
                          **kwargs):
        """Invoke the ``hg` executable, expect and assert it to fail

        All ``expectations`` kwargs can be either `str` instances, compiled
        regular expressions or iterables of such. It will be asserted that the
        actual error output matches them.

        :param error_message_expectations: check done on the expected channel
          (stdout or stderr), which can depend on the Mercurial client
          version.
        :param stdout_expectations: check done unconditionally on stdout.
        :param stderr_expectations: check done unconditionally on stderr.
        :returns: (process return code, stdout, stderr).
        """
        code, out, err = self.hg_unchecked(*args, **kwargs)
        # code 1 is hg standard for "no change"
        assert code not in (0, 1)

        err_msg_chan = out if hg_client_version() < (5, 9) else err
        assert_message(err_msg_chan, error_message_expectations)

        assert_message(out, stdout_expectations)
        assert_message(err, stderr_expectations)

        return code, out, err

    def graphlog(self, hidden=False):
        """Return a full log.

        This is useful to print (captured by the runner and displayed if there
        are failures), maybe to send to a file.

        :param hidden: if True, also display hidden (obsolete) changesets.

        """
        cmd = ['log', '--graph', '-T', SHORT_TEMPLATE]
        if hidden:
            cmd.append('--hidden')
        return self.hg(*cmd)

    def changeset_extracts(self, template_exprs,
                           collection=tuple,
                           revs=None,
                           val_sep='|:|', eol="\n"):
        """Extract information from changesets, as a collection of entries.

        This does not represent the graph information, but the ordering given
        by `hg log`, on which this method is based, is preserved if using
        an ordered collection.

        :param template_exprs: an iterable of template keywords or pairs
           (attribute, template expression).

           Examples:
           - ``['rev', 'phase', 'desc']``
           - ``['phase', ('desc', 'desc|firstline')]``

           The second one will return named tuples with ``phase`` and ``desc``
           attributes.
        :param collection: the wished collection class. Must be instantiable
           by a generator expression, like `set` and `tuple` are.
        :return: a named tuple class whose attributes are the elements of
          ``template_exprs`` and a set of instances of that class,
          one for each changeset.

        WARNING: there is no escaping. The command will fail utterly
        if the rendering of one template expression contains ``val_sep`` or
`       ``eol``.
        """
        template_exprs = [
            (expr, expr) if isinstance(expr, str) else tuple(expr)
            for expr in template_exprs
        ]
        template = val_sep.join("{%s}" % expr[1] for expr in template_exprs)
        cmd = ['log', '-T', template + eol]
        if revs is not None:
            cmd.extend(('-r', revs))

        Extract = namedtuple('Extract', (expr[0] for expr in template_exprs))
        return Extract, collection(Extract(*line.split(val_sep))
                                   for line in self.hg(*cmd).split(eol)
                                   if line)

    def branches(self):
        """Return `hg branches` as a set of names."""
        return set(self.hg('branches', '-T', '{branch}\n').splitlines())

    def node(self, revspec):
        """Return the node id for specified revision (can be symbolic)"""
        return self.hg('log', '-T', "{node}", '-r', revspec)

    def init_gitlab_ci(self,
                       message="Init GitLab CI",
                       script=("grep foo foo",),
                       ):
        """Create an commit a .gitlab-ci.yml file.

        A convenience method to have a valid configuration without caring
        too much with what it entails.
        """
        ci_config = dict(job=dict(script=script))
        # JSON is a subset of YaML and part of Python standard library
        self.path.join('.gitlab-ci.yml').write(json.dumps(ci_config))
        self.hg('add', '.gitlab-ci.yml')
        self.hg('commit', '-m', message)

    def count_changesets(self):
        """Return the total number of changesets in repo.

        Obsolete changesets are taken into account.
        """
        # for empty repo, this gives 1 + (-1), hence the expected 0
        return 1 + int(self.hg('log', '-r', 'tip', '-T', '{rev}'))

    def wait_pull_new_changesets(self, number, *flags,
                                 retry_wait_factor=0.1, **kwargs):
        """Pull repeatedly until new changesets are retrieved by pulls.

        If not enough changesets are retrieved, this is an ``AssertionError``.

        :param int number: the minimal number of new changesets to pull
        :param flags: additional arguments to pass to the pull.
           Example::
             repo.wait_pull_changesets(2, '-u')
        :param kwargs: other :func:`wait_assert` keyword arguments.
        :raises: AssertionError if not enough changesets are retrieved before
           timeout.
        """
        # can be -1 (empty repo, and that is still consistent)
        expected = self.count_changesets() + number
        wait_assert(
            lambda: self.hg('pull', *flags),
            lambda _: self.count_changesets() >= expected,
            retry_wait_factor=retry_wait_factor,
            **kwargs,
        )


def assert_matching_changesets(repo1, repo2, fields, ordered=True, revs=None):
    """Assert changesets to have same information in the two given repos

    Of course all structural information of the changesets can be checked
    with just ``node``, but there is also outer information, like for example
    ``phases``, and ``bookmarks``, whose inclusion depends on the test case.

    Also, adding some human-readable information such as `desc` or `topic`
    can make matter more obvious to people engaged in debugging.

    The ordering can be kept or not, according to the test case.
    """
    collection = tuple if ordered else set
    extract1, extract2 = [
        repo.changeset_extracts(fields, collection=collection, revs=revs)[1]
        for repo in (repo1, repo2)
    ]
    assert extract1 == extract2


def cli_pushvars(pushvars):
    """Turn pushvars into CLI arguments

    :params dict pushvars: the wished push variables and their values both
    as strings, except the special case of ``True``, which is meant for
    actions (currently translates as, e.g, ``ci.skip=``, same as an empty
    string, but that can change).

    :return: an iterable of arguments that can simply appended to a
      :meth:`LocalRepo.hg` call.
    """
    cli_args = []
    for k, v in pushvars.items():
        if v is True:
            v = ''
        cli_args.extend(('--pushvars', '='.join((k, v))))
    return cli_args
