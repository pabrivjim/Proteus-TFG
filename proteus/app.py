# ==========================================================================
# File: app.py
# Description: the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from pathlib import Path

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus
import sys
from proteus.config import Config
from PyQt5.QtWidgets import QApplication
from proteus.view.main_window import MainWindow

# --------------------------------------------------------------------------
# Class: ProteusApplication
# Description: Class for the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

class ProteusApplication:
    def __init__(self):
        """
        It initializes the PROTEUS application.
        """
        self.config : Config = Config()

    def run(self) -> int:
        """
        PROTEUS application main method.
        """
        self.directories()
        status = self.frontend()
        return status

    def directories(self):
        proteus.logger.info(f"Current working directory: {Path.cwd()}")
        proteus.logger.info(f"Home directory: {Path.home()}")
        proteus.logger.info(f"{Path(__file__) = }")

        proteus.logger.info(f"{self.config.resources_directory = }")
        proteus.logger.info(f"{self.config.icons_directory = }")
        proteus.logger.info(f"{self.config.archetypes_directory = }")

    def frontend(self):

        #https://stackoverflow.com/questions/46653337/using-a-local-file-in-html-for-a-pyqt5-webengine
        sys.argv.append("--disable-web-security")
        print(sys.argv)
        app = QApplication(sys.argv)

        main_window = MainWindow()
        main_window.resize(1024, 768)
        main_window.show()
        status = app.exec()
        return status


