# ==========================================================================
# File: main_window_logic.py
# Description: File where is located the project dialog logic.
# Date: 08/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import copy
import shortuuid
from PyQt5.QtCore import (Qt, QModelIndex)
from proteus.model.archetype_proxys import ObjectArchetypeProxy
from proteus.model.object import Object
from proteus.utils.model.qundo_commands import CreateObject
import proteus

class MainWindowLogic():
    """
    Class that contains the logic of the main window.
    """

    def __init__(self, parent) -> None:
        proteus.logger.info('Init MainWindowLogic')
        self.parent = parent
    
    def select_object(self, index: QModelIndex) -> None:
        """
        Updates selected object, focus object and enables accepted archetypes
        in the ribbon.

        :param index: index of object in the QTreeWidget.
        """
        proteus.logger.info('Main Window Logic - select object')

        item = self.parent.document_tree.itemFromIndex(index)
        obj: Object = item.data(0, Qt.UserRole)
        self.parent.views.focus_object(item.data(0, Qt.UserRole).id)
        self.parent.selected_object: Object = item.data(0, Qt.UserRole)
        for button in self.parent.ribbon.buttons:
            tb, b, b_type = self.parent.ribbon.buttons[button]
            if b_type == "archetype":
                # Check if :Proteus-any or archetype class in acceptedChildren
                accepted = {":Proteus-any", button} & set(obj.acceptedChildren)
                print(accepted)
                print(button)
                tb.setEnabled(bool(accepted))


    def add_object(self, obj: ObjectArchetypeProxy) -> None:
        """
        Adds a child to the selected object.

        :param obj: The object to be cloned and inserted.
        """
        proteus.logger.info('Main Window Logic - add object')
        
        if self.parent.selected_object:
            obj_clone = copy.copy(obj.get_object(self.parent.projectController.project))
            obj_clone.id = str(shortuuid.random(length=12))
            command = CreateObject(self.parent.projectController.project, self.parent.selected_object,
                                   obj_clone)

            self.parent.undoStack.push(command)
        
    def combo_box_add_item(self):
        """
        Adds an item to the combo box.
        """
        proteus.logger.info('Main Window Logic - combo box add item')
        
        for document in self.parent.projectController.project.documents.values():
            name = document.get_property("name").value
            self.parent.document_combobox.addItem(name, document)