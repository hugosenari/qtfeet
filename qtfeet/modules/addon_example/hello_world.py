# -- Content-Encoding: UTF-8 --

"""
Defines Hello World Component Addon

You can look at iPOPO and Pelix documentation for help
http://ipopo.coderxpress.net/tutorials/index.html
http://ipopo.coderxpress.net/api/

Basically how this work:
You define a class, you decorate with ComponentFactory and Instantiate
iPOPO create intance to you
You define requirement services to your class
When this services are usable, iPOPO will set an attr with service instance
When all required service are OK, iPOPO call method that has @Validate

Service examples:
- Logger
- Configuration
- Main Window (main_frame)
- toolbar
- status bar
- other addon
- etc  # TODO: Link documentation of all services avaiable


Tip:

iPOPO can read any bundle (addon) that are in Python Path
Create an simple packages with your addons,
Add them to config and have a fun.
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


# This is complex case to express examples
# The only necessary is ComponentFactory and Instantiate
# All othes (Required, Property and Provides) are optional
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
@Instantiate(__addon_name__ + '_instance')  # autostart this
class HelloWorld(object):

    """
    The hello world component

    All methods aren't required
    But you need @validated to know that your dependencies are satisfied
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
    @BindField('_logger_svc')
    def bindLogger(self, field, service, reference):
        """
        Logger service bound
        :param field: field name '_logger_svc' in this case
        :param service: field value LoggerService in this case
        :param reference: iPOPO.ServiceReference
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
    # also called before system stop this addon
    @Invalidate
    def invalidate(self, context):
        """
        Component invalidated
        """
        if self._logger_svc:
            self._logger_svc.info(self, 'Im invalid')
