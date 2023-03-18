# ==========================================================================
# File: traces.py
# Description: File where are located the traces.
# Date: 04/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QVBoxLayout, QComboBox, QListWidget,
                             QDialogButtonBox, QLabel, QDialog)
from PyQt5.QtGui import QIcon
import proteus.config as config
import proteus.utils.persistence as persistance
from proteus.utils.i18n import trans
import proteus.utils.model.traces_logic as trl
from proteus.utils.model.nodes_utils import get_node
import proteus

class TraceFormDialog(QDialog):
    """
    Dialog to add new object traces.
    """

    def __init__(self, parent=None):
        proteus.logger.info('Init TraceFormDialog')
        super(TraceFormDialog, self).__init__(parent)
        self.setWindowTitle("Add trace")
        self.trace_logic = trl.TraceLogic(self)

        self.object_list_widget = QListWidget()
        objects = persistance.get_project_objects(parent.parentWidget().project.data)

        self.trace_logic.list_widget_add_item(objects)

        trace_types = self.trace_logic.get_traces_types()
        trace_type_combo = QComboBox()
        trace_type_combo.addItems(trace_types)

        button_box = QDialogButtonBox()
        button_box.addButton("Add", QDialogButtonBox.AcceptRole)
        button_box.addButton("Cancel", QDialogButtonBox.RejectRole)

        #If any item is seleted then, the we add that item and the type of trace as a trace.
        #If we haven't selected any item, then we don't add any trace.
        button_box.accepted.connect(
            lambda: self.trace_logic.add_trace(
                self.object_list_widget.itemFromIndex(self.object_list_widget.selectedIndexes()[0]).data(Qt.UserRole),
                trace_type_combo.currentText()) if len(self.object_list_widget.selectedItems()) != 0 else None) 
        button_box.rejected.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Object"))
        layout.addWidget(self.object_list_widget)
        layout.addWidget(QLabel("Trace type"))
        layout.addWidget(trace_type_combo)
        layout.addWidget(button_box)
        self.setLayout(layout)

class DeleteObjectWithTraces(QDialog):
    def __init__(self, traces, project):
        super().__init__()

        # Hide Question Mark
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        
        self.resize(500, 200)

        warning_text = "<html>"+trans("If you delete this item, the following traces will be discarted")+":<ul>"
        for trace in traces:
            name = get_node(project, trace)["properties"]["name"]["value"]
            warning_text += f'<li>{name}</li>'
        
        warning_text += "</ul></html>"
        

        #We set the title of the window
        self.setWindowTitle(trans("Traces will be lost even if you undo your changes!"))

        #We add a QdialogButton with ok or cancel
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        
        #Set the layout and the message with an link
        self.layout = QVBoxLayout()
        message = QLabel()
        message.setText(warning_text)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
        self.setWindowIcon(QIcon(f'{config.Config().resources_directory}/icons/warning.svg'))