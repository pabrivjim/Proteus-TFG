# ==========================================================================
# File: undo_action.py
# Description: File where is located the action (QAction) of undo.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================

from PyQt5.QtWidgets import QAction, QUndoStack
from PyQt5.QtGui import QIcon, QKeySequence
from proteus import config
from proteus.utils.i18n import trans
from proteus.view.widgets.ribbons.ribbon import Ribbon
import proteus


class UndoAction(QUndoStack):
    """
    Class where is located the action (QAction) of undo.
    """

    def getAction(self, ribbon: Ribbon) -> QAction:
        """
        Method that create the action (QToolButton) create a new project.

        :returns: Undo Action
        :rtype: QAction
        """
        proteus.logger.info('UndoAction - get action')
        undoStack = self.parent()
        undo_action = undoStack.createUndoAction(self, trans("undo"))
        undo_action.setShortcut(QKeySequence.Undo)
        undo_action.setIcon(QIcon(f"{config.Config().icons_directory}/undo.png"))
        undo_button = ribbon.undo_tb
        undo_button.setDefaultAction(undo_action)
        undo_button.setIcon(QIcon(f"{config.Config().icons_directory}/undo.png"))
        return undo_button
