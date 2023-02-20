# ==========================================================================
# File: archetype_manager.py
# Description: PROTEUS archetype manager
# Date: 01/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
#         Amador Durán Toro
# ==========================================================================
# Update: 01/10/2022 (Amador)
# Description:
# - Code review.
# ==========================================================================

# standard library imports
import logging
import shortuuid
from enum import Enum, auto
from os import listdir
import os
from os.path import join, dirname, abspath, isfile, isdir, exists
from os import pardir
import shutil

# other libraries imports
import lxml.etree as ET

import proteus.model.config as config

# PROTEUS imports
from proteus.model import PROPERTIES_TAG
from proteus.model.archetype_proxys import DocumentArchetypeProxy, ObjectArchetypeProxy, ProjectArchetypeProxy
from proteus.model.property import Property, PropertyFactory

# logging configuration
log = logging.getLogger(__name__)

# TODO: estos directorios habrá que establecerlos por configuración o como
# parámetros pasados al comienzo de la aplicación.


ARCHETYPES_FOLDER = config.Config().archetypes_directory
PROJECT_PROPERTIES_TO_SAVE = ["name", "description", "author", "date"]
DOCUMENT_PROPERTIES_TO_SAVE = ["name", "description", "author", "date"]

# --------------------------------------------------------------------------
# Class: ArchetypesType
# Description: String-based enumeration for archetypes' types
# Date: 01/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------
# https://stackoverflow.com/questions/58608361/string-based-enum-in-python
# --------------------------------------------------------------------------

class ArchetypesType():
    """
    Enumeration for archetypes' types.
    """
    PROJECTS  = 'projects'
    DOCUMENTS = 'documents'
    OBJECTS   = 'objects'

# --------------------------------------------------------------------------
# Class: ArchetypeManager
# Description: Class for managing PROTEUS archetypes
# Date: 19/09/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

# TODO: poner métodos como @classmethod

