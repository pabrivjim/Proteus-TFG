"""
Pytest file for the PROTEUS ArchetypeManager.
"""
# ==========================================================================
# File: test_archetype_manager.py
# Description: pytest file for the PROTEUS ArchetypeManager
# Date: 20/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import os
import pathlib
import shutil


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------

from proteus.config import Config
from proteus.model.archetype_manager import ArchetypeManager
from proteus.model.archetype_proxys import DocumentArchetypeProxy, ObjectArchetypeProxy, ProjectArchetypeProxy
from proteus.model.object import Object
from proteus.model.project import Project

# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------
app : Config = Config()
test_project : Project = Project.load(app.base_directory / "tests" / "project")


def test_project_archetype_manager():
    """
    Test the project archetype manager.
    """
    # Get the number of projects in archetypes projects
    dir_path = str(app.archetypes_directory / "projects")
    number_of_projects = len(os.listdir(dir_path))

    # Check if load project function return all the projects
    projects = ArchetypeManager.load_project_archetypes()
    assert len(projects) == number_of_projects

    # Check if the project is a ProjectArchetypeProxy and has all the attributes
    for _, project_arch in projects.items():
        assert all(x for x in [isinstance(project_arch, ProjectArchetypeProxy),
                               project_arch.path, project_arch.id, project_arch.name, project_arch.description,
                               project_arch.author, project_arch.date])
        
        # Check we can get an instance of the project.
        project = project_arch.get_project()
        assert isinstance(project, Project)

        # Get each project folder and their files
        project_dir = os.path.dirname(project_arch.path)
        project_files = [file for file in os.listdir(project_dir)]

        # Check if the project has assets and objects
        assert  all(elem in project_files for elem in ["assets", "objects"])

        # Check if the project has at least one .xml file (the project file)
        assert len([x for x in project_files if x.endswith('.xml')]) >= 1
            
            
def test_document_archetype_manager():
    """
    Test the document archetype manager.
    """
    # Get the number of documents in archetypes documents
    dir_path = str(app.archetypes_directory / "documents")
    number_of_documents = len(os.listdir(dir_path))

    # Check if load document function return all the documents
    documents = ArchetypeManager.load_document_archetypes()
    assert len(documents) == number_of_documents

    # Check if the document is a DocumentArchetypeProxy and has all the attributes
    for _, document_arch in documents.items():
        assert all(x for x in [isinstance(document_arch, DocumentArchetypeProxy),
                               document_arch.path, document_arch.id, document_arch.name, document_arch.description,
                               document_arch.author, document_arch.date, document_arch.classes, document_arch.acceptedChildren])
        
        # Check we can get an instance of the document.
        document = document_arch.get_document(test_project)
        assert isinstance(document, Object)

        # Get each document folder and their files
        document_dir = os.path.dirname(os.path.dirname(document_arch.path))
        document_files = [file for file in os.listdir(document_dir)]

        # Check if the document has assets and objects
        assert all(elem in document_files for elem in ["assets", "objects"])

        # Check if the document archetype has a document.xml file
        assert len([x for x in document_files if (x == "document.xml")]) == 1

def test_object_archetype_manager():
    """
    Test the document archetype manager.
    """
    # Get the number of objects in archetypes objects
    dir_path = str(app.archetypes_directory / "objects")
    number_of_type_of_objects = len(os.listdir(dir_path))

    # Check if load object function return all the objects
    objects = ArchetypeManager.load_object_archetypes()
    assert len(objects) == number_of_type_of_objects


    # Check if the object is a ObjectArchetypeProxy and has all the attributes
    for _, object_arch_list in objects.items():
        object_arch: ObjectArchetypeProxy
        for object_arch in object_arch_list:
            assert all(x for x in [isinstance(object_arch, ObjectArchetypeProxy),
                                object_arch.path, object_arch.id, object_arch.name, object_arch.classes,
                                object_arch.acceptedChildren])
            
            # Check we can get an instance of the Object.
            object = object_arch.get_object(test_project)
            assert isinstance(object, Object)

            # Get each object type folder and their files
            object_dir = os.path.dirname(object_arch.path)
            object_files = [file for file in os.listdir(object_dir)]

            # Check if all the files inside each object type folder are .xml files
            assert len([x for x in object_files if (x.endswith(".xml")) ]) == len(object_files)

def test_clone_project():
    """
    Test the clone project function.
    """
    # Get the archetypes projects and select the first one
    projects = ArchetypeManager.load_project_archetypes()
    project_archetype_name: str =  list(projects.keys())[0]
    project_to_be_cloned : ProjectArchetypeProxy = projects[project_archetype_name]

    # New path where we want to clone the archetype
    new_cloned_project_path = pathlib.Path.cwd() / "proteus" / "tests" / "new_cloned_project"
    # If dir already exists, then we remove it
    if(new_cloned_project_path.resolve().exists()):
        shutil.rmtree(new_cloned_project_path)

    # Create a dir
    os.mkdir(new_cloned_project_path)

    # Archetype path
    project_to_be_cloned_path = pathlib.Path(project_to_be_cloned.path)

    # Clone project
    ArchetypeManager.clone_project(project_to_be_cloned_path,new_cloned_project_path.resolve())
    
    # Check everything was copied (.xml main file, assets folder and objects folder)
    assert(os.listdir(project_to_be_cloned_path.parent) == os.listdir( new_cloned_project_path))
    assert(os.listdir(project_to_be_cloned_path.parent / "objects") == os.listdir( new_cloned_project_path/ "objects"))
    assert(os.listdir(project_to_be_cloned_path.parent / "assets") == os.listdir( new_cloned_project_path/ "assets"))

    # We remove the dir
    shutil.rmtree(new_cloned_project_path)
