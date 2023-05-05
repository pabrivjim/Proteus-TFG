# ==========================================================================
# File: qundo_commands.py
# Description: File where is located the logic of QUndoCommands and QUndoStack
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QUndoCommand
import lxml.etree as ET
from PyQt5.QtWidgets import QComboBox
from proteus.model import PROTEUS_ANY
from proteus.model.abstract_object import ProteusState
from proteus.model.object import Object
from proteus.model.project import Project
from copy import deepcopy
import proteus

class CreateObject(QUndoCommand):
    """
    Command to insert an object to a given parent. Adds a previously cloned
    object to the end of parent children list.
    """

    def __init__(self, project: Project, parent_obj: Object, obj: Object):
        proteus.logger.info('Init CreateObject')
        super(CreateObject, self).__init__()
        self.obj = obj
        self.parent_obj = parent_obj
        self.parent_obj_state: ProteusState = deepcopy(parent_obj.state)
        self.project = project
        self.project_state: ProteusState = deepcopy(project.state)

    def redo(self) -> None:
        """
        Inserts object to parent children list.
        Set object state to FRESH.
        Set parent's object to DIRTY.
        """
        proteus.logger.info('CreateObject - redo')
        self.obj.state = ProteusState.FRESH
        self.obj.parent = self.parent_obj
        if(self.obj.parent.state != ProteusState.FRESH):
            self.parent_obj.state = ProteusState.DIRTY
        self.project.state = ProteusState.DIRTY
        self.parent_obj.children[self.obj.id] = self.obj
        updated_doc = {self.parent_obj.id: self.parent_obj}
        if(isinstance(self.parent_obj.parent, Project)):
            dict.update(self.parent_obj.parent.documents, updated_doc)
        else:
            dict.update(self.parent_obj.parent.children, updated_doc)

    def undo(self) -> None:
        """
        Removes object from parent children list.
        Removes object state.
        Set parent's state to previous state.
        """
        proteus.logger.info('CreateObject - undo')
        if(self.obj.parent.state != ProteusState.FRESH):
            self.obj.state = ProteusState.DEAD
        else:
            self.parent_obj.children.pop(self.obj.id)
        self.parent_obj.state = self.parent_obj_state
        self.project_state = self.project.state
        updated_doc = {self.parent_obj.id: self.parent_obj}
        #FIXME
        if(isinstance(self.parent_obj.parent, Project)):
            dict.update(self.parent_obj.parent.documents, updated_doc)
        else:
            dict.update(self.parent_obj.parent.children, updated_doc)

def change_combo_box(app, index = None):
    """
    This function changes the combo box of the document dialog.
    And updates the combobox with the new documents.
    """
    proteus.logger.info('document dialog logic - change combo box')
    project = app.projectController.project
    app.document_combobox.clear()
    document: Object
    for document in project.documents.values():
        name = document.get_property("name").value
        app.document_combobox.addItem(name, document)
    app.document_combobox.currentIndexChanged.connect(
        lambda index: app.projectController.change_document_index(index=index))
    app.document_combobox.currentIndexChanged.connect(lambda index: app.projectController.change_document(document = app.document_combobox.itemData(index)))
    if (index is None):
        app.document_combobox.setCurrentIndex(len(project.documents) - 1)
    else:
        app.document_combobox.setCurrentIndex(index)


class CreateDocument(QUndoCommand):
    """
    Command to create project documents.
    """
    def __init__(self, project: Project, document: Object, app, index: int):
        proteus.logger.info('Init CreateDocument')
        super(CreateDocument, self).__init__()
        self.document = document
        self.app = app
        self.combo_box: QComboBox = app.document_combobox
        self.position = index
        self.project: Project = project
        self.project_state: ProteusState = deepcopy(project.state)

    def redo(self) -> None:
        """
        Inserts document to project documents list.
        Set object state to FRESH.
        Set objects's children to FRESH.
        """
        proteus.logger.info('CreateDocument - redo')
        self.document.state = ProteusState.FRESH
        self.project.state = ProteusState.DIRTY
        self.project.documents[self.document.id] = self.document
        self.document.parent = self.project
        change_combo_box(self.app)

    def undo(self) -> None:
        """
        Removes document from project documents list.
        Removes object state.
        Removes object's children states.
        """
        proteus.logger.info('CreateDocument - undo')
        #FIXME SET TO DEAD
        if(self.document.state != ProteusState.FRESH):
            self.document.state = ProteusState.DEAD
        else:
            self.project.documents.pop(self.document.id)
        self.project.state = self.project_state
        self.combo_box.removeItem(self.position)

