# ==========================================================================
# File: document_dialog.py
# Description: File where is located the document dialog.
# Date: 06/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QDialog
from proteus.controllers.utils.i18n import trans
from proteus.controllers.utils.widgets_logic.document_dialog_logic import DocumentDialogLogic
import proteus.config as config
from PyQt5 import uic
import proteus

class DocumentDialog(QDialog):
    """
    Dialog to select and clone document archetype.
    """

    def __init__(self, parent):
        proteus.logger.info('Init DocumentDialog')
        super().__init__(parent)
        uic.loadUi(f"{config.Config().resources_directory}/ui/new.ui", self)

        # Here we get the text like ("Name", "Description", etc) and translate them
        self.setWindowTitle(trans(self.windowTitle()))
        self.description_label.setText(trans(self.description_label.text()))
        self.name_label.setText(trans(self.name_label.text()))
        self.project_label.setText(trans(self.project_label.text()))

        self.setWindowTitle(trans("New document"))

        # Get dict from project file name and DocumentArcheTypeProxy
        self.document_archetypes = parent.archetype_controller.get_document_archetypes()

        self.document_logic = DocumentDialogLogic(self)
        
        #Here we get the names of the project from the dict keys, and add it to the combobox
        list_keys = list(self.document_archetypes.keys())
        self.document_logic.change_archetype(list_keys[0])
        self.archetypes.addItems(list_keys)
        
        # Connect the combobox change index to the change_archetype method
        self.archetypes.currentIndexChanged.connect(
            lambda: self.document_logic.change_archetype(self.archetypes.currentText()))

        # Connect the accept button to the create_document method
        self.buttonBox.accepted.connect(
            lambda: self.document_logic.create_document(self.archetypes.currentText()))
