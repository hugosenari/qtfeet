#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines a Logging Service component

Join all logging to expose to others
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


@ComponentFactory('log-service-factory')
@Provides('qtfeet.log.service')
@Requires('_loggers', 'qtfeet.log.provider', aggregate=True, optional=True)
@Property('_name', constants.IPOPO_INSTANCE_NAME)
@Instantiate('log-service0')
class LogService(object):

    """
    The module to log service
    """

    def __init__(self):
        """
        Sets up the component
        """
        self._name = None
        self._loggers = []

    @property
    def name(self):
        """
        Returns the instance name
        """
        return self._name

    def debug(self, sender, message):
        """
        Logs a message
        level: message priority
        sender: instance of object that send this log
        message: log message
        """
        for logger in self._loggers:
            logger.debug(sender, message)

    def error(self, sender, message):
        """
        Logs a error message
        sender: instance of object that send this log
        message: log message
        """
        for logger in self._loggers:
            logger.error(sender, message)

    def info(self, sender, message):
        """
        Logs a info message
        sender: instance of object that send this log
        message: log message
        """
        for logger in self._loggers:
            logger.info(sender, message)

    def warning(self, sender, message):
        """
        Logs a warning message
        sender: instance of object that send this log
        message: log message
        """
        for logger in self._loggers:
            logger.warning(sender, message)
