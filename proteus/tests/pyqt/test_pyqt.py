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
from proteus.view.main_window import MainWindow
#python -m pytest .\proteus\tests\pyqt\test_pyqt.py
def test_pyqt(qtbot):
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
    assert window.ribbon.open_tb.text() == "Abrir"
    assert window.ribbon.new_tb.text() == "Nuevo"
    assert window.ribbon.save_tb.text() == "Guardar"
    assert window.ribbon.edit_tb.text() == "Editar"

    assert window.ribbon.open_tb.objectName() == "Open Project"
    assert window.ribbon.new_tb.objectName() == "New Project"
    assert window.ribbon.save_tb.objectName() == "Save Project"
    assert window.ribbon.edit_tb.objectName() == "Edit Project"

    assert window.ribbon.open_tb.isEnabled() == True
    assert window.ribbon.new_tb.isEnabled() == True
    assert window.ribbon.save_tb.isEnabled() == False
    assert window.ribbon.edit_tb.isEnabled() == False

def default_ribbon_document_buttons(window: MainWindow):
    assert window.ribbon.create_tb.text() == "Crear"
    assert window.ribbon.delete_tb.text() == "Eliminar"
    assert window.ribbon.export_tb.text() == "Exportar"

    assert window.ribbon.create_tb.objectName() == "Create Document"
    assert window.ribbon.delete_tb.objectName() == "Delete Document"
    assert window.ribbon.export_tb.objectName() == "Export Document"

    assert window.ribbon.create_tb.isEnabled() == False
    assert window.ribbon.delete_tb.isEnabled() == False
    assert window.ribbon.export_tb.isEnabled() == False

def default_ribbon_qundostack_buttons(window: MainWindow):
    assert window.ribbon.undo_tb.text() == "Deshacer"
    assert window.ribbon.redo_tb.text() == "Rehacer"

    assert window.ribbon.undo_tb.isEnabled() == False
    assert window.ribbon.redo_tb.isEnabled() == False

def archetype_objects_buttons(window: MainWindow):
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
    path_to_project = str(pathlib.Path().cwd() / "proteus" / "tests" / "project" / "proteux.xml")
    file_controller = window.file
    file_controller.load_project(path_to_project)
    project_controller = window.projectController
    project_title = project_controller.project.get_property("name").value
    window.setWindowTitle("Proteus - " + project_title)
    assert window.windowTitle() == ("Proteus - " + project_title)
