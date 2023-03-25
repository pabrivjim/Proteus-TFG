# ==========================================================================
# File: save_project.py
# Description: File where is located the button (QToolButton) of save project.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus.utils.i18n import trans
from proteus.utils.loader import resource_path
import proteus

class SaveProject():
    """
    Class where is located the button (QToolButton) of save project.
    """

    def getButton(self) -> QToolButton:
        """
        Method that creates the action (QToolButton) of save project.
        :returns: Action of save project.
        :rtype: QToolButton
        """
        proteus.logger.info('SaveProject Button - get button')

        self.save_tb = QToolButton()
        self.save_tb.setObjectName("Save Project")
        self.save_tb.setText(trans("save"))
        self.save_tb.setToolTip(trans("save project"))
        self.save_tb.setEnabled(False)
        self.save_tb.setIcon(QIcon(resource_path("icons/save.svg")))
        # self.save_tb.setShortcut("Ctrl+O")
        return self.save_tb
