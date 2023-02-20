# ==========================================================================
# File: dialogs.py
# Description: Dialogs to clone projects and documents.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QDialog
from proteus.utils.model.project_dialog_logic import ProjectDialogLogic
import proteus.utils.config as config
from PyQt5 import uic
import logging

class ProjectDialog(QDialog):
    """
    Dialog to select and clone project archetype.
    """

    def __init__(self, parent):
        logging.info('Init ProjectDialog')
        super().__init__(parent)
        uic.loadUi('proteus/resources/ui/new.ui', self)
        self.project_logic = ProjectDialogLogic(self)
        archetypes = config.Config.load_project_archetypes()
        self.project_logic.change_archetype(archetypes[0])
        self.archetypes.addItems(archetypes)
        self.archetypes.currentIndexChanged.connect(
            lambda: self.project_logic.change_archetype(archetypes[self.archetypes.currentIndex()]))
        archetype_dir = f"{config.ARCHETYPES_FOLDER}/projects/"
        self.buttonBox.accepted.connect(
            lambda: self.project_logic.create_project(archetype_dir + archetypes[self.archetypes.currentIndex()] + "/project.xml", self.archetypes.currentIndex()))
