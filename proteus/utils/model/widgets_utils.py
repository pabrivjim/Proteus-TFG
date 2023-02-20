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
from proteus.model.property import BooleanProperty, ClassListProperty, DateProperty, EnumProperty, FileProperty, FloatProperty, IntegerProperty, MarkdownProperty, Property, StringProperty, TimeProperty, UrlProperty
import proteus.view.widgets.properties as properties
import logging

def string_widget(parent: QWidget, obj: StringProperty) -> QLineEdit:
    """
    Widget for string property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QLineEdit widget.
    """
    logging.info('widgets utils - string widget')
    
    w = QLineEdit(parent)
    w.setText(str(obj.value))
    return w


def time_widget(parent: QWidget, obj: TimeProperty) -> QTimeEdit:
    """
    Widget for time property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QTimeEdit widget.
    """
    logging.info('widgets utils - time widget')
    
    w = QTimeEdit(parent)
    time = QTime.fromString(str(obj.value))
    w.setTime(time)
    return w


def date_widget(parent: QWidget, obj: DateProperty) -> QDateEdit:
    """
    Widget for date property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QDateEdit widget.
    """
    logging.info('widgets utils - date widget')
    
    w = QDateEdit(parent)
    date = QDate.fromString(str(obj.value))
    w.setDate(date)
    return w


def enum_widget(parent: QWidget, obj: EnumProperty) -> QComboBox:
    """
    Widget for enum property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QDateEdit widget.
    """
    logging.info('widgets utils - enum widget')
    
    w = QComboBox(parent)
    w.addItems(list(obj.get_choices_as_set()))
    if obj.get_choices_as_set():
        w.setCurrentIndex(list(obj.get_choices_as_set()).index(obj.value))
    return w


def boolean_widget(parent: QWidget, obj: BooleanProperty) -> QCheckBox:
    """
    Widget for boolean property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QCheckbox widget.
    """
    logging.info('widgets utils - boolean widget')
    
    w = QCheckBox(parent)
    w.setChecked(bool(obj.value))
    return w


def number_widget(parent: QWidget, obj: IntegerProperty) -> QSpinBox:
    """
    Widget for number property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QDoubleSpinBox widget.
    """
    logging.info('widgets utils - number widget')
    
    w = QSpinBox(parent)
    if(obj.value is None or obj.value == "None"):
        obj.value = 1
    w.setValue(int(obj.value))
    return w

def real_widget(parent: QWidget, obj: FloatProperty) -> QDoubleSpinBox:
    """
    Widget for number property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QDoubleSpinBox widget.
    """
    logging.info('widgets utils - number widget')
    
    w = QDoubleSpinBox(parent)
    if(obj.value is None or obj.value == "None"):
        obj.value = 1
    
    # check if is str
    if(isinstance(obj.value, str) and "," in obj.value):
        obj.value = obj.value.replace(",", ".")
    w.setValue(float(obj.value))
    return w


def file_widget(parent: QWidget, obj: FileProperty) -> QLineEdit:
    """
    TODO
    Widget for file property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QLineEdit widget.
    """
    logging.info('widgets utils - file widget')
    
    w = QLineEdit(parent)
    w.setText(str(obj.value))
    return w

def url_widget(parent: QWidget, obj: UrlProperty) -> QLineEdit:
    """
    TODO
    Widget for url property.

    :param parent: Parent widget.
    :param obj: Property dict.
    :return: QLineEdit widget.
    """
    logging.info('widgets utils - url widget')
    
    w = QLineEdit(parent)
    w.setText(str(obj.value))
    return w

def class_list_widget(parent: QWidget, obj: ClassListProperty) -> QListWidget:
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
        MarkdownProperty.element_tagname: properties.MarkdownWidget,
        StringProperty.element_tagname: string_widget,
        FloatProperty.element_tagname: real_widget,
        IntegerProperty.element_tagname: number_widget,
        UrlProperty.element_tagname: url_widget,
        FileProperty.element_tagname: file_widget,
        TimeProperty.element_tagname: time_widget,
        DateProperty.element_tagname: date_widget,
        EnumProperty.element_tagname: enum_widget,
        BooleanProperty.element_tagname: boolean_widget,
        ClassListProperty.element_tagname: class_list_widget,
    }
    property_type = object_property.element_tagname
    widget = widgets[property_type] if property_type in widgets else string_widget
    return widget(parent, object_property)

