# ==========================================================================
# File: document_dialog.py
# Description: File where is located the document dialog.
# Date: 06/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QDialog
from proteus.model.archetype_manager import ArchetypeManager
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
        uic.loadUi(f"{config.RESOURCES_FOLDER}/ui/new.ui", self)
        self.setWindowTitle("New document")

        # Get dict from project file name and DocumentArcheTypeProxy
        archetypes = ArchetypeManager.load_document_archetypes()

        self.document_logic = DocumentDialogLogic(self)
        
        #Here we get the names of the project from the dict keys, and add it to the combobox
        list_keys = list(archetypes.keys())
        self.document_logic.change_archetype(list_keys[0])
        self.archetypes.addItems(list_keys)
        
        # Connect the combobox change index to the change_archetype method
        self.archetypes.currentIndexChanged.connect(
            lambda: self.document_logic.change_archetype(self.archetypes.currentText()))

        # Connect the accept button to the create_document method
        self.buttonBox.accepted.connect(
            lambda: self.document_logic.create_document(self.archetypes.currentText()))