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
from pathlib import Path
from proteus.config import Config
import pytest
# --------------------------------------------------------------------------
# Tests
# --------------------------------------------------------------------------

# https://stackoverflow.com/questions/62044541/change-pytest-working-directory-to-test-case-directory
# Because the file proteus.ini is not in the same folder as the test, we need to change the working directory
@pytest.fixture
def base_path() -> Path:
    """Get directory of proteus.ini"""
    return Path(__file__).parent.parent.parent

def test_application_directories(base_path: Path, monkeypatch: pytest.MonkeyPatch):
    """
    It tests that essential PROTEUS directories exist.
    """
    monkeypatch.chdir(base_path)
    app : Config = Config()
    assert app.resources_directory.is_dir()
    assert app.icons_directory.is_dir()
    assert app.archetypes_directory.is_dir()
