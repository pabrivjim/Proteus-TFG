# ==========================================================================
# File: markdown.py
# Description: File where is located the MarkdownWidget.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import logging
from PyQt5.QtWidgets import (QWidget, QTextEdit, QPushButton, QVBoxLayout)

from proteus.model.property import MarkdownProperty

class MarkdownWidget(QWidget):
    """
    Class to edit and visualize markdown object type.
    """

    def __init__(self, parent: QWidget, obj: MarkdownProperty):
        logging.info('Init MarkdownWidget')
        super(MarkdownWidget, self).__init__(parent)

        self.widget = QTextEdit()
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
        logging.info('MarkdownWidget - switch')
        if self.visualize_html:
            self.btn.setText("Visualize")
            self.widget.setPlainText(self.widget.toMarkdown())
        else:
            self.btn.setText("View source")
            self.widget.setMarkdown(self.widget.toPlainText())
        self.visualize_html = not self.visualize_html

    def get_value(self):
        """
        Returns the value of the widget.
        """
        logging.info('MarkdownWidget - get value')
        return self.widget.toMarkdown() if self.visualize_html else self.widget.toPlainText()
