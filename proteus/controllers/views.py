# ==========================================================================
# File: views.py
# Description: Contains the logic related to views and visualizer.
# Date: 
# Version: 1.0.0
# Author: Gamaza
# ==========================================================================

from PyQt5.QtWidgets import QFileDialog

from .base import Controller
from .file import Dialog


class ViewsController(Controller):
    """
    Views controller class where view controller actions are located.
    """

    def print_view(self):
        """
        Prints view.
        """
        selected_files = Dialog.request(
            self.app, "Export current view as pdf", "application/pdf", "pdf",
            QFileDialog.AcceptSave, self.app.projectController.project.get_property("name").value)

        if selected_files:
            filename = selected_files[0]
            # self.app.save_project(filename)
            self.app.centralWidget().currentWidget().save_pdf(filename)

    def export_view(self):
        """
        Exports view.
        """
        selected_files = Dialog.request(
            self.app, "Export current view as html", "application/html", "html",
            QFileDialog.AcceptSave, self.app.projectController.project.get_property("name").value)

        if selected_files:
            filename = selected_files[0]
            # self.save_project(filename)
            self.app.centralWidget().currentWidget().save_html(filename)

    def update_views(self):
        """
        Updates views.
        """
        for visualizer in self.app.visualizers:
            visualizer.update(
                self.app.projectController.project,
                self.app.projectController.selected_document_index)

    def focus_object(self, object_id: str):
        """
        Focuses object in visualizers.

        :param object_id. Id of the object to focus.
        """
        for visualizer in self.app.visualizers:
            visualizer.focus(object_id)
