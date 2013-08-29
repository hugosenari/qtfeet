#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Defines the Qt main frame

:author: Thomas Calmant
:copyright: Copyright 2013, isandlaTech
:license: GPLv3
:version: 0.1
:status: Alpha
"""

# -----------------------------------------------------------------------------

# PyQt5
import PyQt5.uic as uic
import PyQt5.QtWidgets as QtWidgets


class _QtMainFrame(QtWidgets.QMainWindow):

    """
    Represents the UI, loaded from a UI file
    """

    def __init__(self, controller, ui_file):
        """
        Sets up the frame
        """
        # Parent constructor
        QtWidgets.QMainWindow.__init__(self)

        # Store the controller
        self.__controller = controller

        # Load the frame UI
        uic.loadUi(ui_file, self)

        # Connect to signals
        self.action_quit.triggered.connect(controller.quit)
        self.action_about.triggered.connect(self.__about)
        self.action_about_qt.triggered.connect(self.__about_qt)

    def __about(self):
        """
        About signal handler
        """
        QtWidgets.QMessageBox.about(self, "About QtFeet", """
        <a href="https://github.com/hugosenari/qtfeet">QtFeet</a>
        Is a DBus introspection tool, clone of DFeet.
        """)

    def __about_qt(self):
        """
        About Qt signal handler
        """
        QtWidgets.QMessageBox.aboutQt(self)
