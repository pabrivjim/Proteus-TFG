# ==========================================================================
# File: __init__.py
# Description: PROTEUS persistence package initializer
# Date: 25/08/2022
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================

from os import listdir, mkdir
from os.path import dirname, isfile, join
from re import T
from lxml import etree as ET
from lxml import html
import os
from proteus.controllers.save_state_machine import SaveMachine, set_all_states_clean
from proteus.controllers.save_state_machine import States
from proteus.controllers.incoming_traces import IncomingTraces
from proteus.utils.model.nodes_utils import get_node
from .converter import dict2xml, xml2dict
import proteus
import proteus.utils.config as config
import shutil

def load_objects(path: str, clean=False) -> dict:
    """
    Method that loads objects.

    :param path
    """
    proteus.logger.info('persistence init - load object')

    res = {}
    print(path)
    project_dir = dirname(path)
    files = [f for f in listdir(join(project_dir, "objects")) if isfile(join(project_dir, "objects", f))]
    for obj in files:
        if(str(obj[-3:]) == "xml"):
            o = ET.parse(join(project_dir, "objects", obj))
            o_root = o.getroot()
            o_id = o_root.attrib["id"]
            res[o_id] = xml2dict(o_root)
            if(res[o_id]["traces"]):
                for element in res[o_id]["traces"]:
                    trace = IncomingTraces(element["id"])
                    trace.add_trace(res[o_id]["id"])

            obj = SaveMachine(res[o_id]["id"])
            if clean:    
                obj.set_state(States.CLEAN)
            else:
                obj.set_state(States.FRESH)
            

    return res

def load_project(path, clean=False) -> dict:
    """
    Methods that load project.

    :param path:
    :return project
    """
    proteus.logger.info('persistence init - load project')

    root = ET.parse(path).getroot()
    obj = SaveMachine(root.attrib.get("id"))
    if clean:    
        obj.set_state(States.CLEAN)
    else:
        obj.set_state(States.FRESH)

    project = {
        "id": root.attrib.get("id"),
        "documents": [document.attrib.get("id") for document in root.find("documents")],
    }

    properties = {}
    for prop in root.find("properties"):
        properties[prop.attrib["name"]] = {
            "type": prop.tag,
            "value": prop.text,
            "category": prop.attrib.get("category", "")
        }
    project["properties"] = properties

    objects = load_objects(path, clean)
    for _, value in objects.items():
        value["children"] = list(
            map(lambda o: objects[o], value["children"]))

    return {
        **project,
        "documents": list(map(lambda o: objects[o], project["documents"]))
    }

def save_existing_project(filename, project) -> None:
    """
    Method that saves an existing project.

    :param: filename
    :param: project
    """
    proteus.logger.info('persistence init - save project')
    
    p = {
        "project": project["id"],
        "properties": project["properties"],
        "documents": list(map(lambda d: d["id"], project["documents"]))
    }
    objects = []

    # We get all the objects of a doc and if the object is dirty or has been
    # Delete, we added to our list of objects to save
    def get_objects(nodes, res):
        for node in nodes:
            obj = SaveMachine(node["id"])
            if(obj.is_dirty() or obj.is_deleted() or obj.is_fresh()):
                res.append(dict2xml(node))
            get_objects(node["children"], res)


    # For each document, we do the same as we did with object,
    # if its dirty or has been deleted, we add it to our list of objects to save
    for document in project["documents"]:
        obj = SaveMachine(document["id"])
        if(obj.is_dirty() or obj.is_deleted()):
            objects.append(dict2xml(document))
        get_objects(document["children"], objects)

    # Directory where we save the project
    to_dir = dirname(filename)


    project_obj = SaveMachine(project["id"])
    
    # If the project is dirty or has been deleted, we save it
    if(project_obj.is_dirty() or project_obj.is_deleted()):
        # # Save project file
        with open(filename, "w") as outfile:
            project = ET.Element("project")
            project.set("id", p["project"])
            properties = ET.SubElement(project, "properties")
            documents = ET.SubElement(project, "documents")

            for name, val in p["properties"].items():
                prop = ET.SubElement(properties, val["type"])
                prop.set("name", name)

                if "category" in val:
                    prop.set("category", val["category"])

                if "value" in val and val["value"]:
                    prop.text = val["value"]

            for doc in p["documents"]:
                document = ET.SubElement(documents, "document")
                document.set("id", doc)

            ET.indent(project)
            outfile.write(ET.tostring(project).decode())

    # We save the objects
    obj: ET.Element
    for obj in objects:
        # doc = ET.parse(obj)
        tree = obj.getroottree()
        with open(join(to_dir, "objects", ".".join((obj.attrib["id"], "xml"))), "wb") as outfile:
            # outfile.write(ET.tostring(obj).decode())
            tree.write(outfile, xml_declaration=True, encoding='utf-8')
    
    # At the end we set everything to clean
    set_all_states_clean()

