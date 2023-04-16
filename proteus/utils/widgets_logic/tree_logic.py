# ==========================================================================
# File: tree_logic.py
# Description: File where is located de logic of the TreeWidget.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================

from functools import partial
from PyQt5.QtCore import (Qt, QByteArray, QPoint, QModelIndex)
from PyQt5.QtGui import (QDrag, QIcon)
from PyQt5.QtWidgets import (QTreeWidget, QMenu, QTreeWidgetItem, QMessageBox)
from proteus.model import PROTEUS_ANY
from proteus.model.object import Object
from proteus.model.project import Project
from .qundo_commands import CreateDocument
from proteus.utils.widgets_logic.qundo_commands import CreateObject
from proteus.view.widgets.properties import PropertyDialog
from proteus.utils.widgets_logic.qundo_commands import DeleteObject, DeleteDocument, MoveNode
import proteus.config as config
import proteus

class TreeLogic():
    """
    Class that contains the tree logic.
    """

    def __init__(self, docInspector, parent, dragged) -> None:
        proteus.logger.info('Init TreeLogic')
        self._draggedItem = dragged
        self.parent = parent
        self.docInspector = docInspector

    def mimeTypes(self) -> list:
        """
        Returns mimetypes.
        """
        proteus.logger.info('TreeLogic - mimeTypes')

        mimetypes = QTreeWidget.mimeTypes(self.docInspector)
        mimetypes.append(self.docInspector.mimetype)
        return mimetypes

    def startDrag(self, supportedActions) -> None:
        """
        Logic to do when dragging an item.

        :param supportedActions:
        """
        proteus.logger.info('TreeLogic - start drag')
        drag = QDrag(self.docInspector)
        mimedata = self.docInspector.model().mimeData(self.docInspector.selectedIndexes())

        encoded = QByteArray()
        mimedata.setData(self.docInspector.mimetype, encoded)

        # change
        self._draggedItem = self.docInspector.selectedItems()[0]

        drag.setMimeData(mimedata)
        drag.exec(supportedActions)

    def dropEvent(self, event):
        """
        Logic to do on drop event.

        :param event:
        """
        proteus.logger.info('TreeLogic - drop event')

        # Get previous position
        from_parent = self._draggedItem.parent()
        # Get new position
        to_parent = self._draggedItem.parent()

        if(to_parent is None):
            event.ignore()
        else:
            # Exec Drop
            event.setDropAction(Qt.MoveAction)
            QTreeWidget.dropEvent(self.docInspector, event)
            
            new_parent: Object = to_parent.data(0, Qt.UserRole)
            dragged_object: Object = self._draggedItem.data(0, Qt.UserRole)

            # If the new parent doesn't havent all the types or the new parent doesnt accept any of the classes
            # that the dragged object has, then we don't do anything and we warn the user.
            if (not((PROTEUS_ANY in new_parent.acceptedChildren) or
                any(x in new_parent.acceptedChildren for x in dragged_object.classes))):
                proteus.logging.warning('TreeLogic - drop event - Not accepted children')

                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText(f"'{new_parent.get_property('name').value}' doesn't accept '{dragged_object.get_property('name').value}' as a child")
                msg.setDetailedText(f"{new_parent.get_property('name').value} accepted children (classes): {new_parent.acceptedChildren}\n{dragged_object.get_property('name').value} classes: {dragged_object.classes}")
                msg.setWindowTitle("Not accepted children")
                msg.exec_()

            project: Project = self.parent.projectController.project

            command = MoveNode(
                    project,
                    self._draggedItem.data(0, Qt.UserRole),
                    from_parent.data(0, Qt.UserRole),
                    to_parent.data(0, Qt.UserRole))
            self.parent.undoStack.push(command)

    def fillItem(self, inItem, outItem):
        """
        Fill item.

        :param inItem:
        :param outItem:
        """
        proteus.logger.info('TreeLogic - fill item')

        for col in range(inItem.columnCount()):
            for key in range(Qt.UserRole):
                role = Qt.ItemDataRole(key)
                outItem.setData(col, role, inItem.data(col, role))

    def fillItems(self, itFrom, itTo):
        """
        Fill items.

        :param itFrom:
        :param itTo:
        """
        proteus.logger.info('TreeLogic - fill items')

        for ix in range(itFrom.childCount()):
            it = QTreeWidgetItem(itTo)
            ch = itFrom.child(ix)
            self.fillItem(ch, it)
            self.fillItems(ch, it)

    def load_document(self) -> None:
        """
        Method that load the document from the project.
        """
        proteus.logger.info('TreeLogic - load document')

        self.docInspector.clear()
        documents: dict = self.parent.projectController.project.documents

        list_documents: list = list(documents.values())
        if (self.parent.projectController.selected_document_index == len(documents)):
            self.parent.projectController.selected_document_index = self.parent.projectController.selected_document_index-1
        if documents:
            self.parent.ribbon.delete_tb.setEnabled(True)
            current_document: Object = list_documents[self.parent.projectController.selected_document_index]
            return self.loadData(current_document)
        self.parent.ribbon.delete_tb.setEnabled(False)

    def loadData(self, doc: Object, root=None) -> None:
        """
        Loads data.

        :param data:
        :param root:
        """
        proteus.logger.info('TreeLogic - load data')

        if not root:
            name = doc.get_property("name").value or "Untitled"

            root = QTreeWidgetItem(self.docInspector, [str(doc.id)])
            root.setData(0, Qt.UserRole, doc)
            root.setText(0, name)
            root.setExpanded(True)

        children = doc.children.values()
        for child in children:
            child_item = self.add_child(root, child)
            self.loadData(child, root=child_item)

    def add_child(self, parent: Object, child: Object) -> QTreeWidgetItem:
        """
        Adds widget item to parent item.

        :param parent: Parent TreeWidgetItem.
        :param child:
        :return: Child item.
        """
        proteus.logger.info('TreeLogic - add child')

        name = child.get_property("name").value or "Untitled"
        obj_classes = child.classes
        klass = obj_classes[len(obj_classes) - 1]

        child_item = QTreeWidgetItem(parent, [name])
        child_item.setIcon(0, QIcon(f"{config.Config().resources_directory}/assets/icons/{klass}.svg"))
        child_item.setData(0, Qt.UserRole, child)
        child_item.setExpanded(True)
        return child_item

    def transverse(self, model=None, root=None) -> dict:
        """
        Transverses tree widget.

        :param model:
        :param root:
        """
        proteus.logger.info('TreeLogic - transverse')

        if not model:
            model = self.docInspector.itemAt(0, 0)
            root = model.data(0, Qt.UserRole)
            root["children"] = []

        for i in range(model.childCount()):
            item = model.child(i)
            aux = item.data(0, Qt.UserRole)
            aux["children"] = []
            root["children"].append(aux)
            self.transverse(model=item, root=aux)

        return root

    def open_menu(self, position: QPoint) -> None:
        """
        Opens right-click context menu.

        :param position: right-click position.
        """
        proteus.logger.info('TreeLogic - open menu')

        mdlIdx = self.docInspector.indexAt(position)
        if not mdlIdx.isValid():
            return
        item = self.docInspector.itemFromIndex(mdlIdx)

        right_click_menu = QMenu()
        txt = "object" if item.parent() else "document"
        act_edit = right_click_menu.addAction(self.docInspector.tr(f"Edit {txt}"))
        act_edit.triggered.connect(partial(self.edit_item, mdlIdx))

        act_del = right_click_menu.addAction(self.docInspector.tr(f"Delete {txt}"))
        act_del.triggered.connect(partial(self.delete_item, item))

        act_clone = right_click_menu.addAction(self.docInspector.tr(f"Clone {txt}"))
        act_clone.triggered.connect(partial(self.clone_item, item))

        right_click_menu.exec(self.docInspector.sender().viewport().mapToGlobal(position))

    def delete_item(self, item) -> None:
        """
        Deletes item.

        :param item: Item to remove from the tree.
        """
        proteus.logger.info('TreeLogic - delete item')

        proteus_item: Object = item.data(0, Qt.UserRole)
        if item.parent():
            parent_obj: Object = item.parent().data(0, Qt.UserRole)
            item.parent().removeChild(item)
            command = DeleteObject(self.parent.projectController.project, parent_obj, proteus_item)
            self.parent.undoStack.push(command)
        else:
            command = DeleteDocument(self.parent.projectController.project, proteus_item,
                                     self.parent.document_combobox, self.parent.projectController.selected_document_index)
            self.parent.undoStack.push(command)

    def edit_item(self, index: QModelIndex) -> None:
        """
        Updates item.

        :param index: Index of the item to edit.
        """
        proteus.logger.info('TreeLogic - edit item')

        item = self.docInspector.itemFromIndex(index)
        obj = item.data(0, Qt.UserRole)
        dialog = PropertyDialog(self.parent, obj)
        dialog.exec()

    def clone_item(self, item) -> None:
        """
        Method that clones item and if has children
        it also clone them too.

        :param item: Item to remove from the tree.
        """
        proteus.logger.info('TreeLogic - clone item')

        obj: Object = item.data(0, Qt.UserRole)
        obj_clone = obj.clone_object(obj.parent)
        project: Project = self.parent.projectController.project
        app = self.parent
        if(item.parent() == None):
            command = CreateDocument(project, obj_clone, app, len(project.documents))
            self.parent.undoStack.push(command)
        else:
            command = CreateObject(self.parent.projectController.project, obj.parent,
                                   obj_clone)
            self.parent.undoStack.push(command)
