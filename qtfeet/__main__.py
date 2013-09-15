#!/usr/bin/python
# -- Content-Encoding: UTF-8 --
"""
Pelix/Qt application bootstrap.

Loads Qt in the main thread and starts a Pelix framework in a second one

:author: Thomas Calmant
:copyright: Copyright 2013, isandlaTech
:license: GPLv3
:version: 0.1
:status: Alpha
"""

# Module version
__version_info__ = (0, 1, 0)
__version__ = ".".join(map(str, __version_info__))

# Documentation strings format
__docformat__ = "restructuredtext en"

# ------------------------------------------------------------------------

# Import Pelix
import pelix.framework

# Standard library
import logging

# QtFeet library

from .utils import threaded
from .ui import qt_bridge

# ------------------------------------------------------------------------


def first(framework, qtloader):
    """
    Start QT loop
    """
    # Run the Qt loop (blocking)
    qtloader.loop()

# ------------------------------------------------------------------------


def second(framework, qtloader):
    """
    Start pelix loop (in other thread)
    """
    context = framework.get_bundle_context()
    framework.start()
    # [...] Install bundles, instantiate components [...]
    context.install_bundle('qtfeet.main').start()
    # Wait for the framework to stop
    framework.wait_for_stop()

# ------------------------------------------------------------------------


def stop(framework, qtloader):
    """
    stop everything
    """
    #try stop qtloader
    try:
        qtloader and qtloader.on_stop()
    except:
        pass

    #try stop framework
    try:
        framework and framework.stop()
    except:
        pass

# ------------------------------------------------------------------------


def qtfeet_main():
    logging.basicConfig(level=logging.WARNING)

    # Loads Qt and the framework.
    framework = pelix.framework.create_framework(
        ['pelix.ipopo.core', 'pelix.shell.core', 'pelix.shell.ipopo'])
    context = framework.get_bundle_context()

    # Load Qt
    qtloader = qt_bridge.QtLoader()
    qtloader.setup()

    context.register_service("qtfeet.ui.loader", qtloader, {})

    threaded.OnStopThread(first, second, stop)\
        .run(framework, qtloader)


# Classic...
if __name__ == "__main__":
    qtfeet_main()
