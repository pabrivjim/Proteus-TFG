"""
Pytest file for the PROTEUS application directories.
"""
# ==========================================================================
# File: test_directories.py
# Description: pytest file for the PROTEUS application directories
# Date: 10/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Project specific imports
# --------------------------------------------------------------------------
from configparser import ConfigParser
from pathlib import Path
from proteus.config import ARCHETYPES_CUSTOM_DIRECTORY, DIRECTORIES, XSLT_CUSTOM_FILE, Config
import pytest

from proteus.tests import PATH
# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

# https://stackoverflow.com/questions/62044541/change-pytest-working-directory-to-test-case-directory
# Because the file proteus.ini is not in the same folder as the test, we need to change the working directory
@pytest.fixture
def base_path() -> Path:
    """Get directory of proteus.ini"""
    return PATH

def test_application_directories(base_path: Path, monkeypatch: pytest.MonkeyPatch):
    """
    It tests that essential PROTEUS directories exist.
    """
    monkeypatch.chdir(base_path)
    app : Config = Config()
    assert app.resources_directory.is_dir()
    assert app.icons_directory.is_dir()
    assert app.archetypes_directory.is_dir()

    # Check the custom directories
    filename = str(app.config_file)
    parser = ConfigParser()
    parser.read(filename)

    # If the XSLT_CUSTOM_FILE exists, then the path of the XSLT_CUSTOM_FILE must be the same as the one in the config file
    # Otherwise, the XSLT_CUSTOM_FILE must not exist in the config file
    if (app.xslt_custom_file != None):
        assert str(parser[DIRECTORIES][XSLT_CUSTOM_FILE]) == str(app.xslt_custom_file)
    else:
        assert parser.has_option(DIRECTORIES, XSLT_CUSTOM_FILE) == False

    # If the ARCHETYPES_CUSTOM_DIRECTORY exists, then the path of the ARCHETYPES_CUSTOM_DIRECTORY must be the same as the one in the config file
    # Otherwise, the ARCHETYPES_CUSTOM_DIRECTORY must not exist in the config file
    if (app.archetypes_custom_directory != None):
        assert str(parser[DIRECTORIES][ARCHETYPES_CUSTOM_DIRECTORY]) == str(app.archetypes_custom_directory)
    else:
        assert parser.has_option(DIRECTORIES, ARCHETYPES_CUSTOM_DIRECTORY) == False
