# ==========================================================================
# File: export_dialog.py
# Description: Dialogs to export projects.
# Date: 06/08/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import proteus.config as config
import proteus
from proteus.controllers.utils.i18n import trans

class ExportDialog(QDialog):
    """
    Dialog to select and clone project archetype.
    """
    def __init__(self, parent):
        proteus.logger.info('Init ExportDialog')
        super().__init__(parent)
        uic.loadUi(f"{config.Config().resources_directory}/ui/export.ui", self)
        self.setWindowTitle(trans("Export"))
        self.label.setText(trans(self.label.text()))
        self.types.addItems(["PDF", "HTML"])
        self.buttonBox.accepted.connect(
            lambda: parent.views.print_view() if self.types.currentIndex() == 0 else self.parent().views.export_view())

