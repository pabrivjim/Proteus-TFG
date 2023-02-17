# ==========================================================================
# File: project_dialog_logic.py
# Description: File where is located the project dialog logic.
# Date: 06/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from lxml import etree as ET
from proteus.controllers.save_state_machine import SaveMachine
import proteus.utils.config as config 
import logging
import proteus.controllers.file as file

class ProjectDialogLogic():
    """
    Class that contains the logic of the project dialog.
    """
    def __init__(self, parent) -> None:
        logging.info('Init ProjectDialogLogic')
        self.parent = parent
    
    # OLD CODE to create a new prioject (we used this to create a project 
    # from an archetype but it was loaded on memory and not saved)

    # def create_project(self, path: str, archetype) -> None:
    #     """
    #     Open archetype project

    #     :param path: path of project archetype.
    #     """
    #     logging.info('ProjectDialogLogic - create project')
    #     main_class = self.parent.parent().__class__
    #     project_title = self.parent.name.text()
    #     m = main_class(project_path=path, project_title=project_title)
    #     m.setWindowTitle("Proteus - " + project_title)
    #     m.show()

    def create_project(self, path, archetype) -> None:
        """
        Create a new project.
        :param path: path of project archetype.
        """
        logging.info('ProjectDialogLogic - create project')
        selected_files = self.parent.parent().file.req_save_new_project(archetype)
        if selected_files:
            filename = selected_files[0]
            config.project_folder = filename
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
        logging.info('ProjectDialogLogic - change archetype')
        
        project_path = f"{config.ARCHETYPES_FOLDER}/projects/{archetype}/project.xml"
        element = ET.parse(project_path).getroot()

        # Load properties to get name FIXME
        project_properties = {}
        for prop in element.find("properties"):
            name = prop.attrib["name"]
            value = prop.text
            project_properties[name] = {"type": prop.tag, "value": value}

            if "category" in prop.attrib:
                project_properties[name]["category"] = prop.attrib["category"]

            if prop.tag == "enumProperty":
                project_properties[name]["choices"] = prop.attrib.get("choices", "").split()

        project_description = project_properties.get("description", {}).get("value", "")
        self.parent.archetype_description.setText(project_description)
