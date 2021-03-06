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
        result = None
        try:
            result = module.__file__
        except AttributeError:
            result = module
        result = os.path.dirname(result)
        result = os.path.join(result, 'ui')
        return result


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
            path = os.path.dirname(module.__file__)
        except AttributeError:
            path = os.path.dirname(module)
        sys.path.append(path)
