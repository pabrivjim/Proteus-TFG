# ==========================================================================
# File: properties.py
# Description: File where are located the properties.
# Date: 04/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import copy
from functools import partial
from PyQt5.QtGui import (QImage, QPixmap)
from PyQt5.QtCore import (Qt)
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout,
                             QComboBox, QCheckBox, QDialogButtonBox, QLabel,
                             QTreeWidget, QTabWidget, QHBoxLayout,
                             QDialog)
from proteus.utils.model.properties_logic import PropertiesLogic
from proteus.utils.i18n import trans
import proteus.utils.model.traces_logic as traces
from proteus.view.widgets.markdown import MarkdownWidget
import logging

class PropertyDialog(QDialog):
    """
    Dialog to edit object properties.
    """

    def __init__(self, parent: QWidget, obj: dict) -> None:
        logging.info('Init PropertyDialog')
        super(PropertyDialog, self).__init__(parent)
        self.setWindowTitle(trans("edit properties"))
        self.properties_logic = PropertiesLogic(self)
        self.obj = obj
        self.updated_obj = copy.deepcopy(self.obj)
        self.traces_widget = QTreeWidget()
        self.traces_widget.currentItem()
        
        

        self.init_ui()

    def load_tab_widget(self) -> None:
        """
        Method that loads the tab widget.
        """
        logging.info('PropertyDialog - load tab widget')
        
        self.tab_widget = QTabWidget()
        widgets = self.properties_logic.load_widgets()
        
        # Todo refactor
        for key in widgets.keys():
            if isinstance(widgets[key], QCheckBox):
                widgets[key].stateChanged.connect(
                    lambda value, key=key: self.properties_logic.update_property(key, bool(value)))
            elif isinstance(widgets[key], QComboBox):
                widgets[key].currentTextChanged.connect(
                    lambda value, key=key: self.properties_logic.update_property(key, value))
            elif isinstance(widgets[key], MarkdownWidget):
                markdown_widget = widgets[key]
                widgets[key].btn.clicked.connect(
                    lambda: markdown_widget.switch())
                widgets[key].widget.textChanged.connect(
                    lambda key=key: self.properties_logic.update_property(key, markdown_widget.get_value()))
            elif hasattr(widgets[key], "textChanged"):
                widgets[key].textChanged.connect(partial(self.properties_logic.update_property, key))

        # Trace widget todo refactor
        trace_widget = QWidget()
        add_button = QPushButton("Add trace")
        self.remove_button = QPushButton("Remove trace")

        #BUG when open project
        self.remove_button.setDisabled(True)
        add_button.clicked.connect(lambda: traces.TraceLogic.open(self))
        self.remove_button.clicked.connect(lambda: traces.TraceLogic.remove(self))

        self.properties_logic.load_traces()

        layout = QVBoxLayout()
        button_widget = QWidget()
        button_layout = QHBoxLayout()

        layout.addWidget(self.traces_widget)
        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)
        button_layout.addWidget(add_button)
        button_layout.addWidget(self.remove_button)
        trace_widget.setLayout(layout)

        self.tab_widget.addTab(trace_widget, trans("traces"))

        return self.tab_widget

    def init_ui(self) -> None:
        """
        init_ui
        """
        tab_widget = self.load_tab_widget()

        button_box = QDialogButtonBox(Qt.Vertical)
        # button_box.addButton("Settings...", QDialogButtonBox.RejectRole)
        button_box.addButton("OK", QDialogButtonBox.AcceptRole)
        button_box.addButton("Cancel", QDialogButtonBox.RejectRole)
        button_box.accepted.connect(self.properties_logic.save_changes)
        button_box.rejected.connect(self.close)

        logo_image = QImage()
        logo_image.load("icons/logo_us.png")
        logo = QLabel()
        logo.setPixmap(QPixmap.fromImage(logo_image))

        v_layout = QVBoxLayout()
        v_layout.addWidget(button_box)
        v_layout.addWidget(logo)
        vw = QWidget()
        vw.setLayout(v_layout)

        layout = QHBoxLayout()
        layout.addWidget(tab_widget)
        layout.addWidget(vw)

        self.setLayout(layout)

    def load_traces(self):
        """
        Load traces in the tree widget.
        """
        logging.info('PropertyDialog - load traces')
        self.properties_logic.load_traces()