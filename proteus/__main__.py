# ==========================================================================
# File: main.py
# Description: File where the main application is defined.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import os
import sys
import unittest
from PyQt5.QtCore import (QTranslator, QSettings)
from PyQt5.QtGui import QGuiApplication, QIcon
from PyQt5.QtWidgets import QApplication
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from proteus.utils.config import Config, CONFIG_FOLDER, PARENT_FOLDER
from proteus.view.main_window import MainWindow
import logging
from proteus.utils.config import LOGGING_FILE
from importlib import reload

#https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
import ctypes
myappid = 'US.proteus.1.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class ViewUpdateHandler(FileSystemEventHandler):
    """
    Update views on view code update (proteus views folder).
    The purpouse of this function is to debug.
    """

    def on_modified(self, event):
        main_window.update_view.emit()


class AutoRestartHandler(FileSystemEventHandler):
    """
    Update program on code update.
    The purpouse of this function is to debug.
    """

    def on_modified(self, event):
        os.execl(sys.executable, sys.executable, *sys.argv)


if __name__ == '__main__':
    
    # https://stackoverflow.com/questions/12011091/trying-to-implement-python-testsuite
    # test_suite = unittest.TestSuite()
    # test_suite.addTest(unittest.makeSuite(TestUtils))
    # mySuit=test_suite

    # runner=unittest.TextTestRunner(failfast=True)
    # runner.run(mySuit)

    # https://stackoverflow.com/questions/31169540/python-logging-not-saving-to-file
    reload(logging)
    
    # autodelete https://stackoverflow.com/questions/43947206/automatically-delete-old-python-log-files
    logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
      filename=LOGGING_FILE,
      filemode='w')
    
    logging.info('Init App')
    # If is set to True QThreads errors could appear
    debug = False

    #https://stackoverflow.com/questions/46653337/using-a-local-file-in-html-for-a-pyqt5-webengine
    sys.argv.append("--disable-web-security")
    print(sys.argv)
    app = QApplication(sys.argv)

    # Set language
    settings = QSettings("Proteus", "SettingsDesktop")
    language = settings.value("language", "en_EN")
    translation = f"{language}.qm"
    translator = QTranslator()
    translator.load(translation, f"{CONFIG_FOLDER}/i18n/")
    app.installTranslator(translator)

    app.setWindowIcon(QIcon(f'{PARENT_FOLDER}/icons/proteus_logo.png'))

    main_window = MainWindow()
    main_window.resize(1024, 768)
    main_window.show()

    observer = Observer()
    observer.schedule(ViewUpdateHandler(), Config.get_views_folder(),
                      recursive=True)
    if debug:
        observer.schedule(AutoRestartHandler(),
                          os.path.dirname(os.path.realpath(__file__)),
                          recursive=True)
        screens = QGuiApplication.screens()
        if len(screens) > 1:
            target_screen = 0
            frameGm = main_window.frameGeometry()
            screen = QGuiApplication.screens()[target_screen]
            centerPoint = screen.geometry().center()
            frameGm.moveCenter(centerPoint)
            main_window.move(frameGm.topLeft())

    observer.start()
    status = app.exec()
    observer.stop()
    observer.join()
    sys.exit(status)
