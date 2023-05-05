# ==========================================================================
# File: create_document.py
# Description: File where is located the button (QToolButton) of create a doc.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus import config
from proteus.controllers.utils.i18n import trans
import proteus

class CreateDocument():
    """
    Class where is located the button (QToolButton) of create a new doc.
    """

    def getButton(self) -> QToolButton:
        """
        Method that creates the action (QToolButton) of create a new doc.

        :returns: Action of create a new doc.
        :rtype: QToolButton
        """
        proteus.logger.info('CreateDocument Button - get button')

        self.create_tb = QToolButton()
        self.create_tb.setObjectName("Create Document")
        self.create_tb.setText(trans("Create"))
        self.create_tb.setToolTip(trans("New Document from Archetype"))
        self.create_tb.setEnabled(False)
        self.create_tb.setIcon(QIcon(f"{config.Config().icons_directory}/add.png"))
        # self.open_tb.setShortcut("Ctrl+N")
        return self.create_tb
