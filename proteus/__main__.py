"""
File where the entry point for the PROTEUS application is defined.
"""
# ==========================================================================
# File: __main__.py
# Description: File where the entry point for the PROTEUS application is defined
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================

#https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
import ctypes
import sys
import os
myappid = 'US.proteus.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

# This is need to import the proteus package. If we run with -m or not it will works the same.
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_dir)
os.chdir(project_dir)

from proteus.app import ProteusApplication

# --------------------------------------------------------------------------
# Function: main
# Description: Entry point for the PROTEUS application
# Date: 09/10/2022
# Version: 0.1
# Author: Amador Durán Toro
# --------------------------------------------------------------------------

def main() -> int:
    """
    It runs the PROTEUS application.
    :return: the status of the application
    :rtype: int
    """
    print("="*40)
    print("PROTEUS application 0.1")
    print("="*40)

    app = ProteusApplication()
    return app.run()

if __name__ == '__main__':
    status = main()
    sys.exit(status)