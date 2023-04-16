# ==========================================================================
# File: __init__.py
# Description: module initialization for the PROTEUS application
# Date: 25/08/2022
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================

# --------------------------------------------------------------------------
# Standard library imports
# --------------------------------------------------------------------------

import logging
from pathlib import Path
from datetime import datetime
# --------------------------------------------------------------------------
# Constant declarations for PROTEUS logger name
# --------------------------------------------------------------------------

PROTEUS_LOGGER_NAME    = str('proteus')
PROTEUS_LOGGING_FORMAT = str('%(name)s:%(filename)s [%(levelname)s] -> %(message)s')

# --------------------------------------------------------------------------
# Get the parent of the parent of this file (.../PROTEUS TFG) and the path to
# the temporary file where the loggings will be saved.
# --------------------------------------------------------------------------
tmp_folder = Path(__file__).parent.parent.absolute() / 'tmp'

# --------------------------------------------------------------------------
# Create tmp directory if it does not exist
# --------------------------------------------------------------------------

Path(tmp_folder).mkdir(parents=True, exist_ok=True)

# --------------------------------------------------------------------------
# Create each logging file with the current date and time
# --------------------------------------------------------------------------

logging_file_name = str(datetime.now()).replace(":", "-")
logging_file_path = tmp_folder / (logging_file_name + '.log')

# --------------------------------------------------------------------------
# Logger configuration
# --------------------------------------------------------------------------

# logging levels =
#   NOTSET=0
#   DEBUG=10
#   INFO=20
#   WARN=30
#   ERROR=40
#   CRITICAL=50

logging.basicConfig(
    filename=logging_file_path,
    filemode='w',
    level=logging.DEBUG,
    format=PROTEUS_LOGGING_FORMAT
)

logger = logging.getLogger(PROTEUS_LOGGER_NAME)