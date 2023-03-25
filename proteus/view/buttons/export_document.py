# ==========================================================================
# File: export_document.py
# Description: File where is located the button (QToolButton) to export a doc.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus.utils.i18n import trans
from proteus.utils.loader import resource_path
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
        self.export_tb.setText(trans("export"))
        self.export_tb.setToolTip(trans("export current document"))
        self.export_tb.setEnabled(False)
        self.export_tb.setIcon(QIcon(resource_path("icons/export.png")))
        # self.open_tb.setShortcut("Ctrl+N")
        return self.export_tb
