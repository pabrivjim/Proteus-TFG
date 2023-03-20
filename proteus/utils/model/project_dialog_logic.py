# ==========================================================================
# File: project_dialog_logic.py
# Description: File where is located the project dialog logic.
# Date: 06/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from lxml import etree as ET
import proteus.config as config
import proteus
from proteus.model.archetype_manager import ArchetypeManager

class ProjectDialogLogic():
    """
    Class that contains the logic of the project dialog.
    """
    def __init__(self, parent) -> None:
        proteus.logger.info('Init ProjectDialogLogic')
        self.parent = parent

    def create_project(self, path, archetype) -> None:
        """
        Create a new project.
        :param path: path of project archetype.
        """
        proteus.logger.info('ProjectDialogLogic - create project')
        selected_files = self.parent.parent().file.req_save_new_project(archetype)
        if selected_files:
            filename = selected_files[0]
            main_class = self.parent.parent().__class__
            project_title = self.parent.name.text()
            m = main_class(project_path=path, project_title=project_title, clean=True)
            m.setWindowTitle("Proteus - " + project_title)
            m.show()

    def change_archetype(self, archetype: int) -> None:
        """
        Select archetype to clone.

        :param archetype: archetype index.
        """
        proteus.logger.info('ProjectDialogLogic - change archetype')
        project_description = ArchetypeManager.load_project_archetypes()[archetype].description
        self.parent.archetype_description.setText(project_description)
