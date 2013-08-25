#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines a Cmd Configuration component

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

# -----------------------------------------------------------------------------


@ComponentFactory('cmd-config-provider-factory')
@Provides('modules.config.provider')
@Property('_name', constants.IPOPO_INSTANCE_NAME)
@Instantiate('cmd-config-provider0')
class CmdConfigProvider(object):

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

    def get_name(self):
        """
        Returns the instance name
        """
        return self._name

    def get_config(self, name, default=None):
        """
        Return a value of config
        """
        default = self._opts.get(name, default)
        return default

    def set_config(self, name, value):
        """
        Sets a value of config
        CMD has no set method
        """
        pass
