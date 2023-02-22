# ==========================================================================
# File: ribbon.py
# Description: File where is located the view related to ribbons (TOP MENU).
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from functools import partial
from PyQt5.QtWidgets import (QWidget, QTabWidget,
                             QToolButton)
from proteus.utils.i18n import trans
from proteus.view.buttons import (open_project, new_project, save_project,
                          edit_project, create_document, delete_document,
                          export_document)
from .ribbon_tab_content import RibbonTabContent
from proteus.utils.model.ribbons_logic import RibbonsLogic
import logging

class Ribbon:
    """
    Ribbon styled top menu.
    """

    def __init__(self, parent: QWidget, tab_widget: QTabWidget):
        logging.info('Init Ribbon')
        
        self.parent = parent
        self.tab_widget = tab_widget
        self.buttons = {}

        # Buttons creation
        self.create_buttons()
        self.connect_buttons()
        self.tabs_add_button()

        # Archetypes
        self.ribbons_logic = RibbonsLogic(self)
        self.ribbons_logic.set_archetypes()
    
    def create_buttons(self) -> None:
        """
        Method that create buttons.
        """
        logging.info('Ribbon - create buttons')
        #Projects
        self.open_tb = open_project.OpenProject().getButton()
        self.new_tb = new_project.NewProject().getButton()
        self.save_tb = save_project.SaveProject().getButton()
        self.edit_tb = edit_project.EditProject().getButton()

        # Documents
        self.create_tb = create_document.CreateDocument().getButton()
        self.delete_tb = delete_document.DeleteDocument().getButton()
        self.export_tb = export_document.ExportDocument().getButton()

        # Edition
        self.undo_tb = QToolButton()
        self.redo_tb = QToolButton()
    
    def connect_buttons(self):
        """
        Method that connects the buttons to the actions.
        """
        logging.info('Ribbon - connect buttons')
        # When Open Project Button is clicked, open the project dialog.
        self.open_tb.clicked.connect(self.parent.file.req_open_project)

        # When New Project Button is clicked, open the new project dialog.
        self.new_tb.clicked.connect(self.parent.file.req_new_project)

        # When Save Project Button is clicked, save the project.
        self.save_tb.clicked.connect(self.parent.file.req_save_project)

        # When Edit Project Button is clicked, open the edit project dialog.
        self.edit_tb.clicked.connect(self.parent.projectController.edit_project)

        # When Create Document Button is clicked, open the create document dialog.
        self.create_tb.clicked.connect(self.parent.projectController.create_document)

        self.export_tb.clicked.connect(self.parent.projectController.export_project)

        # When Delete Document Button is clicked, delete the document.
        self.delete_tb.clicked.connect(self.parent.projectController.remove_document)

    def tabs_add_button(self):
        """
        Adds buttons to the tabs.
        """
        logging.info('Ribbon - tabs add button')
        tab_content = self.add_tab(trans("project"))
        project_group = tab_content.add_group(trans("project"))

        # Project Tab
        project_group.add_button(self.open_tb)
        project_group.add_button(self.new_tb)
        project_group.add_button(self.save_tb)
        project_group.add_button(self.edit_tb)

        # Document Tab
        document_group = tab_content.add_group(trans("document"))
        document_group.add_button(self.create_tb)
        document_group.add_button(self.delete_tb)
        document_group.add_button(self.export_tb)

        #Edit Tab
        edit_group = tab_content.add_group(trans("edit"))
        edit_group.add_button(self.undo_tb)
        edit_group.add_button(self.redo_tb)

    def add_tab(self, name: str) -> RibbonTabContent:
        """
        Adds a tab to the ribbon menu.

        :param name: Tab name.
        :return: Tab widget.
        """
        logging.info('Ribbon - add tab')
        
        tab = RibbonTabContent()
        self.tab_widget.addTab(tab, name)
        return tab
