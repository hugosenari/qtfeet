#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines a Home Configuration component

"""

# Module version
__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))

# Documentation strings format
__docformat__ = "restructuredtext en"

# -----------------------------------------------------------------------------

# iPOPO
from pelix.ipopo.decorators import ComponentFactory, Provides, Property, \
    Instantiate, Validate, Invalidate
import pelix.ipopo.constants as constants

# Standard library
import json
import os

# QtFeet Utils
from ..utils import StdCfgType

# -----------------------------------------------------------------------------


@ComponentFactory('home-config-provider-factory')
@Provides('modules.config.provider')
@Property('_name', constants.IPOPO_INSTANCE_NAME)
@Instantiate('home-config-provider0')
class PwdConfigProvider(object):

    """
    The module to provide config information from current dir file .qtfeet
    """

    def __init__(self):
        """
        Sets up the component
        """
        # Instance name
        self._name = None

        # read configuration from args
        self._file = None
        self._opts = {}
        self._writable = False

    def get_name(self):
        """
        Returns the instance name
        """
        return self._name

    def get_type(self):
        """
        Return cfg type for sort
        """
        return StdCfgType.HOME

    def writable(self):
        """
        Defines if this kind of config can save config
        """
        return self._writable

    def get_config(self, name):
        """
        Return a value of config
        """
        return self._opts.get(name, None)

    def set_config(self, name, value):
        """
        Sets a value of config
        """
        self._opts[name] = value

    @Validate
    def validate(self, context):
        """
        Component validated
        """
        # we need open file and read configs
        config_file = os.path.join(
            os.path.expanduser('~'), '.qtfeet')
        exist = os.path.exists(config_file) \
            and os.path.isfile(config_file)
        if exist:
            self._file = config_file
            if os.access(config_file, os.R_OK):
                with open(config_file) as cfg_file:
                    self._opts = json.loads(cfg_file.read())
                self._writable = os.access(config_file, os.W_OK)

    @Invalidate
    def invalidate(self, context):
        """
        Component invalidated
        """
        if self._writable:
            with open(self._file, "w") as cfg_file:
                cfg_file.write(
                    json.dumps(self._opts))
        self._file = None
        self._opts = {}
        self._writable = False
