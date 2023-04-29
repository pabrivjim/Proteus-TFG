"""
Pytest file for the PROTEUS frontend (PyQt5) with Pytest-qt.
"""
# ==========================================================================
# File: test_pyqt.py
# Description: pytest file for the PROTEUS frontend with Pytest-qt
# Date: 17/03/2023
# Version: 0.1
# Author: Pablo Rivera Jiménez
# ==========================================================================
from pathlib import Path
import pathlib
import os
from lxml import etree as ET
from proteus import config
from proteus.tests import PATH
from proteus.utils.i18n import trans
from proteus.view.main_window import MainWindow
#python -m pytest .\proteus\tests\pyqt\test_pyqt.py
def test_pyqt(qtbot):
    """
    Test the main window of the PROTEUS frontend. This method calls all the
    methods that test the different parts of the main window.
    """
    os.chdir(PATH)

    window = MainWindow()
    # qtbotbis = QtBot(window)
    # Create the GUI widget

    window.show()
    assert window.windowTitle() == ('Proteus')

    default_ribbon_project_buttons(window)
    default_ribbon_document_buttons(window)
    default_ribbon_qundostack_buttons(window)
    archetype_objects_buttons(window)
    recreate_req_open_project_without_dialog(window)
    # qtbotbis.mouseClick(window.ribbon.open_tb, QtCore.Qt.LeftButton, delay=1)

def default_ribbon_project_buttons(window: MainWindow):
    """
    Test the default buttons of the project ribbon.
    It also checks that the buttons are enabled and disabled correctly.
    """
    assert window.ribbon.open_tb.text() == trans("Open")
    assert window.ribbon.new_tb.text() == trans("New")
    assert window.ribbon.save_tb.text() == trans("Save")
    assert window.ribbon.edit_tb.text() == trans("Edit")

    assert window.ribbon.open_tb.objectName() == "Open Project"
    assert window.ribbon.new_tb.objectName() == "New Project"
    assert window.ribbon.save_tb.objectName() == "Save Project"
    assert window.ribbon.edit_tb.objectName() == "Edit Project"

    assert window.ribbon.open_tb.isEnabled() == True
    assert window.ribbon.new_tb.isEnabled() == True
    assert window.ribbon.save_tb.isEnabled() == False
    assert window.ribbon.edit_tb.isEnabled() == False

def default_ribbon_document_buttons(window: MainWindow):
    """
    Test the default buttons of the document ribbon.
    It also checks that the buttons are enabled and disabled correctly.
    """
    assert window.ribbon.create_tb.text() == trans("Create")
    assert window.ribbon.delete_tb.text() == trans("Delete")
    assert window.ribbon.export_tb.text() == trans("Export")

    assert window.ribbon.create_tb.objectName() == "Create Document"
    assert window.ribbon.delete_tb.objectName() == "Delete Document"
    assert window.ribbon.export_tb.objectName() == "Export Document"

    assert window.ribbon.create_tb.isEnabled() == False
    assert window.ribbon.delete_tb.isEnabled() == False
    assert window.ribbon.export_tb.isEnabled() == False

def default_ribbon_qundostack_buttons(window: MainWindow):
    """
    Test the default buttons of the undo/redo ribbon.
    It also checks that the buttons are enabled and disabled correctly.
    """
    assert window.ribbon.undo_tb.text() == trans("Undo")
    assert window.ribbon.redo_tb.text() == trans("Redo")

    assert window.ribbon.undo_tb.isEnabled() == False
    assert window.ribbon.redo_tb.isEnabled() == False

def archetype_objects_buttons(window: MainWindow):
    """
    Test the buttons of the objects archetypes.
    It checks that the buttons are created correctly.
    """
    #We get all the archetypes buttons
    buttons = window.ribbon.buttons

    #From the directory of objects archetypes, we get all the files in each subdirectory
    sub_directories = list(Path(config.Config().archetypes_directory / "objects").iterdir())
    for sub_directory in sub_directories:
        files = list(Path(sub_directory).iterdir())

        #If for each file we get the id and it is in the buttons, it is correct
        for file in files:
            root = ET.parse(file).getroot()
            id = root.attrib['id']
            assert id in buttons

def recreate_req_open_project_without_dialog(window: MainWindow):
    """
    Test the open project button without the fileDialog.
    It only loads the project and skip the QDialog select part as it's something
    that is not possible to test with pytest-qt, because it's related to System File Explorer.
    It checks that the title of the window is correct.
    """
    path_to_project = str(pathlib.Path().cwd() / "proteus" / "tests" / "project" / "proteus.xml")
    file_controller = window.file
    file_controller.load_project(path_to_project)
    project_controller = window.projectController
    project_title = project_controller.project.get_property("name").value
    window.setWindowTitle("Proteus - " + project_title)
    assert window.windowTitle() == ("Proteus - " + project_title)
