#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines a Add On Service component

"""

# Module version
__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))

# Documentation strings format
__docformat__ = "restructuredtext en"

# -----------------------------------------------------------------------------

# iPOPO
from pelix.ipopo.decorators import ComponentFactory, Provides, Property, \
    Instantiate, Requires, Validate
import pelix.ipopo.constants as constants

# -----------------------------------------------------------------------------


@ComponentFactory('add-ons-service-factory')
@Requires('_config_svc', 'qtfeet.config.service')
@Requires('_logger_svc', 'qtfeet.log.service', optional=True)
@Provides('qtfeet.addons.service')
@Property('_name', constants.IPOPO_INSTANCE_NAME)
@Instantiate('add_ons-service0')
class AddonsService(object):

    """
    The module start stop add_ons
    Add-Ons are just bundles
    """

    def __init__(self):
        """
        Sets up the component
        """
        self._context = None
        # Instance name
        self._name = None

        # Configuration
        self._config_svc = None
        self._logger_svc = None
        self._addons = {}
        self._bundles = {}

    @Validate
    def _validate(self, context):
        """
        Component validated

        :param context: Bundle context
        """
        self._context = context
        for addon in self.addons:
            if addon['active']:
                self.start_addon(addon)
        # Log info
        self._logger_svc and \
            self._logger_svc.info(self, 'validated')

    @property
    def name(self):
        """
        Returns the instance name
        """
        return self._name

    @property
    def addons(self):
        """
        Returns a list with current addons
        """
        #read addons from config
        addons_from = self._config_svc.values('addons', [])
        for cfg_type, addons in addons_from:
            for addon in addons:
                path = addon['bundle']
                if path not in self._addons:
                    self._addons[path] = self._addons
                    yield addon

    def start_addon(self, addon):
        """
        Start some addon
        """
        path = addon['bundle']
        bundle = self._bundles.get(path, None)
        if not bundle:
            bundle = self._context.install_bundle(path)
            self._bundles[path] = bundle
        bundle.start()

    def stop_addon(self, addon):
        """
        Stop some addon
        """
        path = addon['bundle']
        bundle = self._bundles.get(path, None)
        if bundle:
            bundle.stop()

    def install(self, addon):
        """
        Install an addon

        :param addon: addon information see .qtfeet for example
        """
        self._config_svc.set(addon)

    def uninstall(self, addon):
        """
        Uninstall an addon
        """
        addons_from = self._config_svc.values('addons', [])
        for cfg_type, addons in addons_from:
            if addon in addons:
                addons.remove(addon)
                self._config_svc.set(addons)
