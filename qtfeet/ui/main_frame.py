#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines the Qt main frame component

:author: Thomas Calmant
:copyright: Copyright 2013, isandlaTech
:license: GPLv3
:version: 0.1
:status: Alpha
"""

# Module version
__version_widget__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_widget__))

# Documentation strings format
__docformat__ = "restructuredtext en"

# -----------------------------------------------------------------------------

# iPOPO
from pelix.ipopo.decorators import ComponentFactory, Requires, Provides, \
    Validate, Invalidate, BindField, UnbindField, Instantiate

# Standard library
import os

# QTFeet library
from .. import utils
from ._qt_main_frame import _QtMainFrame

# ------------------------------------------------------------------------


@ComponentFactory('MainFrameFactory')
@Requires('_qt_loader', 'qtfeet.ui.loader')
@Requires('_logger_svc', 'qtfeet.log.service')
@Requires('_config_svc', 'qtfeet.config.service', optional=True)
@Requires('_widgets_svc', 'qtfeet.ui.widget', aggregate=True, optional=True,
          spec_filter="(placement=main)")
@Provides('qtfeet.ui.mainframe')
@Instantiate("MainFrame")
class MainFrame(object):

    """
    The main frame component
    """

    def __init__(self):
        """
        Sets up the component
        """
        # Bundle context
        self._context = None

        # Valid state flag
        self.__validated = False

        # Main frame
        self._frame = None

        # Qt Loader service
        self._qt_loader = None

        # Frameworks
        self._widgets_svc = None

        # Logger service
        self._logger_svc = None

        # Config service
        self._config_svc = None

        # Tabs
        self._widgets_tabs = {}

    def __make_ui(self):
        """
        Sets up the frame. Must be called from the UI thread
        """
        # Load the UI file
        ui_path = os.path.join(utils.UI.get_ui_dir(__file__), "main.ui")
        self._frame = _QtMainFrame(self, ui_path)

        # Show the frame
        self._frame.show()

    def __clear_ui(self):
        """
        Clears the UI. Must be called from the UI thread
        """
        # Close the window
        self._frame.hide()
        self._frame = None

    @property
    def frame(self):
        """
        Retrieves the main frame object
        """
        return self._frame

    def quit(self):
        """
        Stops the framework
        """
        self._context.get_bundle(0).stop()

    def __add_tab(self, widget_qt):
        """
        Adds a tab

        To run in the UI thread.
        """
        # Prepare the content
        name = widget_qt.get_name()
        widget = widget_qt.get_widget(self._frame)

        # Add the tab
        tab_bar = self._frame.tab_bar
        tab_bar.addTab(widget, name)

        # Store its widget
        self._widgets_tabs[name] = widget

    def __remove_tab(self, widget_qt):
        """
        Removes a tab

        To run in the UI thread.
        """
        # Get component name
        name = widget_qt.get_name()

        # Pop its widget
        widget = self._widgets_tabs.pop(name)

        # Remove the tab
        tab_bar = self._frame.tab_bar
        index = tab_bar.indexOf(widget)
        if index > -1:
            # Found it
            tab_bar.removeTab(index)

        # Clean the component
        widget_qt.clean(self._frame)

    @BindField('_widgets_svc')
    def _bind_widget(self, field, service, reference):
        """
        Widget service bound
        """
        if self.__validated:
            self._qt_loader.run_on_ui(self.__add_tab, service)

        self._logger_svc.info and \
            self._logger_svc.info(self, '_widgets_svc binded')

    @UnbindField('_widgets_svc')
    def _unbind_widget(self, field, service, reference):
        """
        Widget service gone
        """
        if self.__validated:
            self._qt_loader.run_on_ui(self.__remove_tab, service)

        self._logger_svc.info and \
            self._logger_svc.info(self, '_widgets_svc unbinded')

    @Validate
    def _validate(self, context):
        """
        Component validated

        :param context: Bundle context
        """
        self._context = context
        self._qt_loader.run_on_ui(self.__make_ui)

        # Make tabs for already known widgets
        if self._widgets_svc:
            for service in self._widgets_svc:
                self._qt_loader.run_on_ui(self.__add_tab, service)

        # Flag to allow un/bind probes to work
        self.__validated = True

        # Log info
        self._logger_svc.info and \
            self._logger_svc.info(self, 'validated')

    @Invalidate
    def _invalidate(self, context):
        """
        Component invalidated

        :param context: Bundle context
        """

        # De-activate binding call backs
        self.__validated = False

        # Removes tabs
        if self._widgets_svc:
            for service in self._widgets_svc:
                self._qt_loader.run_on_ui(self.__remove_tab, service)

        # Clear the UI
        self._qt_loader.run_on_ui(self.__clear_ui)

        self._context = None

        # Log info
        self._logger_svc and \
            self._logger_svc.info(self, 'invalidated')
