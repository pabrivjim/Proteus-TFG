# ==========================================================================
# File: markdown.py
# Description: File where is located the MarkdownWidget.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import proteus
from PyQt5.QtWidgets import (QWidget, QTextEdit, QPushButton, QVBoxLayout)

from proteus.model.property import MarkdownProperty
from proteus.utils.i18n import trans

class MarkdownWidget(QWidget):
    """
    Class to edit and visualize markdown object type.
    """

    def __init__(self, parent: QWidget, obj: MarkdownProperty):
        proteus.logger.info('Init MarkdownWidget')
        super(MarkdownWidget, self).__init__(parent)

        self.widget = QTextEdit(parent)
        self.widget.setPlainText(obj.value)
        # self.widget.setEnabled(False)
        self.btn = QPushButton("Visualize")
        self.visualize_html = False

        lv = QVBoxLayout()
        lv.setContentsMargins(0, 0, 0, 0)
        lv.addWidget(self.widget)
        lv.addWidget(self.btn)
        self.setLayout(lv)

    def switch(self):
        """
        Switches between plain text and html.
        """
        proteus.logger.info('MarkdownWidget - switch')
        if self.visualize_html:
            self.btn.setText(trans("Visualize"))
            self.widget.setPlainText(self.widget.toMarkdown())
        else:
            self.btn.setText(trans("View source"))
            self.widget.setMarkdown(self.widget.toPlainText())
        self.visualize_html = not self.visualize_html

    def get_value(self):
        """
        Returns the value of the widget.
        """
        proteus.logger.info('MarkdownWidget - get value')
        return self.widget.toMarkdown() if self.visualize_html else self.widget.toPlainText()
