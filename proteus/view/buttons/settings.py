# ==========================================================================
# File: change_theme.py
# Description: File where is located the settings button.
# Date: 20/03/23
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus.utils.i18n import trans
from proteus.utils.loader import resource_path
import proteus

class Settings():
    """
    Class where is located the button (QToolButton) of settings.
    """

    def getButton(self) -> QToolButton:
        """
        Method that creates the action (QToolButton) of settings.
        :returns: Action of settings.
        :rtype: QToolButton
        """
        proteus.logger.info('ChangeTheme Button - get button')
        
        self.create_tb = QToolButton()
        self.create_tb.setObjectName("Settings")
        self.create_tb.setText(trans("Settings"))
        self.create_tb.setToolTip(trans("Change settings"))
        self.create_tb.setEnabled(True)
        self.create_tb.setIcon(QIcon(resource_path("icons/settings.png")))
        return self.create_tb
