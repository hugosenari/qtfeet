#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines a Logging component

"""

# Module version
__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))

# Documentation strings format
__docformat__ = "restructuredtext en"

# -----------------------------------------------------------------------------

# iPOPO
from pelix.ipopo.decorators import ComponentFactory, Provides, Property, \
    Instantiate, Requires, BindField
import pelix.ipopo.constants as constants

# Standard library
import logging

# -----------------------------------------------------------------------------


@ComponentFactory('logging-service-factory')
@Requires('_config_svc', 'modules.config.service')
@Provides('modules.logger.service')
@Property('_name', constants.IPOPO_INSTANCE_NAME)
@Instantiate('logger-service0')
class LoggerService(object):

    """
    The module to logger
    """

    def __init__(self):
        """
        Sets up the component
        """
        # Instance name
        self._name = None

        # Configuration
        self._config_svc = None
        self.level = logging.WARNING

    @BindField('_config_svc')
    def bind_config(self, field, service, reference):
        """
        Config service bound
        """
        level = self._config_svc.get_config(
            'loglevel', 'WARNING')
        self.level = self.parse_level(level) or self.level
        logging.basicConfig(level=self.level)

    def get_name(self):
        """
        Returns the instance name
        """
        return self._name

    def log(self, level, sender, message):
        """
        Logs a message
        level: message priority
        sender: instance of object that send this log
        message: log message
        """
        try:
            logger = logging.getLogger(str(sender))
            logger.setLevel(self.level)
            logger.log(level, message)
        except Exception as e:
            logger.error(e)

    def debug(self, sender, message):
        """
        Logs a message
        level: message priority
        sender: instance of object that send this log
        message: log message
        """
        self.log(logging.DEBUG, sender, message)

    def error(self, sender, message):
        """
        Logs a error message
        sender: instance of object that send this log
        message: log message
        """
        self.log(logging.ERROR, sender, message)

    def info(self, sender, message):
        """
        Logs a info message
        sender: instance of object that send this log
        message: log message
        """
        self.log(logging.INFO, sender, message)

    def warning(self, sender, message):
        """
        Logs a warning message
        sender: instance of object that send this log
        message: log message
        """
        self.log(logging.WARNING, sender, message)

    def parse_level(level, default=logging.WARNING):
        level = str(level).upper()
        return getattr(logging, level, default)
