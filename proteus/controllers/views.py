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
import proteus
from os import listdir
from os.path import join, isfile
import proteus.config as config

def load_views() -> list:
    """
    Method that loads the views.
    """
    proteus.logger.info('Config - load views')
    views_dir = join(config.Config().resources_directory, "views")
    views = [f for f in listdir(views_dir) if not isfile(join(views_dir, f))]
    res = []
    for view in views:
        try:
            if (config.Config().xslt_custom_file != None):
                proteus.logger.error(f'Config - load views - custom')
                file = config.Config().xslt_custom_file
                res.append({"type": "xslt", "path": file})
            else:
                proteus.logger.error(f'Config - load views - default')
                res.append({"type": "xslt", "path": join(views_dir, view, "main.xslt")})
        except Exception as e:
            proteus.logger.error(f'Config - load views - error: {e}')
            res.append({"type": "xslt", "path": join(views_dir, view, "main.xslt")})
    return res

def get_views_folder() -> str:
    """
    Method that returns the views folder.
    """
    proteus.logger.info('Config - get views folder')
    return join(config.Config().resources_directory, "views")


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
            QFileDialog.AcceptSave, self.app.document_combobox.currentText())

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
            QFileDialog.AcceptSave, self.app.document_combobox.currentText())

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
        Focuses object in visualizers. This method is called from the tree view.
        It is used to scroll to the object in the visualizer.

        :param object_id: Id of the object to focus.
        """
        for visualizer in self.app.visualizers:
            visualizer.focus(object_id)
