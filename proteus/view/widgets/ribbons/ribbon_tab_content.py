# ==========================================================================
# File: ribbon_tab_content.py
# Description: File where is located the view related to
#              the tab content.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from .ribbon_button_group import RibbonButtonGroup
from PyQt5.QtWidgets import (QWidget)
from PyQt5 import uic
import proteus

class RibbonTabContent(QWidget):
    """
    Tab Widget container.
    """

    def __init__(self):
        proteus.logger.info('Init RibbonTabContent')
        super(RibbonTabContent, self).__init__()
        uic.loadUi("proteus/resources/ui/ribbonTabContent.ui", self)

    def add_group(self, title: str) -> RibbonButtonGroup:
        """
        Adds a group to a tab.

        :param title: Group title.
        :return: Button group.
        """
        proteus.logger.info('RibbonTabContent - add group')

        button_group = RibbonButtonGroup(title)
        self.ribbonHorizontalLayout.addWidget(button_group)
        return button_group
