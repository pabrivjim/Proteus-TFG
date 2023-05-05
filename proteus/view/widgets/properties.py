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
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QComboBox, QCheckBox,
                             QDialogButtonBox, QLabel, QTabWidget, QHBoxLayout,
                             QDialog)
from proteus.controllers.utils.widgets_logic.properties_logic import PropertiesLogic
from proteus.controllers.utils.i18n import trans
from proteus.view.widgets.markdown import MarkdownWidget
import proteus

class PropertyDialog(QDialog):
    """
    Dialog to edit object properties.
    """

    def __init__(self, parent: QWidget, obj: dict) -> None:
        proteus.logger.info('Init PropertyDialog')
        super(PropertyDialog, self).__init__(parent)
        self.setWindowTitle(trans("edit properties"))
        self.obj = obj
        self.updated_obj = copy.deepcopy(self.obj)
        self.properties_logic = PropertiesLogic(self)
        self.init_ui()

    def load_tab_widget(self) -> None:
        """
        Method that loads the tab widget.
        """
        proteus.logger.info('PropertyDialog - load tab widget')
        self.tab_widget = QTabWidget()
        widgets = self.properties_logic.load_widgets()

        # Todo refactor
        # Because there could be different MarkdownWidgets instances, we need to add each so the app
        # knows which one is the actual one.
        markdown_widgets = {}
        for key in widgets.keys():
            if isinstance(widgets[key], QCheckBox):
                widgets[key].stateChanged.connect(
                    lambda value, key=key: self.properties_logic.update_property(key, bool(value)))
            elif isinstance(widgets[key], QComboBox):
                widgets[key].currentTextChanged.connect(
                    lambda value, key=key: self.properties_logic.update_property(key, value))
            elif isinstance(widgets[key], MarkdownWidget):
                markdown_widget = widgets[key]
                markdown_widgets[key] = markdown_widget
                widgets[key].widget.textChanged.connect(
                    lambda key=key: self.properties_logic.update_property(key, markdown_widgets[key].get_value()))
            elif hasattr(widgets[key], "textChanged"):
                widgets[key].textChanged.connect(partial(self.properties_logic.update_property, key))

        layout = QVBoxLayout()
        button_widget = QWidget()
        button_layout = QHBoxLayout()

        button_widget.setLayout(button_layout)
        layout.addWidget(button_widget)

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
