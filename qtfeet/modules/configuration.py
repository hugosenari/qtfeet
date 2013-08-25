#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines a Configuration component

"""

# Module version
__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))

# Documentation strings format
__docformat__ = "restructuredtext en"

# -----------------------------------------------------------------------------

# iPOPO
from pelix.ipopo.decorators import ComponentFactory, Provides, Property, \
    Instantiate, Requires
import pelix.ipopo.constants as constants

# -----------------------------------------------------------------------------


@ComponentFactory('config-service-factory')
@Requires('_configs_svc', 'modules.config.provider',
          aggregate=True)
@Provides('modules.config.service')
@Property('_name', constants.IPOPO_INSTANCE_NAME)
@Instantiate('config-service0')
class ConfigService(object):

    """
    The module to config
    """

    def __init__(self):
        """
        Sets up the component
        """
        # Instance name
        self._name = None

        # Config
        self._configs_svc = None

    def get_name(self):
        """
        Returns the instance name
        """
        return self._name

    def get_config(self, name, default=None):
        """
        Return a value of config
        """
        if self._configs_svc:
            for cfg_provider in self._configs_svc:
                cfg_value = cfg_provider.get_config(name, default)
                if cfg_value != default:
                    return cfg_value
        return default

    def set_config(self, name, value):
        """
        Sets a value of config
        """
        if self._configs_svc:
            for cfg_provider in self._configs_svc:
                cfg_provider.set_config(name, value)
