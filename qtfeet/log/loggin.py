#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines a Logging component

Use python logging to log information
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


@ComponentFactory('logging-provider-factory')
@Requires('_config_svc', 'qtfeet.config.service')
@Provides('qtfeet.log.provider')
@Property('_name', constants.IPOPO_INSTANCE_NAME)
@Instantiate('logging-provider0')
class LoggingProvider(object):

    """
    The module to logging provider
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
        level = self._config_svc.get(
            'loglevel', 'WARNING')
        self.level = self._parse_level(level) or self.level
        logging.basicConfig(level=self.level)

    def _parse_level(level, default=logging.WARNING):
        """
        Convert string into loglevel

        :param level: string name
        :param default: level if unknow
        """
        level = str(level).upper()
        return getattr(logging, level, default)

    @property
    def name(self):
        """
        Returns the instance name
        """
        return self._name

    def _log(self, level, sender, message):
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
        self._log(logging.DEBUG, sender, message)

    def error(self, sender, message):
        """
        Logs a error message
        sender: instance of object that send this log
        message: log message
        """
        self._log(logging.ERROR, sender, message)

    def info(self, sender, message):
        """
        Logs a info message
        sender: instance of object that send this log
        message: log message
        """
        self._log(logging.INFO, sender, message)

    def warning(self, sender, message):
        """
        Logs a warning message
        sender: instance of object that send this log
        message: log message
        """
        self._log(logging.WARNING, sender, message)
