#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines a Configuration Service component

Join all configuration to expose to others
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
@Requires('_configs_svc', 'qtfeet.config.provider',
          aggregate=True)
@Provides('qtfeet.config.service')
@Property('_name', constants.IPOPO_INSTANCE_NAME)
@Instantiate('config-service0')
class ConfigService(object):

    """
    The module to config

    0 - cmd 'args' / file suplied by cmd
    1 - current dir config file
    2 - user config (can be a file or a server)
    3 - system config (can be a file or a server)  # TODO
    -1 - Default value (will be the last)
    """

    def __init__(self):
        """
        Sets up the component
        """
        # Instance name
        self._name = None

        # Config
        self._configs_svc = None

    @property
    def name(self):
        """
        Returns the instance name
        """
        return self._name

    def values(self, name, default=None):
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
            for provider in self._configs_svc:
                value = provider.get(name)
                if not value is None:
                    yield provider.type, value
        yield StdCfgType.DEFAULT, default

    def get(self, name, default=None):
        """
        Return a value of config
        """
        configs = self.values(name, default)
        cfg_type, value = configs.next()
        return value

    def set(self, name, value=None, where=StdCfgType.DEFAULT):
        """
        Save configuration

        :param name: of config
        :param value: to set
        :param where: to try set this value (default is first possible)
        """
        if self._configs_svc:
            for service in self._configs_svc:
                if where is service.type or where is -1:
                    if service.writable:
                        service.set(name, value)
                        break

    def _sort(self):
        """
        Sort my services
        """
        self._configs_svc = sorted(
            self._configs_svc,
            key=lambda cfg_svc: cfg_svc.type
        )

    @BindField('_configs_svc')
    def _bind_service(self, field, service, reference):
        """
        Config service bound

        :param field: field name '_configs_svc' in this case
        :param service: field value (bundle providing modules.config.provider)
        :param reference: iPOPO.ServiceReference
        """
        # we need sort services
        self._sort()

    @UnbindField('_configs_svc')
    def _unbind_service(self, field, service, reference):
        """
        Config service gone

        :param field: field name '_configs_svc' in this case
        :param service: field value (bundle providing modules.config.provider)
        :param reference: iPOPO.ServiceReference
        """
        # we need sort services
        self._sort()
