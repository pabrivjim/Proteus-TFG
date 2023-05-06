# ==========================================================================
# File: document_dialog_logic.py
# Description: File where is located the document dialog logic.
# Date: 06/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import shortuuid
from proteus.model.abstract_object import ProteusState
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.controllers.utils.widgets_logic.qundo_commands import CreateDocument
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
        for doc in documents.values():
            print(doc.path)

        app = self.parent.parentWidget()
        project: Project  = app.projectController.project
        id: str = str(shortuuid.random(length=12))
        documents[archetype].id = id
        
        document: Object = documents[archetype].get_document(project)
        document.id = id
        def _set_to_fresh(parent: Object):
            for child in parent.children.values():
                child.state = ProteusState.FRESH
                if(child.children):
                    _set_to_fresh(child)
        _set_to_fresh(document)


        # Update document name
        if(self.parent.name.text().strip() != ""):
            new_prop = document.get_property("name").clone(self.parent.name.text())
            document.set_property(new_prop)

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
