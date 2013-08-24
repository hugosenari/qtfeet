# -*- coding: utf-8 -*-
import os
import sys


class UI(object):

    """
    Utility class for UI
    """

    @staticmethod
    def get_ui_dir(module):
        """
        Return the default ui path from some module
        module.__path__/ui
        """
        path = None
        try:
            path = module.__path__
        except AttributeError:
            path = os.path.dirname(module.__file__)
        return os.path.join(path, 'ui')


class Path(object):

    """
    Utility class sys.path adm
    """

    @staticmethod
    def add_module_dir_to_path(module):
        """
        Include module dir into path
        """
        path = None
        try:
            path = os.path.join(module.__path__)
        except AttributeError:
            path = os.path.dirname(module.__file__)
        if path:
            sys.path.append(path)
