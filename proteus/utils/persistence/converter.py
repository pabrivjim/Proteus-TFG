# ==========================================================================
# File: converter.py
# Description: File where is located the Converter functions.
# Date: 04/07/22
# Version: 1.0.0
# Author: Gamaza & Pablo
# ==========================================================================
from collections import OrderedDict
from lxml import etree as ET
import logging

#DELETE
def dict2xml(element: dict, collapse=True) -> ET.Element:
    """
    dict2xml converts an object dict to XML

    :param element
    :param collapse
    :return XML object
    """
    pass


def xml2dict(element: ET.Element) -> dict:
    """
    xml2dict transforms XML object to dict

    :param element: XML element
    :return object dict
    """
    logging.info('converter - xml2dict')
    
    id = element.attrib["id"]

    classes = []
    accepted_children = []
    if "classes" in element.attrib and "acceptedChildren" in element.attrib:
        classes = element.attrib["classes"].split()
        accepted_children = element.attrib["acceptedChildren"].split()

    properties = OrderedDict()
    properties.setdefault("name", {"value": "", "type": "text"})

    prop: ET.Element
    for prop in element.find("properties"):
        name = prop.attrib["name"]
        value = prop.text
        properties[name] = {"type": prop.tag, "value": value}
        if "category" in prop.attrib:
            properties[name]["category"] = prop.attrib["category"]

        if prop.tag == "enumProperty":
            properties[name]["choices"] = prop.attrib.get("choices", "").split()

    traces = []
    if len(element.find("traces")) or element.find("traces") is not None:
        # traces = [{"id": trace.attrib["id"],"name": trace.attrib["name"], "type": trace.attrib["type"], "klass": trace.attrib["klass"]} for trace in element.find("traces")]
        traces = [{"id": trace.attrib["id"], "type": trace.attrib["type"]} for trace in element.find("traces")]


    children = []
    if len(element.find("children")) or element.find("children") is not None:
        children = [child.attrib["id"] for child in element.find("children")]

    return {
        "id": id,
        "classes": classes,
        "acceptedChildren": accepted_children,
        "properties": properties,
        "traces": traces,
        "children": children
    }
