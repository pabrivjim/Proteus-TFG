# ==========================================================================
# File: tree.py
# Description: File where is located the TreeWidget.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtCore import (Qt, pyqtSignal)
from PyQt5.QtWidgets import (QTreeWidget, QFrame)
from proteus.utils.widgets_logic.tree_logic import TreeLogic
import proteus

class DocumentInspector(QTreeWidget):
    """
    Custom tree widget for project documents.
    """
    mimetype = "application/x-tree-view"
    update = pyqtSignal(dict)
    
    def __init__(self, parent) -> None:
        proteus.logger.info('Init DocumentInspector')
        super(DocumentInspector, self).__init__(parent)
        self.parent = parent
        self._draggedItem = None
        self.tree_logic = TreeLogic(self, self.parent, self._draggedItem)

        # Load and context menu
        self.tree_logic.load_document()
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.tree_logic.open_menu)
        self.doubleClicked.connect(self.tree_logic.edit_item)

        # Conf
        self.setExpandsOnDoubleClick(False)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setHeaderHidden(True)
        self.setFrameShape(QFrame.NoFrame)
    
    # TODO https://stackoverflow.com/questions/67658471/get-mouse-press-event-from-any-widget/67663766#67663766
    
    def load_document(self) -> None:
        """
        Method that load document.
        """
        proteus.logger.info('DocumentInspector - load document')
        return self.tree_logic.load_document()
    
    def startDrag(self, supportedActions) -> None:
        """
        Event that detects the start drag action.
        """
        proteus.logger.info('DocumentInspector - start drag')
        self.tree_logic.startDrag(supportedActions)

    def dropEvent(self, event):
        """
        Event that detects the drop action.
        """
        proteus.logger.info('DocumentInspector - drop event')
        self.tree_logic.dropEvent(event)

