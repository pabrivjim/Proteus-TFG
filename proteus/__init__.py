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

# --------------------------------------------------------------------------
# Constant declarations for PROTEUS logger name
# --------------------------------------------------------------------------

PROTEUS_LOGGER_NAME    = str('proteus')
PROTEUS_LOGGING_FORMAT = str('%(name)s:%(filename)s [%(levelname)s] -> %(message)s')

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
    #filename=PROTEUS_LOGGER_NAME+'.log',
    #filemode='a',    
    level=logging.DEBUG, 
    format=PROTEUS_LOGGING_FORMAT
)

logger = logging.getLogger(PROTEUS_LOGGER_NAME)