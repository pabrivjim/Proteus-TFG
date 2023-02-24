# ==========================================================================
# File: qundo_commands.py
# Description: File where is located the logic of QUndoCommands and QUndoStack
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QUndoCommand
from proteus.controllers.save_state_machine import SaveMachine
import shortuuid
import lxml.etree as ET
from PyQt5.QtWidgets import QComboBox
from proteus.controllers.save_state_machine import States
from proteus.model.abstract_object import ProteusState
from proteus.model.object import Object
from proteus.model.project import Project
import proteus.utils.persistence as persistence
from proteus.utils.model.nodes_utils import (get_node, get_parent)
from copy import deepcopy
import logging

class CreateObject(QUndoCommand):
    """
    Command to insert an object to a given parent. Adds a previously cloned
    object to the end of parent children list.
    """

    def __init__(self, project: Project, parent: Object, obj: Object):
        logging.info('Init CreateObject')
        super(CreateObject, self).__init__()
        self.obj = obj
        self.parent = parent
        self.parent_state: ProteusState = deepcopy(parent.state)
        self.project = project
        self.project_state: ProteusState = deepcopy(project.state)

    def redo(self) -> None:
        logging.info('CreateObject - redo')
        """
        Inserts object to parent children list.
        Set object state to FRESH.
        Set parent's object to DIRTY.
        """
        self.obj.state = ProteusState.FRESH
        self.parent_state = ProteusState.DIRTY
        self.project.state = ProteusState.DIRTY
        self.parent.children[self.obj.id] = self.obj

    def undo(self) -> None:
        logging.info('CreateObject - undo')
        """
        Removes object from parent children list.
        Removes object state.
        Set parent's state to previous state.
        """
        self.obj.state = ProteusState.DEAD
        self.parent.state = self.parent_state
        self.parent.children.pop(self.obj.id)
        self.project_state = self.project.state


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
        app.document_combobox.addItem(name, document)
    app.document_combobox.currentIndexChanged.connect(
        lambda index: app.projectController.change_document_index(index=index))
    app.document_combobox.currentIndexChanged.connect(lambda index: app.projectController.change_document(document = app.document_combobox.itemData(index))) 
    app.document_combobox.setCurrentIndex(len(project.documents) - 1)



class CreateDocument(QUndoCommand):
    """ 
    Command to create project documents.
    """

    def __init__(self, project: Project, document: Object, app, index: int):
        logging.info('Init CreateDocument')
        super(CreateDocument, self).__init__()
        self.document = document
        self.app = app
        self.combo_box: QComboBox = app.document_combobox
        self.position = index
        self.project: Project = project

    def redo(self) -> None:
        logging.info('CreateDocument - redo')
        """
        Inserts document to project documents list.
        Set object state to FRESH.
        Set objects's children to FRESH.
        """
        self.document.state = ProteusState.FRESH
        self.project.documents[self.document.id] = self.document
        change_combo_box(self.app)

    def undo(self) -> None:
        logging.info('CreateDocument - undo')
        """
        Removes document from project documents list.
        Removes object state.
        Removes object's children states.
        """
        #FIXME SET TO DEAD
        self.document.state = ProteusState.DEAD
        self.project.documents.pop(self.document.id)
        self.combo_box.removeItem(self.position)



class DeleteObject(QUndoCommand):
    """
    Command to delete an object.
    """

    def __init__(self, project: Project, object_id: str, obj_state: ProteusState, parent_state: ProteusState):
        logging.info('Init DeleteObject')
        super(DeleteObject, self).__init__()
        self.project = project
        self.object = self.project.documents[object_id]
        self.object_state = obj_state
        self.parent_state = parent_state

    def redo(self):
        logging.info('DeleteObject - redo')
        """
        Removes node from parent children list.
        Set object state to DELETED.
        Set parent's object to DIRTY.
        """
        self.parent.children.remove(self.node)
        self.obj.set_state(States.DELETED)
        self.parent_obj.set_state(States.DIRTY)

    def undo(self):
        logging.info('DeleteObject - undo')
        """
        Inserts node to parent children list.
        Set object state to previous state.
        Set parent's state to previous state.
        """
        self.parent["children"].insert(self.position, self.node)
        self.obj.set_state(self.state)
        self.parent_obj.set_state(self.parent_state)


class DeleteDocument(QUndoCommand):
    """
    Command to delete document from project.
    """

    def __init__(self, project: Project, document: Object, combo_box: QComboBox, combo_box_index: int):
        logging.info('Init DeleteDocument')
        super(DeleteDocument, self).__init__()
        self.document: Object = document
        self.project: Project = project
        self.combo_box: QComboBox = combo_box
        self.combo_box_index: int = combo_box_index
        self.old_document_state = deepcopy(document.state)

    def redo(self):
        logging.info('DeleteDocument - redo')
        """
        Deletes document from project documents list.
        Sets all objects in document to DELETED.
        """
        self.project.documents.pop(self.document.id)
        self.document.state = ProteusState.DEAD
        self.combo_box.removeItem(self.combo_box_index)

    def undo(self):
        logging.info('DeleteDocument - undo')
        """
        Inserts document to project documents list.
        Sets all objects states to previous states.
        """
        self.document.state= self.old_document_state
        self.project.documents[self.document.id] = self.document
        self.combo_box.addItem(self.document.get_property("name").value, self.document)
        


class UpdateNode(QUndoCommand):
    """
    Command to update node attributes.
    """

    def __init__(self, project:Project, new_project:Project):
        logging.info('Init UpdateNode')
        super(UpdateNode, self).__init__()
        self.project = project
        self.back_up_project = deepcopy(project)
        self.new_project = new_project
        self.project_state = project.state

    def redo(self):
        logging.info('UpdateNode - redo')
        """
        Update node dict attributes.
        Set object state to DIRTY.
        """
        project_xml = (ET.tostring(self.project.generate_xml(),
                    xml_declaration=True,
                    encoding='utf-8',
                    pretty_print=True).decode())

        new_project_xml = (ET.tostring(self.new_project.generate_xml(),
                        xml_declaration=True,
                        encoding='utf-8',
                        pretty_print=True).decode())
        if(project_xml != new_project_xml):
            self.project.state = ProteusState.DIRTY
            print(self.new_project.properties)
            self.project.properties = self.new_project.properties

    def undo(self):
        logging.info('UpdateNode - undo')
        """
        Replace node attributes with old attributes.
        Set object state to previous state.
        """
        self.project = self.back_up_project


class MoveNode(QUndoCommand):
    """
    Command to move node in project tree.
    """

    def __init__(self, project, object_id, from_parent, from_row, to_parent,
                 to_row):
        logging.info('Init MoveNode')
        super(MoveNode, self).__init__()
        self.obj = get_node(project, object_id)
        self.from_parent = get_node(project, from_parent)
        self.to_parent = get_node(project, to_parent)
        self.from_row = from_row
        self.to_row = to_row

    def redo(self):
        logging.info('MoveNode - redo')
        """
        Removes node from old position and insert in the new one.
        """
        self.from_parent["children"].remove(self.obj)
        self.to_parent["children"].insert(self.to_row, self.obj)

    def undo(self):
        logging.info('MoveNode - undo')
        """
        Removes node from new position and insert back in old position.
        """
        self.to_parent["children"].remove(self.obj)
        self.from_parent["children"].insert(self.from_row, self.obj)
