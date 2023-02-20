# ==========================================================================
# File: project_dialog_logic.py
# Description: File where is located the document dialog logic.
# Date: 06/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import shortuuid
from os import listdir
from os.path import isfile, join
from lxml import etree as ET
from proteus.model.archetype_manager import ArchetypeManager
from proteus.model.archetype_proxys import DocumentArchetypeProxy
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.utils.model.qundo_commands import CreateDocument
import proteus.utils.config as config 
import proteus.utils.persistence as persistence
import logging

def load_objects(path):
    """
    Method that loads the objects.
    """
    logging.info('document dialog logic - load objects')
    res = {}
    for obj in [f for f in listdir(path) if isfile(join(path, f))]:
        
        o = ET.parse(join(path, obj))
        o = persistence.xml2dict(o.getroot())
        res[o["id"]] = o
    return res

def change_combo_box(app):
    """
    This function changes the combo box of the document dialog.
    And updates the combobox with the new documents.
    """
    logging.info('document dialog logic - change combo box')
    project = app.projectController.project
    app.document_combobox.clear()
    document: Object
    for document in project.documents.values():
        name = document.get_property("name").value
        app.document_combobox.addItem(name)
    app.document_combobox.currentIndexChanged.connect(
        lambda index: app.projectController.change_document(index=index))
    app.document_combobox.setCurrentIndex(len(project.documents) - 1)

class DocumentDialogLogic():
    """
    Class that contains the logic of the document dialog.
    """

    def __init__(self, parent) -> None:
        logging.info('Init DocumentDialogLogic')
        self.parent = parent
    

    def create_document(self, archetype: str) -> None:
        """
        Clone document archetype and adds to project documents list.

        :param archetype: archetype index.
        """
        logging.info('DocumentDialogLogic - create document')
        
        document = ArchetypeManager.load_document_archetypes()

        app = self.parent.parentWidget()
        project: Project  = app.projectController.project
        command = CreateDocument(project, document[archetype].get_document(project), len(project.documents))
        app.undoStack.push(command)
        # Change combobox
        change_combo_box(app)

    def change_archetype(self, archetype: int) -> None:
        """
        Select archetype to clone.

        :param archetype: archetype index.
        """
        logging.info('DocumentDialogLogic - change archetype')
        
        document = ArchetypeManager.load_document_archetypes()
        print(archetype)
        print(document)
        document_description = document[archetype].description
        self.parent.archetype_description.setText(document_description)


