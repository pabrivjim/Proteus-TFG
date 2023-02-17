# ==========================================================================
# File: widgets_utils.py
# Description: File where is functions related to widgets.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
from PyQt5.QtCore import (QTime, QDate)
from PyQt5.QtWidgets import (QWidget, QTimeEdit, QLineEdit, QDateEdit, QComboBox,
                             QCheckBox, QDoubleSpinBox, QListWidget, QSpinBox)
import proteus.view.widgets.properties as properties
import logging

def string_widget(parent: QWidget, obj: dict) -> QLineEdit:
    """
    Widget for string property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QLineEdit widget.
    """
    logging.info('widgets utils - string widget')
    
    w = QLineEdit(parent)
    w.setText(obj["value"])
    return w


def time_widget(parent: QWidget, obj: dict) -> QTimeEdit:
    """
    Widget for time property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QTimeEdit widget.
    """
    logging.info('widgets utils - time widget')
    
    w = QTimeEdit(parent)
    time = QTime.fromString(obj["value"])
    w.setTime(time)
    return w


def date_widget(parent: QWidget, obj: dict) -> QDateEdit:
    """
    Widget for date property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QDateEdit widget.
    """
    logging.info('widgets utils - date widget')
    
    w = QDateEdit(parent)
    date = QDate.fromString(obj["value"])
    w.setDate(date)
    return w


def enum_widget(parent: QWidget, obj: dict) -> QComboBox:
    """
    Widget for enum property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QDateEdit widget.
    """
    logging.info('widgets utils - enum widget')
    
    w = QComboBox(parent)
    w.addItems(obj.get("choices", []))
    if obj.get("choices"):
        w.setCurrentIndex(obj.get("choices", []).index(obj["value"]))
    return w


def boolean_widget(parent: QWidget, obj: dict) -> QCheckBox:
    """
    Widget for boolean property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QCheckbox widget.
    """
    logging.info('widgets utils - boolean widget')
    
    w = QCheckBox(parent)
    w.setChecked(bool(obj["value"]))
    return w


def number_widget(parent: QWidget, obj: dict) -> QSpinBox:
    """
    Widget for number property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QDoubleSpinBox widget.
    """
    logging.info('widgets utils - number widget')
    
    w = QSpinBox(parent)
    if(obj["value"] is None or obj["value"] == "None"):
        obj["value"] = 1
    w.setValue(int(obj["value"]))
    return w

def real_widget(parent: QWidget, obj: dict) -> QDoubleSpinBox:
    """
    Widget for number property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QDoubleSpinBox widget.
    """
    logging.info('widgets utils - number widget')
    
    w = QDoubleSpinBox(parent)
    if(obj["value"] is None or obj["value"] == "None"):
        obj["value"] = 1
    
    # check if is str
    if(isinstance(obj["value"], str) and "," in obj["value"]):
        obj["value"] = obj["value"].replace(",", ".")
    w.setValue(float(obj["value"]))
    return w


def file_widget(parent: QWidget, obj: dict) -> QLineEdit:
    """
    TODO
    Widget for file property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QLineEdit widget.
    """
    logging.info('widgets utils - file widget')
    
    w = QLineEdit(parent)
    w.setText(obj["value"])
    return w


def class_list_widget(parent: QWidget, obj: dict) -> QListWidget:
    """
    TODO
    Widget for list property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QListWidget widget.
    """
    logging.info('widgets utils - class list widget')
    
    w = QListWidget(parent)
    w.setSelectionMode(2)
    return w


# Todo refactor
def get_widget_for_property(object_property, parent=None):
    """
    Function to get widget by property type.

    :param object_property: object property.
    :param parent: parent widget.
    :return: property widget.
    """
    logging.info('widgets utils - get widget for properties')

    # ClassList property is not shown here 
    
    widgets = {
        "markdownProperty": properties.MarkdownWidget,
        "stringProperty": string_widget,
        "realProperty": real_widget,
        "numberProperty": number_widget,
        "fileProperty": file_widget,
        "timeProperty": time_widget,
        "dateProperty": date_widget,
        "enumProperty": enum_widget,
        "booleanProperty": boolean_widget,
        "classList": class_list_widget,
    }
    property_type = object_property.get("type", "string")
    widget = widgets[property_type] if property_type in widgets else string_widget
    return widget(parent, object_property)

