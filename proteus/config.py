"""
It initializes the config paths for PROTEUS application.
"""

# ==========================================================================
# File: config.py
# Description: the config paths for PROTEUS application
# Date: 11/10/2022
# Version: 0.1
# Author: Amador Durán Toro
#         Pablo Rivera Jiménez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

from pathlib import Path
from configparser import ConfigParser

# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

import proteus

# --------------------------------------------------------------------------
# Constant declarations for PROTEUS configuration file keys
# --------------------------------------------------------------------------

CONFIG_FILE          : str = 'proteus.ini'
DIRECTORIES          : str = 'directories'
BASE_DIRECTORY       : str = 'base_directory'
ARCHETYPES_DIRECTORY : str = 'archetypes_directory'
RESOURCES_DIRECTORY  : str = 'resources_directory'
ICONS_DIRECTORY      : str = 'icons_directory'
ARCHETYPES_CUSTOM_DIRECTORY : str = 'archetypes_custom_dir'
XSLT_CUSTOM_FILE: str = 'xslt_custom_file'

# --------------------------------------------------------------------------
# Constant declarations for QSettings for QApplication
# --------------------------------------------------------------------------
ERROR_ARCHETYPES_CUSTOM_DIR = "error_archetypes_custom_directory"

# --------------------------------------------------------------------------
# Class: Config
# Description: Class for the Configuration PROTEUS application
# Date: 11/10/2022
# Version: 0.1
# Author: Amador Durán Toro
#         Pablo Rivera Jiménez
# --------------------------------------------------------------------------
# TODO: this should be a Qt application in the future
# --------------------------------------------------------------------------

class Config:
    """
    Class for the Configuration PROTEUS application.
    """
    def __init__(self):
        """
        It initializes the config paths for PROTEUS application.
        """
        # This is line is needed when we want to run sphinx, otherwise it will fail
        # due to problems with the working directory.
        # import os
        # _proteus_tfg_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # os.chdir(_proteus_tfg_path)

        # Application configuration
        self.config : ConfigParser = self._create_config_parser()
        self.directories = self.config[DIRECTORIES]

        # Application directories
        self.base_directory       : Path = Path.cwd() / self.directories[BASE_DIRECTORY]
        self.resources_directory  : Path = Path.cwd() / self.directories[RESOURCES_DIRECTORY]
        self.icons_directory      : Path = self.resources_directory / self.directories[ICONS_DIRECTORY]
        self.archetypes_directory : Path = Path.cwd() / self.directories[ARCHETYPES_DIRECTORY]
        self.archetypes_custom_directory : Path = None
        self.xslt_custom_file : Path = None
        # Custom Archetypes directory
        if(ARCHETYPES_CUSTOM_DIRECTORY in self.directories):
            self.archetypes_custom_directory : Path = Path.cwd() / self.directories[ARCHETYPES_CUSTOM_DIRECTORY]

        # Custom XSLT directory
        if(XSLT_CUSTOM_FILE in self.directories):
            self.xslt_custom_file : Path = Path.cwd() / self.directories[XSLT_CUSTOM_FILE]

        # Check application directories
        self.check_application_directories()

    def _create_config_parser(self) -> ConfigParser:
        """
        Private methdos that creates configuration parser and loads config file.

        :returns: ConfigParser
        :rtype: ConfigParser
        """
        proteus.logger.info("Creating PROTEUS configuration parser")

        assert Path(CONFIG_FILE).exists(), \
            f"PROTEUS configuration file {CONFIG_FILE} does not exist! {Path(CONFIG_FILE).absolute()} cwd: {Path.cwd()}"
        self.config_file = Path(CONFIG_FILE).absolute()
        config_parser : ConfigParser = ConfigParser()
        config_parser.read(CONFIG_FILE)

        return config_parser

    def check_application_directories(self) -> None:
        """
        It checks that essential PROTEUS directories exist.

        :returns: None
        """
        proteus.logger.info("Checking PROTEUS directories...")

        # Check if resources directory exists
        assert self.resources_directory.is_dir(), \
            f"PROTEUS resources directory '{self.resources_directory}' does not exist!"

        proteus.logger.info("  Resources directory OK")


        # Check if icons directory exists
        assert self.icons_directory.is_dir(), \
            f"PROTEUS icons directory '{self.icons_directory}' does not exist!"

        proteus.logger.info("  Icons directory OK")


        # Check if archetypes directory exists
        assert self.archetypes_directory.is_dir(), \
            f"PROTEUS archetypes directory '{self.archetypes_directory}' does not exist!"

        proteus.logger.info("  Archetypes directory OK")


        # Check if projects archetypes exists
        assert (self.archetypes_directory / "projects").is_dir(), \
            f"PROTEUS archetypes projects directory '{self.archetypes_directory / 'projects'}' does not exist!"

        proteus.logger.info("  Archetypes projects directory OK")


        # Check if documents archetypes exists
        assert (self.archetypes_directory / "documents").is_dir(), \
            f"PROTEUS archetypes document directory '{self.archetypes_directory / 'documents'}' does not exist!"

        proteus.logger.info("  Archetypes documents directory OK")


        # Check if objects archetypes exists
        assert (self.archetypes_directory / "objects").is_dir(), \
            f"PROTEUS archetypes objects directory '{self.archetypes_directory / 'objects'}' does not exist!"

        proteus.logger.info("  Archetypes objects directory OK")
