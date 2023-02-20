# --------------------------------------------------------------------------
# File: file.py
# Description: File where is located de logic of projects actions.
# Date: 11/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

import os
import pathlib
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QWidget
from proteus.model.archetype_manager import ArchetypeManager
from proteus.model.archetype_proxys import ProjectArchetypeProxy
from proteus.model.project import Project
import proteus.utils.config as config
import proteus.utils.persistence as persistence
from proteus.view.widgets.project_dialog import ProjectDialog
from .base import Controller


class Dialog:
    """
    Dialog class where open/save dialog is located.
    """
    @staticmethod
    def request(parent: QWidget, title: str, mime: str, suffix: str,
                accept_mode, default_file_name="Proteus"):
        
        #We set the name of the window (title)
        dialog = QFileDialog(parent, title)

        #We set the filter for the file dialog
        dialog.setMimeTypeFilters([mime])

        #We set the default name for the file that is going to be saved
        dialog.selectFile(default_file_name)

        #Type of mode (if we are going to save (QFileDialog.AcceptSave) 
        #or open (QFileDialog.AcceptOpen))
        dialog.setAcceptMode(accept_mode)

        #We set the suffix for the file
        dialog.setDefaultSuffix(suffix)

        
        if "SNAP" in os.environ:
            dialog.setOption(QFileDialog.DontUseNativeDialog)

        if dialog.exec() != QFileDialog.Accepted:
            return
        return dialog.selectedFiles()
        


class FileController(Controller):
    """
    File controller
    """

    def __init__(self, *args, **kwargs):
        super(FileController, self).__init__(*args, **kwargs)

    def req_new_project(self):
        dialog = ProjectDialog(self.app)
        dialog.exec()

    def req_open_project(self) -> None:
        """
        Request project path to open.
        """
        selected_files = Dialog.request(
            self.app, "Open file", "application/xml", "xml",
            QFileDialog.AcceptOpen)

        if selected_files:
            filename = selected_files[0]
            config.project_folder = filename
            # This variable is used to specify if the project is new or not
            # So as it's opened, we will set the state of all docs and objects
            # to "CLEAN" instead of "FRESH"
            clean = True
            self.load_project(filename, clean)
            project_title = self.app.projectController.project.get_property("name").value
            self.app.setWindowTitle("Proteus - " + project_title)
    
    def req_save_new_project(self, archetype) -> None:
        """
        Method that request path to save a new project.
        """
        projects = ArchetypeManager.load_project_archetypes()
        archetype_proxy : ProjectArchetypeProxy = projects[archetype]
        selected_files = Dialog.request(
            self.app, "Save file", "application/xml", "xml",
            QFileDialog.AcceptSave, archetype_proxy.path)

        if selected_files:
            # TODO change with the new config file
            path_to_be_saved = pathlib.Path(selected_files[0]).parent
            ArchetypeManager.clone_project(archetype_proxy.path, path_to_be_saved)
            return selected_files

    def req_save_project(self) -> None:
        """
        Request path to save project.
        """

        # If we have a project folder it means the project already exists.
        if(config.project_folder != ""):
            # self.save_project(config.project_folder)
            persistence.save_existing_project(config.project_folder, self.app.projectController.project)
            self.app.ribbon.save_tb.setEnabled(False)
        
        # Otherwise we have to save as new.
        else:
            selected_files = Dialog.request(
                self.app, "Save file", "application/xml", "xml",
                QFileDialog.AcceptSave, self.app.projectController.get_property("name").value)

            if selected_files:
                filename = selected_files[0]
                self.save_project(filename)
                self.app.ribbon.save_tb.setEnabled(False)

    def load_project(self, filename: str, clean=False, project_title=None) -> None:
        if self.app.projectController.project:
            return self.app.__class__(path=filename).show()
        # Load...
        project: Project = Project.load(pathlib.Path(filename).parent)
        print(self.app)
        print(self.app.projectController)
        self.app.projectController.project = project
        self.app.create_dock_windows()

        self.app.projectController.saved_command = self.app.undoStack.index()
        self.app.projectController.selected_document_index = 0

        self.app.ribbon.edit_tb.setEnabled(True)
        self.app.ribbon.create_tb.setEnabled(True)
        self.app.ribbon.delete_tb.setEnabled(True)
        self.app.ribbon.export_tb.setEnabled(True)

        # BUG 'MainWindow' object has no attribute 'visualizers'
        # Try to add it at the top
        # self.app.create_dock_windows()

        #If the file is new and we have a title, we will set it
        if project_title:
            new_prop = project.get_property("name").clone(project_title)
            self.app.projectController.project.set_property(new_prop)

        self.app.statusBar().showMessage(f"Loaded {filename}", 2000)

    def save_project(self, filename: str) -> None:
        self.path = filename
        config.project_folder = filename
        if not self.path and os.listdir(os.path.dirname(filename)):
            confirm = QMessageBox(self)
            confirm.setWindowTitle("Delete folder content?")
            confirm.setText("Target folder is not empty, all files will be deleted.")
            confirm.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            confirm.addButton("Change directory", QMessageBox.ApplyRole)
            todo = confirm.exec()

            if todo == QMessageBox.No:
                return
            elif todo == 0:
                # Change directory
                return self.req_save_project()

        persistence.save_project(filename, self.app.projectController.project)
        # self.path = filename

        self.app.statusBar().showMessage(f"Saved '{filename}'", 2000)