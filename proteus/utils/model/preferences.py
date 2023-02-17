# ==========================================================================
# File: preferences.py
# Description: Utils to load preferences.
# Date:
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from os.path import normpath, expanduser
from PyQt5.QtCore import (QCoreApplication, QFile, QSettings, QTextStream,
                          QTranslator)
from PyQt5.QtWidgets import (QMainWindow, QDialog)
import proteus.utils.config as config 
from proteus.utils.loader import resource_path
from PyQt5 import uic
import logging

class Preferences:
    """
    Class to load settings from registry.
    """
    def get_app_instance():
        logging.info('Preferences - get app instance')
        return QCoreApplication.instance()

    @staticmethod
    def load_theme(main: QMainWindow, theme: str) -> None:
        """
        load_theme

        :param main: Main window.
        :param theme: Theme.
        """
        logging.info('Preferences - load theme')
        
        file = QFile(resource_path(f'themes/{theme}.qss'))
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        Preferences.get_app_instance().setStyleSheet(stream.readAll())

    @staticmethod
    def load_language(main: QMainWindow, language: str) -> None:
        """
        load_language

        :param main: Main window.
        :param language: Language.
        """
        logging.info('Preferences - load language')
        
        app = Preferences.get_app_instance()
        translation = "%s.qm" % language
        translator = QTranslator()
        translator.load(translation, f"{config.CONFIG_FOLDER}/i18n/")
        app.installTranslator(translator)

    @staticmethod
    def load_all(main: QMainWindow) -> QSettings:
        """
        load_all

        :param main: Main Window.
        :return: QSettings class.
        """
        logging.info('Preferences - load all')
        
        settings = QSettings("Proteus", "SettingsDesktop")

        theme = settings.value("theme", "light")
        Preferences.load_theme(main, theme)

        language = settings.value("language", "en_EN")
        Preferences.load_language(main, language)

        return settings


class PreferencesDialog(QDialog):
    """
    Dialog to change preferences.
    """

    def __init__(self, parent):
        logging.info('Init PreferencesDialog')
        super(PreferencesDialog, self).__init__(parent)
        uic.loadUi("proteus/resources/ui/preferences.ui", self)

        self.load_preferences()
        self.accepted.connect(self.update_preferences)

    def load_preferences(self) -> None:
        """
        Method that load preferences from the settings.
        """
        logging.info('PreferencesDialog - load preferences')
        
        settings = self.parent().settings

        theme = settings.value("theme", "light")
        self.radioButtonColorDark.setChecked(theme == "dark")
        self.radioButtonColorWhite.setChecked(theme == "light")

        language = settings.value("language", "en_EN")
        self.comboBoxLanguage.setCurrentText(language)

        config_folder = settings.value("config_folder", normpath(expanduser("~/Documents/Proteus")))
        self.configPath.setText(config_folder)

    def update_preferences(self) -> None:
        """
        Method that update the preferences.
        """
        logging.info('PreferencesDialog - update preferences')
        
        settings = self.parent().settings

        theme = "dark" if self.radioButtonColorDark.isChecked() else "light"
        settings.setValue("theme", theme)
        Preferences.load_theme(self.parent(), theme)

        language = self.comboBoxLanguage.currentText()
        settings.setValue("language", language)
        Preferences.load_language(self.parent(), language)
