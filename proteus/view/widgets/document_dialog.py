# ==========================================================================
# File: document_dialog.py
# Description: File where is located the document dialog.
# Date: 06/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QDialog
from proteus.utils.model.document_dialog_logic import DocumentDialogLogic
import proteus.utils.config as config
from PyQt5 import uic
import logging

class DocumentDialog(QDialog):
    """
    Dialog to select and clone document archetype.
    """

    def __init__(self, parent):
        logging.info('Init DocumentDialog')
        super().__init__(parent)
        uic.loadUi('proteus/resources/ui/new.ui', self)
        self.setWindowTitle("New document")
        archetypes = config.Config.load_document_archetypes()

        self.document_logic = DocumentDialogLogic(self)

        self.document_logic.change_archetype(archetypes[0])
        self.archetypes.addItems(archetypes)
        self.archetypes.currentIndexChanged.connect(
            lambda: self.document_logic.change_archetype(archetypes[self.archetypes.currentIndex()]))

        self.buttonBox.accepted.connect(
            lambda: self.document_logic.create_document(archetypes[self.archetypes.currentIndex()]))


