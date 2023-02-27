# ==========================================================================
# File: open_project.py
# Description: File where is located the button (QToolButton) of open project.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus.utils.i18n import trans
from proteus.utils.loader import resource_path
import proteus

class OpenProject():
    """
    Class where is located the button (QToolButton) of open project.
    """

    def getButton(self) -> QToolButton:
        """
        Method that creates the action (QToolButton) of open project.
        :returns: Action of open project.
        :rtype: QToolButton
        """
        proteus.logger.info('OpenProject Button - get button')
        
        self.open_tb = QToolButton()
        self.open_tb.setObjectName("Open Project")
        self.open_tb.setText(trans("open"))
        self.open_tb.setToolTip(trans("open project"))
        self.open_tb.setEnabled(True)
        self.open_tb.setIcon(QIcon(resource_path("icons/folder.svg")))
        # self.open_tb.setShortcut("Ctrl+O")
        return self.open_tb
