# ==========================================================================
# File: tree_logic.py
# Description: File where is located de logic of the TreeWidget.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import copy
from functools import partial
import shortuuid
from PyQt5.QtCore import (Qt, QByteArray, QDataStream, QIODevice, QPoint,
                          QModelIndex)
from PyQt5.QtGui import (QDrag, QIcon)
from PyQt5.QtWidgets import (QTreeWidget, QMenu, QTreeWidgetItem)
from proteus.controllers.save_state_machine import SaveMachine
from proteus.model.object import Object
from proteus.utils.model.traces_logic import TraceLogic
from .nodes_utils import rename_children_ids_from_node
from .document_dialog_logic import change_combo_box
from .qundo_commands import CreateDocument
from proteus.utils.model.qundo_commands import CreateObject
from proteus.view.widgets.properties import PropertyDialog
from proteus.utils.model.qundo_commands import DeleteObject, DeleteDocument, MoveNode
import proteus.utils.config as config 
from proteus.controllers.incoming_traces import IncomingTraces
from proteus.view.widgets.traces import DeleteObjectWithTraces
import logging

class TreeLogic():
    """
    Class that contains the trace logic.
    """

    def __init__(self, docInspector, parent, dragged) -> None:
        logging.info('Init TreeLogic')
        self._draggedItem = dragged
        self.parent = parent
        self.docInspector = docInspector
        
    def mimeTypes(self) -> list:
        """
        Returns mimetypes.
        """
        logging.info('TreeLogic - mimeTypes')
        
        mimetypes = QTreeWidget.mimeTypes(self.docInspector)
        mimetypes.append(self.docInspector.mimetype)
        return mimetypes

    def startDrag(self, supportedActions) -> None:
        """
        Logic to do when dragging an item.

        :param supportedActions:
        """
        logging.info('TreeLogic - start drag')
        
        drag = QDrag(self.docInspector)
        mimedata = self.docInspector.model().mimeData(self.docInspector.selectedIndexes())

        encoded = QByteArray()
        stream = QDataStream(encoded, QIODevice.WriteOnly)
        self.encodeData(self.docInspector.selectedItems(), stream)
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
        logging.info('TreeLogic - drop event')
        
        # Get previous position
        from_parent = self._draggedItem.parent()
        from_row = from_parent.indexOfChild(self._draggedItem)

        # Exec drop
        event.setDropAction(Qt.MoveAction)
        QTreeWidget.dropEvent(self.docInspector, event)

        # Get new position
        to_parent = self._draggedItem.parent()
        to_row = to_parent.indexOfChild(self._draggedItem)

        command = MoveNode(
            self.parent.project.data,
            self._draggedItem.data(0, Qt.UserRole)["id"],
            from_parent.data(0, Qt.UserRole)["id"], from_row,
            to_parent.data(0, Qt.UserRole)["id"], to_row)
        self.parent.undoStack.push(command)

    def fillItem(self, inItem, outItem):
        """
        Fill item.

        :param inItem:
        :param outItem:
        """
        logging.info('TreeLogic - fill item')
        
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
        logging.info('TreeLogic - fill items')
        
        for ix in range(itFrom.childCount()):
            it = QTreeWidgetItem(itTo)
            ch = itFrom.child(ix)
            self.fillItem(ch, it)
            self.fillItems(ch, it)

    def encodeData(self, items, stream):
        """
        Encodes data.

        :param items:
        :param stream:
        """
        logging.info('TreeLogic - encode data')
        
        stream.writeInt32(len(items))
        for item in items:
            p = item
            rows = []
            while p is not None:
                rows.append(self.docInspector.indexFromItem(p).row())
                p = p.parent()
            stream.writeInt32(len(rows))
            for row in reversed(rows):
                stream.writeInt32(row)
        return stream

    def decodeData(self, encoded, tree):
        """
        Decodes data.

        :param encoded:
        :param tree:
        """
        logging.info('TreeLogic - decode data')
        
        items = []
        rows = []
        stream = QDataStream(encoded, QIODevice.ReadOnly)
        while not stream.atEnd():
            nItems = stream.readInt32()
            for i in range(nItems):
                path = stream.readInt32()
                row = []
                for j in range(path):
                    row.append(stream.readInt32())
                rows.append(row)

        for row in rows:
            it = tree.topLevelItem(row[0])
            for ix in row[1:]:
                it = it.child(ix)
            items.append(it)
        return items

    def load_document(self) -> None:
        """
        Method that load the document from the project.
        """
        logging.info('TreeLogic - load document')
        
        print("Loading doc")
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
        logging.info('TreeLogic - load data')
        
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
        logging.info('TreeLogic - add child')
        
        name = child.get_property("name").value or "Untitled"
        obj_classes = child.classes
        klass = obj_classes[len(obj_classes) - 1]

        child_item = QTreeWidgetItem(parent, [name])
        child_item.setIcon(0, QIcon(f"{config.CONFIG_FOLDER}/assets/icons/{klass}.svg"))
        child_item.setData(0, Qt.UserRole, child)
        child_item.setExpanded(True)
        return child_item

    def transverse(self, model=None, root=None) -> dict:
        """
        Transverses tree widget.

        :param model:
        :param root:
        """
        logging.info('TreeLogic - transverse')
        
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
        logging.info('TreeLogic - open menu')
        
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
        logging.info('TreeLogic - delete item')
        proteus_item: Object = item.data(0, Qt.UserRole)
        if item.parent():
            parent_obj = item.parent().data(0, Qt.UserRole).state
            item.parent().removeChild(item)
            command = DeleteObject(self.parent.project.data, proteus_item.id, proteus_item.state, parent_obj)
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
        logging.info('TreeLogic - edit item')
        
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
        logging.info('TreeLogic - clone item')

        obj = item.data(0, Qt.UserRole)
        obj_clone = copy.copy(obj)
        obj_clone["id"] = str(shortuuid.random(length=12))
        project_data = self.parent.project.data
        if(item.parent() == None):
            obj_clone = rename_children_ids_from_node(obj_clone)
            command = CreateDocument(project_data, obj_clone, len(project_data["documents"]))
            self.parent.undoStack.push(command)
            change_combo_box(self.parent)
        else:
            command = CreateObject(project_data, item.parent().data(0, Qt.UserRole)["id"],
                                obj_clone)
            self.parent.undoStack.push(command)