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
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.utils.model.qundo_commands import CreateDocument
import proteus.utils.persistence as persistence
import proteus

def load_objects(path):
    """
    Method that loads the objects.
    """
    proteus.logger.info('document dialog logic - load objects')
    res = {}
    for obj in [f for f in listdir(path) if isfile(join(path, f))]:
        
        o = ET.parse(join(path, obj))
        o = persistence.xml2dict(o.getroot())
        res[o["id"]] = o
    return res
# TODO DELETE, IS IN CREATEDOCUMENT
# def change_combo_box(app):
#     """
#     This function changes the combo box of the document dialog.
#     And updates the combobox with the new documents.
#     """
#     proteus.logger.info('document dialog logic - change combo box')
#     project = app.projectController.project
#     app.document_combobox.clear()
#     document: Object
#     for document in project.documents.values():
#         name = document.get_property("name").value
#         app.document_combobox.addItem(name, document)
#     app.document_combobox.currentIndexChanged.connect(
#         lambda index: app.projectController.change_document_index(index=index))
#     app.document_combobox.currentIndexChanged.connect(lambda index: app.projectController.change_document(document = app.document_combobox.itemData(index))) 
#     app.document_combobox.setCurrentIndex(len(project.documents) - 1)

class DocumentDialogLogic():
    """
    Class that contains the logic of the document dialog.
    """

    def __init__(self, parent) -> None:
        proteus.logger.info('Init DocumentDialogLogic')
        self.parent = parent
    

    def create_document(self, archetype: str) -> None:
        """
        Clone document archetype and adds to project documents list.

        :param archetype: archetype index.
        """
        proteus.logger.info('DocumentDialogLogic - create document')
        
        documents = ArchetypeManager.load_document_archetypes()

        app = self.parent.parentWidget()
        project: Project  = app.projectController.project
        id: str = str(shortuuid.random(length=12))
        documents[archetype].id = id
        
        document: Object = documents[archetype].get_document(project)
        document.id = id
        #TODO reassign id to children
        
        command = CreateDocument(project, document, app, len(project.documents))
        app.undoStack.push(command)
        # Change combobox
        

    def change_archetype(self, archetype: int) -> None:
        """
        Select archetype to clone.

        :param archetype: archetype index.
        """
        proteus.logger.info('DocumentDialogLogic - change archetype')
        
        document = ArchetypeManager.load_document_archetypes()
        document_description = document[archetype].description
        app = self.parent.parentWidget()
        project: Project  = app.projectController.project
        print(project.documents)
        self.parent.archetype_description.setText(document_description)


