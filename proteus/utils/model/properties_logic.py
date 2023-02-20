# ==========================================================================
# File: properties_logic.py
# Description: File where is located de logic of properties.
# Date: 04/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtGui import (QIcon)
from proteus.model.object import Object
from proteus.model.property import Property
from proteus.utils.model.nodes_utils import get_node
from proteus.utils.model.qundo_commands import UpdateNode
import proteus.utils.config as config 
from proteus.controllers.save_state_machine import SaveMachine
from PyQt5.QtWidgets import (QWidget, QTreeWidgetItem, QVBoxLayout,
                             QLabel,QHBoxLayout)
from proteus.utils.i18n import trans
import proteus.utils.model.widgets_utils as widgets_utils
import logging

class PropertiesLogic():
    """
    Class that contains the logic of the property dialog.
    """
    def __init__(self, parent) -> None:
        logging.info('Init PropertiesLogic')
        self.parent = parent
    
    def load_traces(self) -> None:
        """
        Method that load the traces
        """
        logging.info('PropertiesLogic - load traces')
        
        self.traces_widget = self.parent.traces_widget
        self.updated_obj: Object = self.parent.updated_obj
        # print(self.parent)
        # print(self.parent.parent().project.data)
        self.traces_widget.clear()
        self.traces_widget.setHeaderItem(QTreeWidgetItem(["Name", "Trace type"]))
        

    def update_property(self, prop, value) -> None:
        """
        Method that updates the properties of the object.
        """
        logging.info('PropertiesLogic - update property')
        
        self.updated_obj["properties"][prop]["value"] = value

    def save_changes(self) -> None:
        """
        Method that saves object or document changes.
        """
        logging.info('PropertiesLogic - save changes')
        
        app = self.parent.parentWidget()
        project_data = app.projectController.project
        obj = SaveMachine(self.updated_obj["id"])

        command = UpdateNode(project_data, self.updated_obj["id"], self.updated_obj, obj)
        self.parent.parentWidget().undoStack.push(command)
        self.parent.close()

    def load_widgets(self):
        """
        Method that load the widgets.
        """
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