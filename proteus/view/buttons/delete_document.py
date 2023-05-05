# ==========================================================================
# File: delete_document.py
# Description: File where is located the button (QToolButton) of delete a doc.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus import config
from proteus.controllers.utils.i18n import trans
import proteus

class DeleteDocument():
    """
    Class where is located the button (QToolButton) of delete an existent doc.
    """

    def getButton(self) -> QToolButton:
        """
        Method that creates the action (QToolButton) of delete a doc.

        :returns: Action of delete an existent doc.
        :rtype: QToolButton
        """
        proteus.logger.info('DeleteDocument Button - get button')

        self.delete_tb = QToolButton()
        self.delete_tb.setObjectName("Delete Document")
        self.delete_tb.setText(trans("Delete"))
        self.delete_tb.setToolTip(trans("Delete Current Document"))
        self.delete_tb.setEnabled(False)
        self.delete_tb.setIcon(QIcon(f"{config.Config().icons_directory}/delete.svg"))
        # self.delete_tb.setShortcut("Ctrl+D")
        return self.delete_tb
