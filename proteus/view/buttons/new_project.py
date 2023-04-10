# ==========================================================================
# File: new_project.py
# Description: File where is located the button (QToolButton) of create a project.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus.utils.i18n import trans
from proteus.utils.loader import resource_path
import proteus

class NewProject():
    """
    Class where is located the button (QToolButton) of create a new project.
    """

    def getButton(self) -> QToolButton:
        """
        Method that creates the action (QToolButton) of create a new project.
        
        :returns: Action of create a new project.
        :rtype: QToolButton
        """
        proteus.logger.info('NewProject Button - get button')

        self.new_tb = QToolButton()
        self.new_tb.setObjectName("New Project")
        self.new_tb.setText(trans("new"))
        self.new_tb.setToolTip(trans("new project"))
        self.new_tb.setEnabled(True)
        self.new_tb.setIcon(QIcon(resource_path("icons/file.svg")))
        # self.new_tb.setShortcut("Ctrl+N")
        return self.new_tb
