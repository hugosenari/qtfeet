# -- Content-Encoding: UTF-8 --

"""
Defines QtFeet Main Component

"""

# Module infor
__bundle_name__ = "QtFeetMain"
__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))

# Documentation strings format
__docformat__ = "restructuredtext en"

# -----------------------------------------------------------------------------

# iPOPO
from pelix.ipopo.decorators import ComponentFactory, \
    Validate, Invalidate, Instantiate, Provides

# ------------------------------------------------------------------------


@ComponentFactory(__bundle_name__ + 'Factory')
@Provides('qtfeet.addon.' + __bundle_name__)
@Instantiate(__bundle_name__ + '_instance')
class HelloWorldAddon(object):

    """
    The QtFeet Main Component
    """

    def __init__(self):
        pass

    # called when all required (not optional) services bind is done
    @Validate
    def _validate(self, context):
        """
        Component validated

        :param context: iPOPO context
        """
        context.install_bundle('qtfeet.config.pwd_dot_qtfeet').start()
        context.install_bundle('qtfeet.config.home_dot_qtfeet').start()
        context.install_bundle('qtfeet.config.service').start()
        # Start logging services
        context.install_bundle('qtfeet.log.loggin').start()
        context.install_bundle('qtfeet.log.service').start()
        # Start UI service
        context.install_bundle('qtfeet.ui.main_frame').start()
        # Start configured add-ons
        context.install_bundle('qtfeet.addons.service').start()

    @Invalidate
    def _invalidate(self, context):
        """
        Component invalidated

        :param context: iPOPO context
        """
