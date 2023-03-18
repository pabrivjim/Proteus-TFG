# ==========================================================================
# File: main_window.py
# Description: File where is located the main window.
# Date: 08/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtCore import (Qt, pyqtSignal, pyqtSlot)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QMainWindow, QUndoStack, QDockWidget, QWidget,
                             QTabWidget, QVBoxLayout, QComboBox, QMessageBox)

from proteus.controllers import (FileController, ViewsController,
                         ProjectController)
from PyQt5 import uic
from proteus.controllers.views import load_views
from proteus.controllers.save_state_machine import SaveMachine
from proteus.model.object import Object
from proteus.utils.model.main_window_logic import MainWindowLogic
import proteus.config as proteus_config
from proteus.utils.i18n import trans
from proteus.utils.model.visualizer import Visualizer
from proteus.utils.model.preferences import Preferences, PreferencesDialog
from proteus.view.widgets.ribbons.ribbon import Ribbon
from proteus.view.widgets.tree import DocumentInspector
from proteus.view.actions.undo_action import UndoAction
from proteus.view.actions.redo_action import RedoAction
import proteus

class MainWindow(QMainWindow):
    """
    Main window class.
    """
    update_view = pyqtSignal()

    def __init__(self, project_path=None, project_title=None, clean=False):
        proteus.logger.info('Init main window')
        super().__init__()
        uic.loadUi(f"{proteus_config.Config().resources_directory}/ui/main.ui", self)
        self.setWindowIcon(QIcon(f'{proteus_config.Config().resources_directory}/icons/proteus_logo.png'))
        self.window_logic = MainWindowLogic(self)

        # Controllers
        self.projectController = ProjectController(self)
        self.file = FileController(self)
        self.views = ViewsController(self)

        self.ribbon = self.load_ribbon()
        self.settings = Preferences.load_all(self)
        self.selected_object: Object = None

        # Command stack (undo/redo)
        self.undoStack = QUndoStack()
        self.undoStack.indexChanged.connect(self.projectController.update_document)
        UndoAction(self.undoStack).getAction(self.ribbon)
        RedoAction(self.undoStack).getAction(self.ribbon)


        #BUG 'MainWindow' object has no attribute 'visualizers'
        self.update_view.connect(lambda: self.views.update_views)
        self.selected_document_index = 0

        if project_path:
            self.file.load_project(project_path, project_title=project_title)
        
    def closeEvent(self, event):
        """
        Detects the close window event and shows a warning message box,
        if the project is not saved.
        """
        # We check if the Title starts with "Proteus - ". The reason is
        # because the window title is changed to the pattern 
        # "Proteus - 'PROJECTNAME'"when the project is loaded.
        if (self.windowTitle().startswith('Proteus - ')):
            if(not SaveMachine().all_states_clean()):
                close = QMessageBox.question(self,
                                            trans("QUIT"),
                                            trans("If you leave before saving, your changes will be lost."),
                                            trans(QMessageBox.Yes) | trans(QMessageBox.No))
                if close == QMessageBox.Yes:
                    event.accept()
                else:
                    event.ignore()

    def create_dock_windows(self) -> None:
        """
        Creates dock windows.
        """
        proteus.logger.info('Main Window - create dock windows')
        self.create_visualizer_widget()
        self.create_document_inspector()
        self.setDockNestingEnabled(1)

    def load_ribbon(self) -> Ribbon:
        """
        Loads ribbon menu.

        :return: ribbon widget.
        """
        proteus.logger.info('Main Window - load ribbon')
        
        dock = QDockWidget("Ribbon", self)
        dock.setTitleBarWidget(QWidget())

        ribbon = QTabWidget()
        dock.setWidget(ribbon)
        dock.setAcceptDrops(False)
        self.addDockWidget(Qt.TopDockWidgetArea, dock)

        return Ribbon(self, ribbon)

    def create_document_inspector(self) -> None:
        """
        Creates document inspector tree.
        """
        proteus.logger.info('Main Window - create doc inspector')
        
        dock = QDockWidget("Document")
        dock.setObjectName("QDockWidget Document")
        layout = QVBoxLayout()
        layout.setObjectName("create_document_inspector BoxLayout")

        # TODO refactor
        self.document_tree = DocumentInspector(self)
        self.document_tree.update.connect(self.projectController.update_document)
        self.document_tree.clicked.connect(self.window_logic.select_object)

        #Basically we create the Combobox and set the first document as the current one
        self.document_combobox = QComboBox()
        self.window_logic.combo_box_add_item()
        self.projectController.change_document_index(index=0)
        self.projectController.change_document(document = self.document_combobox.itemData(0))
        
        # Signals so the combobox update automatically when change from one to another doc
        self.document_combobox.currentIndexChanged.connect(lambda index: self.projectController.change_document_index(index=index))
        self.document_combobox.currentIndexChanged.connect(lambda index: self.projectController.change_document(document = self.document_combobox.itemData(index)))

        layout.addWidget(self.document_combobox)
        layout.addWidget(self.document_tree)
        layout.setContentsMargins(2, 2, 2, 2)
        docked_widget = QWidget()
        docked_widget.setLayout(layout)
        dock.setWidget(docked_widget)

        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def create_visualizer_widget(self) -> None:
        """
        Creates and loads visualizers.
        """
        proteus.logger.info('Main Window - create visualizer widget')
        
        tab = QTabWidget()
        tab.setTabsClosable(True)
        tab.setMovable(True)

        self.visualizers = []
        self.views2 = load_views()

        for view in self.views2:
            visualizer = Visualizer()
            visualizer.setView(self.views2.index(view))
            visualizer.load(view, self.projectController.project,
                            self.projectController.selected_document_index)
            self.visualizers.append(visualizer)

        for visualizer in self.visualizers:
            tab.addTab(visualizer, f"{trans('visualizer')} {self.visualizers.index(visualizer)}")

        self.setCentralWidget(tab)

    @pyqtSlot()
    def preferences(self) -> None:
        """
        Opens the preferences dialog.
        """
        proteus.logger.info('Main Window - preferences')
        
        dialog = PreferencesDialog(self)
        dialog.exec()

    def add_object(self, obj) -> None:
        """
        Adds a child to the selected object.

        :param obj: The object to be cloned and inserted.
        """
        proteus.logger.info('Main Window - add object')
        
        self.window_logic.add_object(obj)