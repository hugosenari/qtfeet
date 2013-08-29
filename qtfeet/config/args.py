#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines a Args Configuration component

Options that are passed to command line (args)

"""

# Module version
__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))

# Documentation strings format
__docformat__ = "restructuredtext en"

# -----------------------------------------------------------------------------

# iPOPO
from pelix.ipopo.decorators import ComponentFactory, Provides, Property, \
    Instantiate
import pelix.ipopo.constants as constants

# Standard library
import json
import argparse

# QtFeet Utils
from ..utils import StdCfgType

# -----------------------------------------------------------------------------


@ComponentFactory('args-provider-factory')
@Provides('qtfeet.config.provider')
@Property('_name', constants.IPOPO_INSTANCE_NAME)
@Instantiate('args-provider0')
class ArgsProvider(object):

    """
    The module to provide config information from command line
    """

    def __init__(self):
        """
        Sets up the component
        """
        # Instance name
        self._name = None

        # read configuration from args
        try:
            parser = argparse.ArgumentParser(
                description='QtFeet DBus introspection tool')
            parser.add_argument(
                '-o', metavar='options', type=str,
                default='{}', help='json with options',
                dest='options')
            args = parser.parse_args()
            self._opts = json.loads(args.options)
        except Exception:
            self._opts = {}

    @property
    def name(self):
        """
        Returns the instance name
        """
        return self._name

    @property
    def type(self):
        """
        Return cfg type for sort
        """
        return StdCfgType.ARGS

    @property
    def writable(self):
        """
        Defines if this kind of config can save config
        """
        return False

    def get(self, name):
        """
        Return a value of config

        :param name: of config
        """
        return self._opts.get(name, None)

    def set(self, name, value):
        """
        Sets a value of config
        CMD has no set method

        :param name: of config
        :param value: to config
        """
        raise NotImplementedError()
