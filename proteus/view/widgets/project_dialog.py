# ==========================================================================
# File: dialogs.py
# Description: Dialogs to clone projects and documents.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QDialog
from proteus.utils.i18n import trans
from proteus.utils.widgets_logic.project_dialog_logic import ProjectDialogLogic
import proteus.config as config
from PyQt5 import uic
import proteus

class ProjectDialog(QDialog):
    """
    Dialog to select and clone project archetype.
    """

    def __init__(self, parent):
        proteus.logger.info('Init ProjectDialog')
        super().__init__(parent)
        uic.loadUi('proteus/resources/ui/new.ui', self)

        # Here we get the text like ("Name", "Description", etc) and translate them
        self.setWindowTitle(trans(self.windowTitle()))
        self.description_label.setText(trans(self.description_label.text()))
        self.name_label.setText(trans(self.name_label.text()))
        self.project_label.setText(trans(self.project_label.text()))

        self.project_archetypes = parent.archetype_controller.get_project_archetypes()
        self.project_logic = ProjectDialogLogic(self)
        archetypes_list = list(self.project_archetypes.keys())
        self.project_logic.change_archetype(archetypes_list[0])
        self.archetypes.addItems(archetypes_list)
        self.archetypes.currentIndexChanged.connect(
            lambda: self.project_logic.change_archetype(archetypes_list[self.archetypes.currentIndex()]))
        archetype_dir = f"{config.Config().archetypes_directory}/projects/"
        self.buttonBox.accepted.connect(
            lambda: self.project_logic.create_project(archetype_dir + archetypes_list[self.archetypes.currentIndex()] + "/project.xml", self.archetypes.currentText()))

