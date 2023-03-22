"""
Proteus - Archetype Controller
"""
# ==========================================================================
# File: archetype.py
# Description: Contains the ArchetypeController which which calls the Archetype
#              Manager, passing the Custom Folder and if there is any error
#              then the normal archetype folder is passed instead as parameter.
# Date: 
# Version: 1.0.0
# Author: Pablo
# ==========================================================================

import proteus
import proteus.config as config
from PyQt5.QtCore import QSettings

from proteus.model.archetype_manager import ArchetypeManager
from .base import Controller

settings = QSettings("Proteus", "SettingsDesktop")
# Template Method Pattern
class ArchetypeController(Controller):
    """
    Class which which calls the Archetype Manager, passing the Custom Folder
    and if there is any error then the normal archetype folder is passed instead
    as parameter.
    """
    def __init__(self, *args, **kwargs):
        super(ArchetypeController, self).__init__(*args, **kwargs)

    def get_object_archetypes(self) -> dict:
        """
        Get the object archetypes.
        """
        return self._get_archetypes(self._load_object_archetypes)
    
    def get_document_archetypes(self) -> dict:
        """
        Get the document archetypes.
        """
        return self._get_archetypes(self._load_document_archetypes)
    
    def get_project_archetypes(self) -> dict:
        """
        Get the project archetypes.
        """
        return self._get_archetypes(self._load_project_archetypes)
    
    def _get_archetypes(self, loader_func) -> dict:
        """
        Get the archetypes using the loader function passed as parameter and
        if there is any error in the custom archetype folder,
        then the normal archetype folder is passed instead as parameter.
        """
        try:
            folder = config.Config().archetypes_custom_directory
            settings.setValue(config.ERROR_ARCHETYPES_CUSTOM_DIR, False)
            return loader_func(folder)
        except Exception as e:
            proteus.logger.error("Error loading configuration file: %s", e)
            folder = config.Config().archetypes_directory
            settings.setValue(config.ERROR_ARCHETYPES_CUSTOM_DIR, True)
            return loader_func(folder)
    
    def _load_object_archetypes(self, folder) -> dict:
        """
        Private method to load the object archetypes.
        """
        return ArchetypeManager.load_object_archetypes(folder)
    
    def _load_document_archetypes(self, folder) -> dict:
        """
        Private method to load the document archetypes.
        """
        return ArchetypeManager.load_document_archetypes(folder)
    
    def _load_project_archetypes(self, folder) -> dict:
        """
        Private method to load the project archetypes.
        """
        return ArchetypeManager.load_project_archetypes(folder)
