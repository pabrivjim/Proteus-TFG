# ==========================================================================
# File: project.py
# Description: Contains the logic related to project data.
# Date:
# Version: 1.0.0
# Author: Gamaza
#         Pablo Rivera Jiménez
# ==========================================================================

from proteus.model.object import Object
from proteus.model.project import Project
from proteus.view.widgets.export_dialog import ExportDialog
from proteus.utils.widgets_logic.qundo_commands import DeleteDocument
from proteus.view.widgets.document_dialog import DocumentDialog
from proteus.view.widgets.properties import PropertyDialog
from .base import Controller


class ProjectController(Controller):
    """
    Project controller class where the calls to the logic
    of the project and documents actions are located.
    """
    def __init__(self, *args, **kwargs):
        super(ProjectController, self).__init__(*args, **kwargs)
        self.project: Project = None
        self.saved_command = None
        self.selected_object = None
        self.selected_document: Object = None
        self.selected_document_index: int = 0

    def update_document(self) -> None:
        """
        Updates document.
        """
        self.app.views.update_views()
        self.app.document_tree.load_document()
        can_save = self.saved_command != self.app.undoStack.index()
        self.app.ribbon.save_tb.setEnabled(can_save)


    #TODO FIXME it works but the index is not the proper one. We also should search for the id and not the index
    def change_document_index(self, index=0) -> None:
        """
        Changes document.
        """
        self.selected_document_index = index
        self.app.document_tree.load_document()
        self.app.views.update_views()

    def change_document(self, document) -> None:
        """
        Changes document.
        """
        print("Change document")
        self.selected_document = document

    def remove_document(self) -> None:
        """
        Removes document.
        """
        if self.project.documents:
            command = DeleteDocument(self.project, self.project.documents[self.selected_document.id],
                                     self.app.document_combobox, self.selected_document_index)
            self.app.undoStack.push(command)


    def create_document(self) -> None:
        """
        Creates document
        """
        dialog = DocumentDialog(self.app)
        dialog.exec()

    def edit_project(self):
        """
        edit_project
        """
        dialog = PropertyDialog(self.app, self.project)
        dialog.exec()

    def export_project(self):
        dialog = ExportDialog(self.app)
        dialog.exec()
    