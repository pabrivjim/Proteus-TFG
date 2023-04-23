"""Module to load preferences."""
# ==========================================================================
# File: preferences.py
# Description: Utils to load preferences.
# Date:
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from os.path import normpath, expanduser
import pathlib
from PyQt5.QtCore import (QCoreApplication, QFile, QSettings, QTextStream,
                          QTranslator)
from PyQt5.QtWidgets import (QMainWindow, QDialog, QMessageBox, QWidget, QLabel)
import proteus.config as config
from proteus.utils.i18n import trans
from proteus.utils.loader import resource_path
from PyQt5 import uic
from PyQt5.QtWidgets import QFileDialog
from configparser import ConfigParser
import proteus
from proteus.view.visualizer import loadCSS

class Preferences:
    """
    Class to load settings from registry.
    """
    def get_app_instance():
        proteus.logger.info('Preferences - get app instance')
        return QCoreApplication.instance()

    @staticmethod
    def load_theme(main: QMainWindow, theme: str) -> None:
        """
        Method that load the theme.

        :param main: Main window.
        :param theme: Theme.
        """
        proteus.logger.info('Preferences - load theme')

        file = QFile(resource_path(f'themes/{theme}.qss'))
        file.open(QFile.ReadOnly | QFile.Text)
        stream = QTextStream(file)
        Preferences.get_app_instance().setStyleSheet(stream.readAll())

    @staticmethod
    def load_language(main: QMainWindow, language: str) -> None:
        """
        Method that load the language.

        :param main: Main window.
        :param language: Language.
        """
        proteus.logger.info('Preferences - load language')

        app = Preferences.get_app_instance()
        translation = "%s.qm" % language
        translator = QTranslator()
        translator.load(translation, f"{config.Config().resources_directory}/i18n/")
        app.installTranslator(translator)

    @staticmethod
    def load_all(main: QMainWindow) -> QSettings:
        """
        load_all

        :param main: Main Window.
        :return: QSettings class.
        """
        proteus.logger.info('Preferences - load all')

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
        proteus.logger.info('Init PreferencesDialog')
        super(PreferencesDialog, self).__init__(parent)
        uic.loadUi(f"{config.Config().resources_directory}/ui/preferences.ui", self)
        
        # Translate the text of the dialog
        self.setWindowTitle(trans("Preferences"))
        self.groupBox_5.setTitle(trans(self.groupBox_5.title()))
        self.xslt_label_path.setText(trans(self.xslt_label_path.text()))
        self.label_path.setText(trans(self.label_path.text()))

        self.was_archetypes_path_changed = False
        self.was_xslt_path_changed = False
        self.load_preferences()
        self.accepted.connect(self.update_preferences)
        self.toolButtonArchetypesPath.clicked.connect(self.select_archetypes_path)
        self.toolButtonXSLTPath.clicked.connect(self.select_xslt_path)


    def select_xslt_path(self):
        """
        Method that select the path of the XSLT directory, save it in the settings with the name xslt_custom_folder,
        as well as in the input path field.
        """
        proteus.logger.info('PreferencesDialog - select xslt path')

        settings = self.parent().settings
        if(settings.value("xslt_custom_file") != None):
            xslt_main_file, _ = QFileDialog.getOpenFileName(None, "Open XSLT File", settings.value("xslt_custom_folder"), "XSLT files (*.xslt)")
        else:
            # In case there is no custom folder, the default folder is the one in the user's documents
            xslt_main_file, _ = QFileDialog.getOpenFileName(None, "Open XSLT File", normpath(expanduser("~/Documents/Proteus")), "XSLT files (*.xslt)")
        if (xslt_main_file!= ""):
            settings.setValue("xslt_custom_file", xslt_main_file)
            self.xsltConfigPath.setText(xslt_main_file)
            self.was_xslt_path_changed = True
            return
        self.was_xslt_path_changed = False

    def select_archetypes_path(self):
        """
        Method that select the path of the archetypes directory, save it in settings with the name archetype_custom_folder,
        as well as in the input path field.
        """
        settings = self.parent().settings
        if(settings.value("archetype_custom_folder") != None):
            archetype_dir = QFileDialog.getExistingDirectory(None, "Open Directory", settings.value("archetype_custom_folder"), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        else:
            # In case there is no custom folder, the default folder is the one in the user's documents
            archetype_dir = QFileDialog.getExistingDirectory(None, "Open Directory", normpath(expanduser("~/Documents/Proteus")), QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if (archetype_dir!= ""):
            settings.setValue("archetype_custom_folder", archetype_dir)
            self.archetypeConfigPath.setText(archetype_dir)
            self.was_archetypes_path_changed = True
            return
        self.was_archetypes_path_changed = False

    def load_preferences(self) -> None:
        """
        Method that load preferences from the settings.
        """
        proteus.logger.info('PreferencesDialog - load preferences')

        settings = self.parent().settings

        theme = settings.value("theme", "light")
        self.radioButtonColorDark.setChecked(theme == "dark")
        self.radioButtonColorWhite.setChecked(theme == "light")

        language = settings.value("language", "en_EN")
        self.comboBoxLanguage.setCurrentText(language)
        if(settings.value("archetype_custom_folder") == None):
            settings.setValue("archetype_custom_folder", normpath(expanduser("~/Documents/Proteus")))

        self.xsltConfigPath.setText(settings.value("xslt_custom_file"))
        self.archetypeConfigPath.setText(settings.value("archetype_custom_folder"))

    def update_preferences(self) -> None:
        """
        Method that update the preferences.
        """
        proteus.logger.info('PreferencesDialog - update preferences')
        settings: QSettings = self.parent().settings

        # In case the archetype custom folder was changed by hand (text) we need to update the settings
        if( settings.value("archetype_custom_folder") != self.archetypeConfigPath.text()):
            self.was_archetypes_path_changed = True
            settings.setValue("archetype_custom_folder", self.archetypeConfigPath.text())

        # If the archetype custom path was changed, we need to update the config file
        if(self.was_archetypes_path_changed):
            # If the path was changed, we need to update the config file
            filename = str(config.Config().config_file)
            parser = ConfigParser()
            parser.read(filename)
            parser.set(config.DIRECTORIES, config.ARCHETYPES_CUSTOM_DIRECTORY, settings.value("archetype_custom_folder"))
            with open(filename, 'w') as configfile:
                parser.write(configfile)
            QMessageBox.about(self,
                              trans("Updated archetypes path"),
                              trans("The new archetypes will be updated after restarting the application."))

        # In case the xslt custom file was changed by hand (text) we need to update the settings
        if( settings.value("xslt_custom_file") != self.xsltConfigPath.text()):
            self.was_xslt_path_changed = True
            settings.setValue("xslt_custom_file", self.xsltConfigPath.text())

        # If the archetype custom path was changed, we need to update the config file
        if(self.was_xslt_path_changed):
            # If the path was changed, we need to update the config file
            filename = str(config.Config().config_file)
            parser = ConfigParser()
            parser.read(filename)
            parser.set(config.DIRECTORIES, config.XSLT_CUSTOM_FILE, settings.value("xslt_custom_file"))
            with open(filename, 'w') as configfile:
                parser.write(configfile)
            QMessageBox.about(self,
                              trans("Updated XSLT file path"),
                              trans("The new XSLT files will be updated after restarting the application."))


        theme = "dark" if self.radioButtonColorDark.isChecked() else "light"
        settings.setValue("theme", theme)

        # Check if visualizers is already created. This are only created when we open a project
        if(hasattr(self.parent(), "visualizers")):
            # When we update the system theme, we need to update the theme of the
            # view that shows the documentation.
            css_stylesheet_path = pathlib.Path(f"{config.Config().resources_directory}/views/rem/{settings.value('theme')}.css").resolve()
            for view in self.parent().visualizers:
                loadCSS(view, str(css_stylesheet_path), "script1", 0)

        # When we update the system theme, we need to update the theme of the
        # application.
        Preferences.load_theme(self.parent(), theme)

        language = self.comboBoxLanguage.currentText()

        if (settings.value("language", "en_EN") != language):
            QMessageBox.about(self,
                              trans("Update language"),
                              trans("The language will be updated after restarting the application."))
        settings.setValue("language", language)
        Preferences.load_language(self.parent(), language)