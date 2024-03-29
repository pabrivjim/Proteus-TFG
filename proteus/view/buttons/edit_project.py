# ==========================================================================
# File: edit_project.py
# Description: File where is located the button (QToolButton) of edit project.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus import config
from proteus.controllers.utils.i18n import trans
import proteus

class EditProject():
    """
    Class where is located the button (QToolButton) of edit project.
    """

    def getButton(self) -> QToolButton:
        """
        Method that creates the action (QToolButton) of edit project.

        :returns: Action of edit project.
        :rtype: QToolButton
        """
        proteus.logger.info('EditProject Button - get button')

        self.edit_tb = QToolButton()
        self.edit_tb.setObjectName("Edit Project")
        self.edit_tb.setText(trans("Edit"))
        self.edit_tb.setToolTip(trans("Edit Project Properties"))
        self.edit_tb.setEnabled(False)
        self.edit_tb.setIcon(QIcon(f"{config.Config().icons_directory}/edit.png"))
        # self.edit_tb.setShortcut("Ctrl+O")
        return self.edit_tb
