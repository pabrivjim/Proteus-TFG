# ==========================================================================
# File: change_theme.py
# Description: File where is located the settings button.
# Date: 20/03/23
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from proteus import config
from proteus.controllers.utils.i18n import trans
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
        self.settings_tb = QToolButton()
        self.settings_tb.setObjectName("Settings")
        self.settings_tb.setText(trans("Settings"))
        self.settings_tb.setToolTip(trans("Change settings"))
        self.settings_tb.setEnabled(True)
        self.settings_tb.setIcon(QIcon(f"{config.Config().icons_directory}/settings.png"))
        return self.settings_tb
