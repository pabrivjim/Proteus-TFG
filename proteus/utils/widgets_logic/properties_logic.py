# ==========================================================================
# File: properties_logic.py
# Description: File where is located de logic of properties.
# Date: 04/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from proteus.model.object import Object
from proteus.model.project import Project
from proteus.model.property import Property
from proteus.utils.widgets_logic.qundo_commands import UpdateObject, UpdateProject
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,QHBoxLayout)
from proteus.utils.i18n import trans
import proteus.utils.widgets_utils as widgets_utils
import proteus

class PropertiesLogic():
    """
    Class that contains the logic of the property dialog.
    """
    def __init__(self, parent) -> None:
        proteus.logger.info('Init PropertiesLogic')
        self.parent = parent
        self.updated_item: Object = self.parent.updated_obj
        self.obj = self.parent.obj

    def update_property(self, prop, value) -> None:
        """
        Method that updates the properties of the object.
        """
        proteus.logger.info('PropertiesLogic - update property')

        new_prop : Property = self.obj.get_property(prop).clone(value)
        self.updated_item.set_property(new_prop)

    def save_changes(self) -> None:
        """
        Method that saves the changes of the properties in the project.
        """
        proteus.logger.info('PropertiesLogic - save changes')

        app = self.parent.parentWidget()
        project_data = app.projectController.project
        if(isinstance(self.updated_item, Project)):
            command = UpdateProject(project_data, self.updated_item)
            self.parent.parentWidget().undoStack.push(command)
        else:
            command = UpdateObject(project_data, self.obj, self.updated_item)
            self.parent.parentWidget().undoStack.push(command)

        self.parent.close()

    def load_widgets(self):
        """
        Method that load the widgets.
        """
        proteus.logger.info('PropertiesLogic - load widgets')
        categories = {}
        widgets = {}
        name: str
        prop: Property
        for name, prop in self.parent.obj.properties.items():
            category = prop.category

            if category in categories:
                categories[category][name] = prop
            else:
                categories[category] = {name: prop}
                
        for category, properties in categories.items():
            widget = QWidget()
            layout = QVBoxLayout()

            for name, prop in properties.items():
                w = QWidget()
                hl = QHBoxLayout() if prop.element_tagname != "text" else QVBoxLayout()
                label = QLabel(trans(name))


                widgets[name] = widgets_utils.get_widget_for_property(prop)
                hl.addWidget(label)
                hl.addWidget(widgets[name])
                hl.setStretch(0, 1)
                hl.setStretch(1, 3)
                w.setLayout(hl)
                layout.addWidget(w)

            layout.addStretch(1)
            widget.setLayout(layout)
            self.parent.tab_widget.addTab(widget, trans(category))
        return widgets