class DeleteObject(QUndoCommand):
    """
    Command to delete an object.
    """

    def __init__(self, project: Project, parent: Object, child_obj: Object):
        proteus.logger.info('Init DeleteObject')
        super(DeleteObject, self).__init__()
        self.project = project
        self.parent: Object = parent
        self.obj = child_obj
        self.old_obj = deepcopy(child_obj)
        self.parent_state = deepcopy(parent.state)
        self.obj_state = deepcopy(child_obj.state)
        self.project_state = deepcopy(project.state)

    def redo(self):
        """
        Removes node from parent children list.
        Set object state to DELETED.
        Set parent's object to DIRTY.
        """
        proteus.logger.info('DeleteObject - redo')
        if(self.obj.state == ProteusState.FRESH):
            self.parent.children.pop(self.obj.id)
        else:
            self.obj.state = ProteusState.DEAD
        self.parent.state = ProteusState.DIRTY
        self.project.state = ProteusState.DIRTY

    def undo(self):
        """
        Inserts node to parent children list.
        Set object state to previous state.
        Set parent's state to previous state.
        """
        proteus.logger.info('DeleteObject - undo')
        self.obj = self.old_obj
        # In case it's a section with objects in side ant this section could have other sectiosn etc,
        # we need to set all of them to dirty so it will be saved again.
        def set_all_to_dirty(parent):
            for child in parent.children.values():
                if(child.state == ProteusState.CLEAN):
                    child.state = ProteusState.DIRTY
                if(child.children):
                    set_all_to_dirty(child)
        if(self.obj.children):
            set_all_to_dirty(self.obj)

        # THIS IS NEEDED BECAUSE WITHOUT, IF THE USER DELETE A ITEM, SAVE AND UNDO THE ITEM WILL BE CLEAN AND WON'T BE SAVED.
        # DOING THIS, THE ITEM WILL BE DIRTY AND WILL BE SAVED.
        if(self.obj_state == ProteusState.CLEAN):
            self.obj.state = ProteusState.DIRTY
        else:
            self.obj.state = self.obj_state
        self.parent.state = self.parent_state
        self.project.state = self.project_state
        self.parent.children[self.obj.id] = self.obj


class DeleteDocument(QUndoCommand):
    """
    Command to delete document from project.
    """

    def __init__(self, project: Project, document: Object, app, combo_box_index: int):
        proteus.logger.info('Init DeleteDocument')
        super(DeleteDocument, self).__init__()
        self.document: Object = document
        self.project: Project = project
        self.app = app
        self.combo_box: QComboBox = app.document_combobox
        self.combo_box_index: int = combo_box_index
        self.old_document = deepcopy(document)
        self.old_document_state = deepcopy(document.state)
        self.old_project_state = deepcopy(project.state)

    def redo(self):
        """
        Deletes document from project documents list.
        Sets all objects in document to DELETED.
        """
        proteus.logger.info('DeleteDocument - redo')
        if(self.document.state == ProteusState.FRESH):
            self.project.documents.pop(self.document.id)
        else:
            self.document.state = ProteusState.DEAD
        self.project.state = ProteusState.DIRTY
        self.combo_box.removeItem(self.combo_box_index)
        # change_combo_box(self.app, 0)

    def undo(self):
        """
        Inserts document to project documents list.
        Sets all objects states to previous states.
        """
        proteus.logger.info('DeleteDocument - undo')
        self.document = self.old_document
        if(self.old_document_state == ProteusState.CLEAN):
            self.document.state = ProteusState.DIRTY
        else:
            self.document.state= self.old_document_state
        
        # This is necessary because in case we delete the document, and the child is clean,
        # when we undo, the child will be clean and won't be saved.
        def set_all_to_dirty(parent):
            for child in parent.children.values():
                if(child.state == ProteusState.CLEAN):
                    child.state = ProteusState.DIRTY
                if(child.children):
                    set_all_to_dirty(child)
        set_all_to_dirty(self.document)
        
        if(self.old_project_state == ProteusState.CLEAN):
            self.project.state = ProteusState.DIRTY
        else:
            self.project.state = self.old_project_state
        self.project.documents[self.document.id] = self.document
        self.combo_box.addItem(self.document.get_property("name").value, self.document)

