# ==========================================================================
# File: traces_logic.py
# Description: File where is located de logic of the TreeWidget.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from proteus.controllers.incoming_traces import IncomingTraces
from proteus.utils.model.nodes_utils import get_node
import proteus.view.widgets.traces as traces
import logging
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox
import proteus.utils.config as config
from proteus.utils.i18n import trans
from os.path import join, dirname
import yaml

class TraceLogic():
    """
    Class that contains the trace logic.
    """
    def __init__(self, parent) -> None:
        logging.info('Init TraceLogic')
        self.parent = parent

    @staticmethod
    def open(parent=None):
        """
        Method that execute the function that 
        opens the trace dialog.
        """
        logging.info('TraceLogic - open')
        d = traces.TraceFormDialog(parent)
        d.exec()
    
    @staticmethod
    def delete_outgoing_traces(project, traces, trace_to_delete):
        """
        Method that delete traces of an object because the object
        which was traced is deleted.
        """
        logging.info('TraceLogic - Delete outgoing traces')
        for trace in traces:
            node = get_node(project,trace)

            # For each trace of the list of traces of the object,
            # we delete the trace of the object that is deleted.
            for index, element in enumerate(node["traces"]): 
                if element["id"] == trace_to_delete:
                    del node["traces"][index]
                    break
            

    def remove(self):
        """
        Method that removes a trace of an object.
        """
        logging.info('TraceLogic - remove')
        # We get the row of the selected item.
        selected_item_index = self.traces_widget.currentIndex().row()

        # We delete the item from the traces
        del self.updated_obj["traces"][selected_item_index]
        
        # We remove it from the QTreeWidget
        self.traces_widget.takeTopLevelItem(selected_item_index)
        
        # If the QTreeWidget is empty, we disable the remove button.
        if(self.traces_widget.topLevelItemCount() == 0):
            self.remove_button.setDisabled(True)

    def add_trace(self, obj, trace_type):
        """
        Method that add a trace to the object.
        """
        logging.info('TraceLogic - add trace')
        if("traces" in self.parent.parentWidget().updated_obj):
            traces = self.parent.parentWidget().updated_obj["traces"]
            for t in traces:
                if t["id"] == obj["id"]:
                    t["type"] = trace_type
                    self.parent.parentWidget().load_traces()
                    self.parent.close()
                    return

            traces.append({
                "id": obj["id"],
                # "name": obj["properties"]["name"]["value"],
                # "klass": obj["classes"][len(obj["classes"]) - 1],
                "type": trace_type
            })
            self.parent.parentWidget().load_traces()
            self.parent.close()
            if(self.parent.parent().traces_widget.topLevelItemCount() > 0 and not self.parent.parent().remove_button.isEnabled()):
                self.parent.parent().remove_button.setEnabled(True)
            trace = IncomingTraces(obj["id"])
            trace.add_trace(self.parent.parentWidget().updated_obj["id"])

        else:
            self.parent.close()
            QMessageBox.about(self.parent,
                              trans("Sorry!"),
                              trans("You can't add traces to this object."))

    
    def list_widget_add_item(self, objects):
        """
        Add item to list widget trace.
        """
        for obj in objects:
            klass = obj['classes'][len(obj['classes']) - 1]
            item_name = obj["properties"]["name"]["value"]

            item = QListWidgetItem(item_name)
            item.setData(Qt.UserRole, obj)
            item.setIcon(
                QIcon(f"{config.CONFIG_FOLDER}/assets/icons/{klass}.svg"))
            self.parent.object_list_widget.addItem(item)
    
    @staticmethod
    def get_traces_types():
        """
        Method that returns the types of the traces.
        """

        #TODO archivo de configuración
        with open(join(config.CONFIG_FOLDER, "traces/types") + ".yaml", encoding='utf8') as file:
            types = yaml.load(file, Loader=yaml.FullLoader)
        return(types)

