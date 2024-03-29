"""
PROTEUS archetype proxy.
"""
# ==========================================================================
# File: archetype_proxys.py
# Description: PROTEUS archetype proxy
# Date: 07/10/2022
# Version: 0.2
# Author: Pablo Rivera Jiménez
# ==========================================================================

# Avoid circle import
from __future__ import annotations

import datetime
import proteus.model.object as object
import proteus.model.project as project


# --------------------------------------------------------------------------
# Class: ProjectArchetypeProxy
# Description: Proxy class for managing PROTEUS project archetypes.
# Date: 07/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class ProjectArchetypeProxy:
    """
    Proxy class for managing PROTEUS project archetypes.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a ProjectArchetypeProxy object.
    # Date       : 07/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    def __init__(self, data : dict):
        """
        It initializes a ProjectArchetypeProxy object.

        :param data: Dictionary with the data of the project.
        """

        self.path : str = data["path"]
        self.id : str = data["id"]
        self.name : str = data["name"]
        self.description : str = data["description"]
        self.author : str = data["author"]
        self.date : datetime = data["date"]

    # ----------------------------------------------------------------------
    # Method     : get_project
    # Description: It returns an instance of a project.
    # Date       : 07/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    def get_project(self) -> project.Project:
        """
        It returns an instance of a project.

        :returns: Instance of a Project.
        :rtype: project.Project
        """
        return project.Project(self.path)


# --------------------------------------------------------------------------
# Class: DocumentArchetypeProxy
# Description: Proxy class for managing PROTEUS archetypes
# Date: 08/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class DocumentArchetypeProxy:
    """
    Proxy class for managing PROTEUS document archetypes.
    """
    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a DocumentArchetypeProxy object.
    # Date       : 08/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    def __init__(self, data : dict):
        """
        It initializes a DocumentArchetypeProxy object.

        :param data: Dictionary with the data of the document.
        """
        self.path : str = data["path"]
        self.id : str = data["id"]
        self.name : str = data["name"]
        self.description : str = data["description"]
        self.author : str = data["author"]
        self.date : datetime = data["date"]
        self.classes : str = data["classes"]
        self.acceptedChildren : str = data["acceptedChildren"]

    # ----------------------------------------------------------------------
    # Method     : get_document
    # Description: It returns an instance of a object.
    # Date       : 08/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # # ----------------------------------------------------------------------
    def get_document(self, project: project.Project) -> object.Object:
        """
        It returns an instance of a object.

        :param project: Project where the object is located.
        :return: Instance of an object.
        :rtype: object.Object
        """
        return object.Object(project, self.path, is_document_proxy_archetype=True)


# --------------------------------------------------------------------------
# Class: ObjectArchetypeProxy
# Description: Proxy class for managing PROTEUS object archetypes
# Date: 20/10/2022
# Version: 0.1
# Author: Pablo Rivera Jiménez
# --------------------------------------------------------------------------

class ObjectArchetypeProxy:
    """
    Proxy class for managing PROTEUS object archetypes.
    """

    # ----------------------------------------------------------------------
    # Method     : __init__
    # Description: It initializes a ObjectrchetypeProxy object.
    # Date       : 20/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # ----------------------------------------------------------------------
    def __init__(self, data : dict):
        """
        It initializes a ObjectArchetypeProxy object.

        :param data: Dictionary with the data of the object.
        """
        self.path : str = data["path"]
        self.id : str = data["id"]
        self.name : str = data["name"]
        self.classes : str = data["classes"]
        self.acceptedChildren : str = data["acceptedChildren"]

    # ----------------------------------------------------------------------
    # Method     : get_project
    # Description: It returns an instance of a object.
    # Date       : 08/10/2022
    # Version    : 0.1
    # Author     : Pablo Rivera Jiménez
    # # ----------------------------------------------------------------------
    def get_object(self, project: project.Project) -> object.Object:
        """
        It returns an instance of a object.

        :param project: Project where the object is located.
        :return: Instance of an object.
        :rtype: object.Object
        """
        return object.Object(project, self.path)
