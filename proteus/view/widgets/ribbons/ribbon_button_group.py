# ==========================================================================
# File: ribbon_button_group.py
# Description: File where is located the view related to 
#              the ribbon button group.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtCore import (Qt, QSize)
from PyQt5.QtWidgets import (QWidget, QPushButton, QSizePolicy)
from PyQt5 import uic
import logging

# https://github.com/martijnkoopman/Qt-Ribbon-Widget/
class RibbonButtonGroup(QWidget):
    """
    Ribbon Button Group contains group buttons and group label.
    """

    def __init__(self, title: str):
        logging.info('Init RibbonButtonGroup')
        super(RibbonButtonGroup, self).__init__()
        uic.loadUi("proteus/resources/ui/ribbonButtonGroup.ui", self)
        self.label.setText(title)

    def add_button(self, button: QPushButton) -> None:
        """
        Adds a button to the group.

        :param button: Button to add.
        """
        logging.info('RibbonButtonGroup - add button')
        
        button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        button.setMinimumSize(48, 48)
        button.setMaximumWidth(48)
        # button.setAutoRaise(True)
        button.setIconSize(QSize(32, 32))
        button.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.horizontalLayout.addWidget(button)
