# ==========================================================================
# File: document_dialog_logic.py
# Description: File where is located the document dialog logic.
# Date: 06/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import shortuuid
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.utils.widgets_logic.qundo_commands import CreateDocument
import proteus

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

        documents = self.parent.document_archetypes

        app = self.parent.parentWidget()
        project: Project  = app.projectController.project
        id: str = str(shortuuid.random(length=12))
        documents[archetype].id = id
        
        document: Object = documents[archetype].get_document(project)
        document.id = id

        #TODO reassign id to children
        command = CreateDocument(project, document, app, len(project.documents))
        app.undoStack.push(command)
        

    def change_archetype(self, archetype: int) -> None:
        """
        Select archetype to clone.

        :param archetype: archetype index.
        """
        proteus.logger.info('DocumentDialogLogic - change archetype')
        
        document = self.parent.document_archetypes
        document_description = document[archetype].description
        self.parent.archetype_description.setText(document_description)


