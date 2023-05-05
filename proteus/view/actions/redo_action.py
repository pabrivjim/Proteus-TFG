# ==========================================================================
# File: redo_action.py
# Description: File where is located the action (QAction) of redo.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================

from PyQt5.QtWidgets import QAction, QUndoStack
from PyQt5.QtGui import QIcon, QKeySequence
from proteus import config
from proteus.controllers.utils.i18n import trans
from proteus.view.widgets.ribbons.ribbon import Ribbon
import proteus

class RedoAction(QUndoStack):
    """
    Class where is located the action (QAction) of redo.
    """

    def getAction(self, ribbon: Ribbon) -> QAction:
        """
        Method that create the action (QToolButton) create a new project.

        :returns: Redo Action
        :rtype: QAction
        """
        proteus.logger.info('RedoAction - get action')
        redoStack = self.parent()
        redo_action = redoStack.createRedoAction(self, trans("Redo"))
        redo_action.setShortcut(QKeySequence.Redo)
        redo_action.setIcon(QIcon(f"{config.Config().icons_directory}/redo.png"))
        redo_button = ribbon.redo_tb
        redo_button.setDefaultAction(redo_action)
        redo_button.setIcon(QIcon(f"{config.Config().icons_directory}/redo.png"))
        return redo_button
