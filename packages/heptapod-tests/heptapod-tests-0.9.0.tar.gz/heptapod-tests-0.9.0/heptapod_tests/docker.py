# Copyright 2018 Paul Morelle <madprog@htkc.org>
# Copyright 2019-2020 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import absolute_import
import docker
import sys
_client = docker.from_env()


def heptapod_exec(ct, command, user='root'):
    container = _client.containers.get(ct)
    exit_code, output = container.exec_run(command, tty=True, demux=True,
                                           user=user)
    sys.stdout.write('+ docker exec heptapod {command}\n'.format(
        command=command,
    ))
    out, err = [o.decode() if o is not None else None for o in output]
    if out is not None:
        sys.stdout.write(out)
    if err is not None:
        sys.stderr.write(err)

    return exit_code, out


def heptapod_run_shell(ct, command, **kw):
    exit_code, output = heptapod_exec(ct, command, **kw)
    if exit_code:
        raise RuntimeError(
            ('Heptapod command {command} returned a non-zero '
             'exit code {exit_code}').format(command=command,
                                             exit_code=exit_code,
                                             ))


def heptapod_put_archive(ct, dest, path):
    """Put the tar archive at path at given dest in container."""
    container = _client.containers.get(ct)
    with open(path, 'rb') as arf:
        container.put_archive(dest, arf.read())


def heptapod_put_archive_bin(ct, dest, fobj):
    """Put the tar archive of file-like `fobj` at given dest in container."""
    _client.containers.get(ct).put_archive(dest, fobj.read())


def heptapod_get_archive(ct, path, tarf):
    """Get the file or directory at path as a tar archive.

    The tar binary contents is written to the tarf file-like object and
    a stats dict is returned.

    :param tarf: a binary file-like object
    :param archive_path: path to retrieve inside the Heptapod container
    :returns: dict of stats.
    """
    container = _client.containers.get(ct)
    bits, stats = container.get_archive(path)
    for chunk in bits:
        tarf.write(chunk)
    return stats


def host_address(ct):
    """Return a suitable address for the host, as seen from the container.

    For now this is just the IPv4 gateway, assumed to be the host, i.e. where
    these tests run.

    It will probably fail for more complicated network settings, but that's
    good enough for the time being.
    """
    container = _client.containers.get(ct)
    return container.attrs['NetworkSettings']['Gateway']
