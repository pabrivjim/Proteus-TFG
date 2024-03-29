# ==========================================================================
# File: export_document.py
# Description: File where is located the button (QToolButton) to export a doc.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus import config
from proteus.controllers.utils.i18n import trans
import proteus

class ExportDocument():
    """
    Class where is located the button (QToolButton) of export a doc.
    """

    def getButton(self) -> QToolButton:
        """
        Method that creates the action (QToolButton) of export a doc.

        :returns: Action of export a doc.
        :rtype: QToolButton
        """
        proteus.logger.info('CreateDocument Button - get button')

        self.export_tb = QToolButton()
        self.export_tb.setObjectName("Export Document")
        self.export_tb.setText(trans("Export"))
        self.export_tb.setToolTip(trans("Export Current Document"))
        self.export_tb.setEnabled(False)
        self.export_tb.setIcon(QIcon(f"{config.Config().icons_directory}/export.png"))
        # self.open_tb.setShortcut("Ctrl+N")
        return self.export_tb