class UpdateObject(QUndoCommand):
    """
    Command to update node attributes.
    """

    def __init__(self, project: Project, obj:Object, new_obj:Object, app):
        proteus.logger.info('Init UpdateObject')
        super(UpdateObject, self).__init__()
        self.app = app
        self.obj = obj
        self.project = project
        self.project_state = deepcopy(project.state)
        self.back_up_obj_properties = deepcopy(obj.properties)
        self.new_obj = new_obj
        self.obj_state = obj.state

    def redo(self):
        """
        Update node dict attributes.
        Set object state to DIRTY.
        """
        proteus.logger.info('UpdateObject - redo')
        obj_xml = (ET.tostring(self.obj.generate_xml(),
                    xml_declaration=True,
                    encoding='utf-8',
                    pretty_print=True).decode())

        new_obj_xml = (ET.tostring(self.new_obj.generate_xml(),
                        xml_declaration=True,
                        encoding='utf-8',
                        pretty_print=True).decode())

        if(obj_xml != new_obj_xml):
            if(self.obj.state != ProteusState.FRESH):
                self.obj.state = ProteusState.DIRTY
            self.project.state = ProteusState.DIRTY
            self.obj.properties = self.new_obj.properties
        if(isinstance(self.new_obj.parent, Project)):
            change_combo_box(self.app, self.app.document_combobox.currentIndex())
    def undo(self):
        """
        Replace node attributes with old attributes.
        Set object state to previous state.
        """
        proteus.logger.info('UpdateObject - undo')
        self.obj.state = self.obj_state
        self.project.state = self.project_state
        self.obj.properties = self.back_up_obj_properties
        if(isinstance(self.new_obj.parent, Project)):
            change_combo_box(self.app, self.app.document_combobox.currentIndex())



class UpdateProject(QUndoCommand):
    """
    Command to update node attributes.
    """

    def __init__(self, project:Project, new_project:Project, app):
        proteus.logger.info('Init UpdateProject')
        super(UpdateProject, self).__init__()
        self.app = app
        self.project = project
        self.back_up_project_properties = deepcopy(project.properties)
        self.new_project = new_project
        self.project_state = project.state

    def redo(self):
        """
        Update node dict attributes.
        Set object state to DIRTY.
        """
        proteus.logger.info('UpdateProject - redo')
        project_xml = (ET.tostring(self.project.generate_xml(),
                    xml_declaration=True,
                    encoding='utf-8',
                    pretty_print=True).decode())

        new_project_xml = (ET.tostring(self.new_project.generate_xml(),
                        xml_declaration=True,
                        encoding='utf-8',
                        pretty_print=True).decode())

        # If the project name is updated, then the window title is changed
        if(self.project.get_property("name").value != self.new_project.get_property("name").value):
            self.app.setWindowTitle("Proteus - " + self.new_project.get_property("name").value)

        if(project_xml != new_project_xml):
            self.project.state = ProteusState.DIRTY
            self.project.properties = self.new_project.properties

    # If the project name is updated, then the window title is changed
    def undo(self):
        """
        Replace node attributes with old attributes.
        Set object state to previous state.
        """
        proteus.logger.info('UpdateProject - undo')
        self.project.state = self.project_state
        self.project.properties = self.back_up_project_properties

        # If the project name was updated, then the window title is changed
        if(self.project.get_property("name").value != self.new_project.get_property("name").value):
            self.app.setWindowTitle("Proteus - " + self.project.get_property("name").value)
        

class MoveNode(QUndoCommand):
    """
    Command to move node in project tree.
    """

    def __init__(self, project: Project,  obj: Object, from_parent: Object, to_parent:Object, from_row: int, to_row: int):
        proteus.logger.info('Init MoveNode')
        super(MoveNode, self).__init__()
        self.project = project
        self.something_changed = False
        self.obj = obj
        self.original_parent = from_parent
        self.new_parent = to_parent
        self.from_row = from_row
        self.to_row = to_row
        self.original_parent_state = deepcopy(from_parent.state)
        self.new_parent_state = deepcopy(to_parent.state)
        self.project_state = deepcopy(project.state)

    def redo(self):
        """
        Removes node from old position and insert in the new one.
        """
        proteus.logger.info('MoveNode - redo')
        if ((PROTEUS_ANY in self.new_parent.acceptedChildren) or
            any(x in self.new_parent.acceptedChildren for x in self.obj.classes)):
            self.something_changed = True
            self.original_parent.state = ProteusState.DIRTY
            self.new_parent.state = ProteusState.DIRTY
            self.project.state = ProteusState.DIRTY
            self.original_parent.children.pop(self.obj.id)
            my_list = list(self.new_parent.children.items())
            new_tuple = (self.obj.id, self.obj)
            my_list.insert(self.to_row, new_tuple)
            self.new_parent.children = dict(my_list)
            self.obj.parent = self.new_parent
        else:
            proteus.logger.warning("MoveNode - redo - Node not accepted by new parent")

    def undo(self):
        """
        Removes node from new position and insert back in old position.
        """
        proteus.logger.info('MoveNode - undo')
        if(self.something_changed):
            self.original_parent.state = self.original_parent_state
            self.new_parent.state = self.new_parent_state
            self.project.state = self.project_state
            self.new_parent.children.pop(self.obj.id)
            my_list = list(self.original_parent.children.items())
            new_tuple = (self.obj.id, self.obj)
            my_list.insert(self.to_row, new_tuple)
            self.original_parent.children = dict(my_list)
            self.obj.parent = self.original_parent
