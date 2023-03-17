# ==========================================================================
# File: __init__.py
# Description: PROTEUS config package initializer
# Date: 25/08/2022
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================

from os import listdir
from os.path import join, dirname, abspath, isfile, exists
from os import pardir
from lxml import etree as ET
from ..persistence.converter import xml2dict
import proteus
from datetime import datetime

CURRENT_FOLDER = dirname(dirname(__file__))
PARENT_FOLDER =  abspath(join(CURRENT_FOLDER, pardir))
RESOURCES_FOLDER = join(PARENT_FOLDER, 'resources')
CONFIG_FOLDER = join(PARENT_FOLDER, 'resources\config')
ARCHETYPES_FOLDER = join(abspath(join(PARENT_FOLDER, pardir)), 'archetypes')

# Generate different names from the current date and time
logging_file_name = str(datetime.now()).replace(":", "-")
LOGGING_FILE = join(abspath(join(PARENT_FOLDER, pardir)), "tmp/"+ logging_file_name + ".log")




class Config:
    """
    Class that loads archetypes and other config files.
    """

    @staticmethod
    def load_object_archetypes() -> dict:
        """
        Method that loads the object archetypes.
        """
        print("Load objects Archetypes")
        proteus.logger.info('Config - load object archetypes')
        archetypes_dir = join(ARCHETYPES_FOLDER, "objects")
        categories = [f for f in listdir(archetypes_dir) if not isfile(join(archetypes_dir, f))]
        res = {}

        for category in categories:
            res[category] = {}
            archetypes = [f for f in listdir(join(archetypes_dir, category)) if
                          isfile(join(archetypes_dir, category, f))]

            for arch in archetypes:
                o = ET.parse(join(archetypes_dir, category, arch))
                o_root = o.getroot()
                obj = xml2dict(o_root)
                klass = obj["classes"][len(obj["classes"]) - 1]
                res[category][klass] = res[category].get(klass, []) + [obj]

        return res

    @staticmethod
    def load_document_archetypes() -> list:
        """
        Method that loads the document archetypes.
        """
        print("Load DOCS Archetypes")
        proteus.logger.info('Config - load document archetypes')
        archetypes_dir = join(ARCHETYPES_FOLDER, "documents")
        return [f for f in listdir(archetypes_dir) if not isfile(join(archetypes_dir, f))]

    @staticmethod
    def load_project_archetypes() -> list:
        """
        Method that loads the project archetypes.
        """
        proteus.logger.info('Config - load project archetypes')
        archetypes_dir = join(ARCHETYPES_FOLDER, "projects")
        return [f for f in listdir(archetypes_dir) if not isfile(join(archetypes_dir, f))]

    @staticmethod
    def load_views() -> list:
        """
        Method that loads the views.
        """
        proteus.logger.info('Config - load views')
        views_dir = join(CONFIG_FOLDER, "views")
        views = [f for f in listdir(views_dir) if not isfile(join(views_dir, f))]
        # Todo refactor
        res = []
        for view in views:
            if exists(join(views_dir, view, "index.html")):
                res.append({"type": "html", "path": join(views_dir, view, "index.html")})
            else:
                res.append({"type": "xslt", "path": join(views_dir, view, "main.xslt")})

        return res

    @staticmethod
    def get_views_folder() -> str:
        """
        Method that returns the views folder.
        """
        proteus.logger.info('Config - get views folder')
        return join(CONFIG_FOLDER, "views")
