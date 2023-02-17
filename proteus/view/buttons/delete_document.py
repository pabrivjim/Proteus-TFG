# ==========================================================================
# File: delete_document.py
# Description: File where is located the button (QToolButton) of delete a doc.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus.utils.i18n import trans
from proteus.utils.loader import resource_path
import logging

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
        logging.info('DeleteDocument Button - get button')
        
        self.delete_tb = QToolButton()
        self.delete_tb.setObjectName("Delete Document")
        self.delete_tb.setText(trans("delete"))
        self.delete_tb.setToolTip(trans("delete current document"))
        self.delete_tb.setEnabled(False)
        self.delete_tb.setIcon(QIcon(resource_path("icons/delete.svg")))
        # self.delete_tb.setShortcut("Ctrl+D")
        return self.delete_tb