# TODO REMOVE 
def clone_project_archetype(filename: str, archetype: str) -> None:
    """
    Method that creates a new project from an archetype.

    :param filename: Path where we want to save the project.
    :param archetype: Archetype type.
    """
    print("filename: ",filename)
    # Directory where we save the project
    path = os.path.dirname(os.path.realpath(filename))
    print("path: ",path)

    # Directory where is the archetype
    archetype_dir = f"{config.ARCHETYPES_FOLDER}/projects/{archetype}"

    # Copy the archetype to the project directory
    original = archetype_dir + "/project.xml"
    target = filename
    shutil.copyfile(original, target)

    # In case there is no directory, create it
    if "assets" not in os.listdir(os.path.dirname(filename)):
        mkdir(join(path, "assets"))
    
    # Copy the objects file from the archetypes directory into the project directory   
    source_dir = join(archetype_dir, "objects")
    destination_dir = join(path, "objects")
    shutil.copytree(source_dir, destination_dir)

#OLD code, not used anymore, that saved the project loaded in memory.
def save_project(filename, project) -> None:
    """
    method that saves a non-existent project.

    :param: filename
    :param: project
    """
    proteus.logger.info('persistence init - save project')
    
    p = {
        "project": project["id"],
        "properties": project["properties"],
        "documents": list(map(lambda d: d["id"], project["documents"]))
    }
    objects = []

    # We get all the objects of a doc and we add them to our list of objects to save
    def get_objects(nodes, res):
        for node in nodes:
            res.append(dict2xml(node))
            get_objects(node["children"], res)

    # The same as we did with objects, we add the documents to our list of objects to save
    for document in project["documents"]:
        objects.append(dict2xml(document))
        get_objects(document["children"], objects)

    # Reset dir
    to_dir = dirname(filename)
    

    # In case there is no directory, create it
    if "objects" not in os.listdir(os.path.dirname(filename)):
        mkdir(join(to_dir, "objects"))

    # Save project file
    with open(filename, "w") as outfile:
        project = ET.Element("project")
        project.set("id", p["project"])
        properties = ET.SubElement(project, "properties")
        documents = ET.SubElement(project, "documents")

        for name, val in p["properties"].items():
            prop = ET.SubElement(properties, val["type"])
            prop.set("name", name)
           



            if "category" in val:
                prop.set("category", val["category"])

            if "value" in val and val["value"]:
                prop.text = val["value"]

        for doc in p["documents"]:
            document = ET.SubElement(documents, "document")
            document.set("id", doc)

        ET.indent(project)
        outfile.write(ET.tostring(project).decode())

    # We save the objects
    for obj in objects:
        with open(join(to_dir, "objects", ".".join((obj.attrib["id"], "xml"))), "w") as outfile:
            outfile.write(ET.tostring(obj).decode())
    
    # At the end we set everything to clean
    set_all_states_clean()


def get_project_objects(project) -> list:
    """
    Method that get objects from a project.

    :param project:
    :return: objects
    """
    proteus.logger.info('persistence init - get project objects')
    
    objects = []

    def get_objects(nodes, res):
        for node in nodes:
            res.append(node)
            get_objects(node["children"], res)
            
    for document in project["documents"]:
        get_objects(document["children"], objects)

    return objects