class ArchetypeManager:
    """
    An utility class for managing PROTEUS archetypes. It must provide a way
    to get the project, document, and object archetypes on demand.
    TODO: in the future, it will also be responsible for adding new archetypes.
    """

    # ----------------------------------------------------------------------
    # Method: load_object_archetypes (static)
    # Description: It load object archetypes
    # Date: 19/09/2022
    # Version: 0.1
    # Author: Pablo Rivera Jiménez
    # ----------------------------------------------------------------------

    @classmethod
    def load_object_archetypes( cls ) -> list:
        """
        Method that loads the object archetypes.
        :return: A list of ObjectArchetypeProxy objects.
        """
        log.info('ArchetypeManager - load object archetypes')
        # Build archetypes directory name from archetype type
        archetypes_dir : str = join(ARCHETYPES_FOLDER, ArchetypesType.OBJECTS)

        # Scan all the subdirectories in the archetypes directory (one depth level only)
        # TODO: this means that ALL archetypes must be in one subdirectory, i.e., that
        #       no archetypes are supposed to be in the root directory, AND that only one
        #       level of subdirectories is allowed.
        subdirs : list[str] = [f for f in listdir(archetypes_dir) if isdir(join(archetypes_dir, f))]
        
        # Result as a list of pairs (path,name) <-- is that enough?
        # TODO: check the possibility of using proxy classes
        result : list[ObjectArchetypeProxy] = list ()

        # For each subdirectory
        for subdir in subdirs:
            # Variable were it's going to be saved the data of each object
            object_dicc : dict = dict()

            # Build the full path to the subdirectory
            subdir_path : str = join(archetypes_dir, subdir)

            # We get all the XML files in the subdirectory
            archetype_files : list[str] = [f for f in listdir(subdir_path) if (isfile(join(subdir_path, f)) and f.endswith('.xml'))]

            # For each archetype file, we add it to the result
            for archetype_file in archetype_files:
                archetype_file_path = join(subdir_path, archetype_file)

                # We parse the root element
                object : ET.Element = ET.parse(archetype_file_path)
                
                # We get the root
                root_object = object.getroot()

                #We get id, class, path, acceptedChildren and name
                object_dicc["id"] = root_object.attrib["id"]
                object_dicc["classes"] = root_object.attrib["classes"]
                object_dicc["acceptedChildren"] = root_object.attrib["acceptedChildren"]
                object_dicc["path"] = archetype_file_path
                object_dicc["name"] = archetype_file

            result.append(ObjectArchetypeProxy(object_dicc))
        return result


    # ----------------------------------------------------------------------
    # Method: load_document_archetypes (static)
    # Description: It load document archetypes
    # Date: 19/09/2022
    # Version: 0.1
    # Author: Pablo Rivera Jiménez
    # ----------------------------------------------------------------------

    @classmethod
    def load_document_archetypes( cls ) -> dict:
        """
        Method that loads the document archetypes.
        :return: A dict of project document name and DocumentArchetypeProxy objects.
        """
        log.info('ArchetypeManager - load document archetypes')
        # Build archetypes directory name from archetype type
        archetypes_dir : str = join(ARCHETYPES_FOLDER, ArchetypesType.DOCUMENTS)

        # Scan all the subdirectories in the archetypes directory (one depth level only)
        # TODO: this means that ALL archetypes must be in one subdirectory, i.e., that
        #       no archetypes are supposed to be in the root directory, AND that only one
        #       level of subdirectories is allowed.
        subdirs : list[str] = [f for f in listdir(archetypes_dir) if isdir(join(archetypes_dir, f))]
        
        # Result as a list of pairs (path,name) <-- is that enough?
        # TODO: check the possibility of using proxy classes
        result : dict[str, DocumentArchetypeProxy] = dict ()

        # For each subdirectory
        for subdir in subdirs:
            # Variable were it's going to be saved the data of each document
            document_dicc : dict = dict()
            
            # Build the full path to the subdirectory
            subdir_path : str = join(archetypes_dir, subdir)

            # We get all the XML files in the subdirectory
            archetype_files : list[str] = [f for f in listdir(subdir_path) if (isfile(join(subdir_path, f)) and f.endswith('.xml'))]

            # For each archetype file
            for archetype_file in archetype_files:
                archetype_file_path = join(subdir_path, archetype_file)

                # We get the file "document.xml", we find inside it the id that
                # referes to the main document (the one with class ':Proteus-document'), and we
                # add it to the result list
                if( archetype_file == 'document.xml' ):
                    # Parse the XML file
                    file_subdir : ET.Element = ET.parse(archetype_file_path)

                    # Get the id of the root document from document.xml
                    id : str = file_subdir.getroot().attrib["id"]

                    # Build the path to the root document
                    objects_path = join(subdir_path, "objects")
                    document_root_path = join(objects_path, id + ".xml")
                    
                    # We parse the root element
                    document : ET.Element = ET.parse(document_root_path)

                    # We get the root
                    root_document = document.getroot()

                    # We get the properties and save the id & path
                    properties_element : ET.Element = root_document.find(PROPERTIES_TAG)
                    

                    # TODO en caso de que queramos usar el mismo documento varias veces, tenemos que cambiarle el id ?
                    document_dicc["id"] = id
                    document_dicc["path"] = document_root_path
                    document_dicc["classes"] = root_document.attrib["classes"]
                    document_dicc["acceptedChildren"] = root_document.attrib["acceptedChildren"]

                    # For each element in the properties, we create an instance of the property
                    # Using the PropertyFactory and if the name of the property is "name"
                    # or description we add it to the data of the document with their associated value
                    for element in properties_element:
                        property = PropertyFactory.create(element)
                        property_name : str = property.name
                        if(property_name in DOCUMENT_PROPERTIES_TO_SAVE):
                            document_dicc[property_name] = property.value
                    result[subdir] = DocumentArchetypeProxy(document_dicc)
        return result


    # ----------------------------------------------------------------------
    # Method: load_project_archetypes (static)
    # Description: It load project archetypes
    # Date: 19/09/2022
    # Version: 0.1
    # Author: Pablo Rivera Jiménez
    # ----------------------------------------------------------------------

    @classmethod
    def load_project_archetypes( cls ) -> list:
        """
        Method that loads the project archetypes.
        :return: A list of ProjectArchetypeProxy objects.
        """
        log.info('ArchetypeManager - load project archetypes')
        # Build archetypes directory name from archetype type (project)
        archetypes_dir : str = join(ARCHETYPES_FOLDER, ArchetypesType.PROJECTS)

        # Scan all the subdirectories in the archetypes directory (one depth level only)
        # TODO: this means that ALL archetypes must be in one subdirectory, i.e., that
        #       no archetypes are supposed to be in the root directory, AND that only one
        #       level of subdirectories is allowed.
        subdirs : list[str] = [f for f in listdir(archetypes_dir) if isdir(join(archetypes_dir, f))]
        
        # Result as a list of pairs (path,name) <-- is that enough?
        # TODO: check the possibility of using proxy classes
        result : list [ProjectArchetypeProxy] = []

        # For each subdirectory
        for subdir in subdirs:

            # Variable were it's going to be saved the data of each project
            project_dicc : dict = dict()

            # Build the full path to the subdirectory
            subdir_path : str = join(archetypes_dir, subdir)

            # We get all the XML files in the subdirectory
            archetype_files : list[str] = [f for f in listdir(subdir_path) if (isfile(join(subdir_path, f)) and f.endswith('.xml'))]
            
            # For each archetype file,we get the project main file
            for archetype_file in archetype_files:
                archetype_file_path = join(subdir_path, archetype_file)
                
                # We parse the path into lxml element
                subdir : ET.Element = ET.parse(archetype_file_path)

                # We get the root
                root = subdir.getroot()

                # Get the id
                id : str = root.attrib["id"]

                # Find all properties and set into the project dicc the id & path
                properties_element : ET.Element = root.find(PROPERTIES_TAG)
                project_dicc["id"] = id
                project_dicc["path"] = archetype_file_path

                # For each element in the properties, we get the property and if it's name
                # or description we add it to the result with the associated value
                for element in properties_element:
                    property = PropertyFactory.create(element)
                    property_name : str = property.name
                    if(property_name in PROJECT_PROPERTIES_TO_SAVE):
                        project_dicc[property_name] = property.value
            result.append(ProjectArchetypeProxy(project_dicc))
        return result


    
    # ----------------------------------------------------------------------
    # Method     : clone_project
    # Description: It clones a project archetype into the sys path wanted.
    # Date       : 27/09/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    @staticmethod
    def clone_project(archetype_path: str, filename_path_to_save: str):
        """
        Method that creates a new project from an archetype.
        :param filename: Path where we want to save the project.
        :param archetype: Archetype type.
        """
        
        # Directory where we save the project
        path = os.path.realpath(filename_path_to_save)
        
        # Directory where is the archetype
        archetype_dir = os.path.dirname(archetype_path)

        # Copy the archetype to the project directory
        original = archetype_path
        target = path
        shutil.copy(original, target)
        
        # In case there is no directory, create it
        if "assets" not in os.listdir(path):
            shutil.copytree(join(archetype_dir, "assets"), join(path, "assets"))

        # Copy the objects file from the archetypes directory into the project directory
        source_dir = join(archetype_dir, "objects")
        destination_dir = join(path, "objects")
        
        shutil.copytree(source_dir, destination_dir)