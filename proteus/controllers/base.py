# ==========================================================================
# File: base.py
# Description: The base controller class.
# Date: 
# Version: 1.0.0
# Author: Gamaza
# ==========================================================================

class Controller:
    """
    Base controller class.
    """

    def __init__(self, app):
        """
        Constructor

        :param app: Reference to app instance.
        """
        self.app = app
