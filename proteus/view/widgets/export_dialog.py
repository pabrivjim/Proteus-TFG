# ==========================================================================
# File: export_dialog.py
# Description: Dialogs to export projects.
# Date: 06/08/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QDialog
from PyQt5 import uic
import proteus

class ExportDialog(QDialog):
    """
    Dialog to select and clone project archetype.   
    """

    def __init__(self, parent):
        proteus.logger.info('Init ProjectDialog')
        super().__init__(parent)
        uic.loadUi('proteus/resources/ui/export.ui', self)
        self.types.addItems(["PDF", "HTML"])
        self.buttonBox.accepted.connect(
            lambda: parent.views.print_view() if self.types.currentIndex() == 0 else self.parent().views.export_view())

