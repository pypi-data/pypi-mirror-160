# Copyright 2022 Georges Racinet <georges.racinet@octobus.net>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 3 or any later version.
#
# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
import yaml


class HeptapodConfig:
    """Read Heptapod-specific configuration from its own file.

    The whole point it to use a different file than pytest, so that it
    can be easily ignored.
    """

    schema = {}  # option name to type, defaults etc.

    def __init__(self, pytest_conf):
        self.pytest_conf = pytest_conf
        self.file_conf = {}

    @classmethod
    def load(cls, pytest_conf):
        hpd_conf = cls(pytest_conf)
        rel_path = pytest_conf.getoption('heptapod_config')
        # as of this writing, pytest's rootdir is a py.path object,
        # does not interpret `/` as expected if rel_path is in fact absolute
        conf_path = Path(pytest_conf.rootdir) / rel_path
        if conf_path.exists():
            with conf_path.open() as conf_fobj:
                hpd_conf.file_conf = yaml.safe_load(conf_fobj)
        return hpd_conf

    def get(self, attr_name):
        sch_entry = self.schema.get(attr_name)
        if sch_entry is None:
            raise KeyError(f"Config item {attr_name} is undefined")

        action = sch_entry.get('action')
        # In case of `store_true` and `store_false`,
        # pytest config will normalize as bool
        # hence won't return ``None`` if not set on the CLI
        if action == 'store_true':
            pytest_notset = False
            action_bool = True
        elif action == 'store_false':
            pytest_notset = True
            action_bool = True
        else:
            pytest_notset = None
            action_bool = False

        pyv = self.pytest_conf.getoption(attr_name)
        if pyv is not pytest_notset:
            return pyv

        fv = self.file_conf.get(attr_name)
        if fv is None:
            return sch_entry.get('default')

        # Not exactly the same as setting validator to `bool`
        # Given the wide range of boolean evaluation, we prefer strict
        # type checking here.
        if action_bool and not isinstance(fv, bool):
            raise ValueError("In configuration file, only boolean values "
                             "are allowed for %r" % attr_name)

        validator = sch_entry.get('type')
        return fv if validator is None else validator(fv)

    @classmethod
    def cli_add_config_path_option(cls, pytest_parser):
        pytest_parser.addoption(
            '--heptapod-config',
            default='heptapod-tests.yml',
            help="Path to the Heptapod Tests YaML configuration file, in "
            "which all the other custoom option of these tests can be set")

    @classmethod
    def add_option(cls, pytest_parser, name, **kwargs):
        if not name.startswith('--'):
            raise ValueError(
                "Configuration options must be defined in CLI"
                "form (--something)")
        pytest_kw = kwargs.copy()
        # we don't want argparse to apply defaults before we pass over
        # to the configuration file.
        pytest_kw.pop('default', None)
        pytest_parser.addoption(name, **pytest_kw)

        attr_name = name[2:].replace('-', '_')
        cls.schema[attr_name] = kwargs.copy()
