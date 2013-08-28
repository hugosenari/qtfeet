# -- Content-Encoding: UTF-8 --

"""
Defines Hello World Component Addon

You can look at iPOPO and Pelix documentation for help
http://ipopo.coderxpress.net/tutorials/index.html
"""

# Module infor
__addon_name__ = "HelloWorld"
__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))

# Documentation strings format
__docformat__ = "restructuredtext en"

# -----------------------------------------------------------------------------

# iPOPO
from pelix.ipopo.decorators import ComponentFactory, Requires, Provides, \
    Validate, Invalidate, BindField, UnbindField, Instantiate, Property

# ------------------------------------------------------------------------


@ComponentFactory(__addon_name__ + 'Factory')  # define the name of factory
@Requires('_logger_svc',
          'modules.logger.service')  # define dependency
@Requires('_config_svc',
          'modules.config.service',  # define option dependency
          optional=True)
@Requires('_widgets_svc', 'qt.widget',  # same as other but:
          aggregate=True,  # this will be an list with 0 or more services
          optional=True,  # this is option, set false to require at least 1
          spec_filter="(placement=main)")  # filter services that has property
@Property('_name', 'name', 'HelloWorld')  # example of property
@Provides('addon.' + __addon_name__)  # name to use as Requires in other addon
@Instantiate(__addon_name__)  # autostart this
class HelloWorld(object):

    """
    The hello world component
    """

    def __init__(self):
        """
        Sets up the component
        """
        # system will set this values to us
        # because of @Requires("_logger_svc" ...
        self._logger_svc = None
        # same as other but:
        # this is optionally setted
        self._config_svc = None
        self._widgets_svc = []

    # callback called when self._config_svc is defined
    @BindField('_config_svc')
    def bindConfig(self, field, service, reference):
        """
        Config service bound
        """
        #now we can use
        self._config_svc

    # callback called when self._config_svc is defined
    @BindField('_logger_svc')
    def bindLogger(self, field, service, reference):
        """
        Logger service bound
        """
        #now we can use
        self._logger_svc.info(self, 'log bind')

    # callback called when self._logger_svc is undefined
    @UnbindField('_logger_svc')
    def unbindLogger(self, field, service, reference):
        """
        Logger service unbind
        """
        # No service at self._logger_svc
        self._logger_svc

    # called when all required (not optional) services bind is done
    @Validate
    def validate(self, context):
        """
        Component validated
        """
        # now you can use required services
        self._logger_svc.info(self, 'Im valid')

    # called when some required (not optional) service umbind
    # also called before system stop this
    @Invalidate
    def invalidate(self, context):
        """
        Component invalidated
        """
        self._logger_svc.info is None
