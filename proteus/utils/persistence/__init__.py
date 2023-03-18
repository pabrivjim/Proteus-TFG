# ==========================================================================
# File: __init__.py
# Description: PROTEUS persistence package initializer
# Date: 25/08/2022
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import proteus



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