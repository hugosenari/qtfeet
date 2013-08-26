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
    Instantiate, Requires, BindField, UnbindField
import pelix.ipopo.constants as constants

# QtFeet Utils
from ..utils import StdCfgType

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

    0 - cmd 'args' / file suplied by cmd
    1 - current dir config file
    2 - user config (can be a file or a server)
    3 - system config (can be a file or a server)
    4 - Default value
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

    def get_config_values(self, name, default=None):
        """
        Return all configs values for name
        This sistem can have various config provides ie:
        provider for command args
        provider for user configs file
        provider for system config files
        provider for external server config
        etc
        With this we have various values for same config name
        There are no priority of result

        :param name: name of config option
        :param default=None: default value if name not found
        :return: yield with all configs for this name
        """
        if self._configs_svc:
            for cfg_provider in self._configs_svc:
                cfg_value = cfg_provider.get_config(name)
                if cfg_value:
                    yield cfg_provider.get_type(), cfg_value
        yield StdCfgType.DEFAULT, default

    def get_config(self, name, default=None):
        """
        Return a value of config
        """
        return self.get_config_values(name, default).next()[1]

    def set_config(self, name, value, cfg_type=None):
        """
        Sets a value of config
        """
        if self._configs_svc:
            for cfg_provider in self._configs_svc:
                if cfg_provider.writable() and (
                    cfg_type is None or
                    cfg_provider.get_get_type() == cfg_type
                ):
                    try:
                        cfg_provider.set_config(name, value)
                        return None
                    except:
                        pass
                        # something goes wrong :(
                        # try next config provider

    def sort_cfg_svc(self):
        self._configs_svc = sorted(
            self._configs_svc,
            key=lambda cfg_svc: cfg_svc.get_type()
        )

    @BindField('_configs_svc')
    def bind_widget(self, field, service, reference):
        """
        Config service bound
        """
        # we need sort services
        self.sort_cfg_svc()

    @UnbindField('_configs_svc')
    def unbind_widget(self, field, service, reference):
        """
        Config service gone
        """
        # we need sort services
        self.sort_cfg_svc()
