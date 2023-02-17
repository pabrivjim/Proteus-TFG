# ==========================================================================
# File: qundo_commands.py
# Description: File where is located the logic of QUndoCommands and QUndoStack
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QUndoCommand
from proteus.controllers.save_state_machine import SaveMachine
from proteus.controllers.save_state_machine import States
import proteus.utils.persistence as persistence
from proteus.utils.model.nodes_utils import (get_node, get_parent)
from copy import deepcopy
import logging

class CreateObject(QUndoCommand):
    """
    Command to insert an object to a given parent. Adds a previously cloned
    object to the end of parent children list.
    """

    def __init__(self, project: dict, parent_id: str, object: dict):
        logging.info('Init CreateObject')
        super(CreateObject, self).__init__()
        self.object = object
        self.obj = SaveMachine(self.object["id"])

        self.parent = get_node(project, parent_id)
        self.parent_obj = SaveMachine(self.parent["id"])
        self.parent_state = self.parent_obj.get_state()

        self.position = len(self.parent["children"])
        self.project = project

    def redo(self) -> None:
        logging.info('CreateObject - redo')
        """
        Inserts object to parent children list.
        Set object state to FRESH.
        Set parent's object to DIRTY.
        """
        self.obj.set_state(States.FRESH)
        self.parent_obj.set_state(States.DIRTY)
        self.parent["children"].insert(self.position, self.object)

    def undo(self) -> None:
        logging.info('CreateObject - undo')
        """
        Removes object from parent children list.
        Removes object state.
        Set parent's state to previous state.
        """
        self.obj.remove_state()
        self.parent_obj.set_state(self.parent_state)
        self.parent["children"].pop(self.position)


class CreateDocument(QUndoCommand):
    """
    Command to create project documents.
    """

    def __init__(self, project: dict, document: dict, index: int):
        logging.info('Init CreateDocument')
        super(CreateDocument, self).__init__()
        self.document = document
        self.position = index
        self.project = project
        self.doc = SaveMachine(self.document["id"])
        self.objects = persistence.get_project_objects(self.project)

    def redo(self) -> None:
        logging.info('CreateDocument - redo')
        """
        Inserts document to project documents list.
        Set object state to FRESH.
        Set objects's children to FRESH.
        """
        self.doc.set_state(States.FRESH)
        for i in self.objects:
            obj = SaveMachine(i["id"])
            obj.set_state(States.FRESH)
        self.project["documents"].insert(self.position, self.document)

    def undo(self) -> None:
        logging.info('CreateDocument - undo')
        """
        Removes document from project documents list.
        Removes object state.
        Removes object's children states.
        """
        for i in self.objects:
            obj = SaveMachine(i["id"])
            obj.remove_state()
        self.doc.remove_state()
        self.project["documents"].pop(self.position)


class DeleteObject(QUndoCommand):
    """
    Command to delete an object.
    """

    def __init__(self, project: dict, object_id: str, obj: SaveMachine, parent_obj: SaveMachine):
        logging.info('Init DeleteObject')
        super(DeleteObject, self).__init__()
        self.node = get_node(project, object_id)
        self.parent = get_parent(project, object_id)
        self.position = self.parent["children"].index(self.node)
        self.state = obj.get_state()
        self.parent_state = parent_obj.get_state()
        self.obj = obj
        self.parent_obj = parent_obj

    def redo(self):
        logging.info('DeleteObject - redo')
        """
        Removes node from parent children list.
        Set object state to DELETED.
        Set parent's object to DIRTY.
        """
        self.parent["children"].remove(self.node)
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

    def __init__(self, project, document_index):
        logging.info('Init DeleteDocument')
        super(DeleteDocument, self).__init__()
        self.document = project["documents"][document_index]
        self.position = document_index
        self.project = project
        self.old_states = deepcopy(SaveMachine.states)

    def redo(self):
        logging.info('DeleteDocument - redo')
        """
        Deletes document from project documents list.
        Sets all objects in document to DELETED.
        """
        self.project["documents"].pop(self.position)
        SaveMachine.set_document_objects_to_deleted(self.document)

    def undo(self):
        logging.info('DeleteDocument - undo')
        """
        Inserts document to project documents list.
        Sets all objects states to previous states.
        """
        self.project["documents"].insert(self.position, self.document)
        SaveMachine.states = self.old_states


class UpdateNode(QUndoCommand):
    """
    Command to update node attributes.
    """

    def __init__(self, project, object_id, new_attrs, obj: SaveMachine):
        logging.info('Init UpdateNode')
        super(UpdateNode, self).__init__()
        self.node = get_node(project, object_id)
        self.new_attrs = new_attrs
        self.old_attrs = self.node.copy()
        self.state = obj.get_state()
        self.obj = obj

    def redo(self):
        logging.info('UpdateNode - redo')
        """
        Update node dict attributes.
        Set object state to DIRTY.
        """
        self.node.update(self.new_attrs)
        self.obj.set_state(States.DIRTY)

    def undo(self):
        logging.info('UpdateNode - undo')
        """
        Replace node attributes with old attributes.
        Set object state to previous state.
        """
        self.node.update(self.old_attrs)
        self.obj.set_state(self.state)


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
