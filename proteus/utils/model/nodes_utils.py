# ==========================================================================
# File: nodes_tuils.py
# Description: File where is functions related to nodes.
# Date: 29/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================
import copy
import logging
import shortuuid

def rename_children_ids_from_node(p: dict) -> dict:
    """
    Rename children ids from node.

    :param node: starting node.
    :return: node with children nodes changed.
    """
    logging.info('nodes utils - rename children ids from node')
    
    for i in range(0, len(p["children"])):
        obj_clone = copy.copy(p["children"][i])
        obj_clone["id"] = str(shortuuid.random(length=12))
        p["children"][i] = obj_clone
        if "children" in p["children"][i]:
            rename_children_ids_from_node(p["children"][i])
    return p


def find_node(node: dict, tg_id: str):
    """
    Find node by id (aux func).

    :param node: starting node.
    :param tg_id: node id to be found.
    :return: node if found or otherwise None.
    """
    logging.info('nodes utils - find node')
    
    if node["id"] == tg_id: return node
    for child in node["children"]:
        n = find_node(child, tg_id)
        if n: return n
    return None


def get_node(p: dict, target_id: str):
    """
    Find a node by its id.

    :param p: project dict.
    :param target_id: id of node to be found.
    :return: node if found otherwise None.
    """
    logging.info('nodes utils - get node')
    
    if p.get("id", None) == target_id: return p
    for document in p["documents"]:
        if document["id"] == target_id: return document
        n = find_node(document, target_id)
        if n: return n

def find_parent(node: dict, target_id: str):
    """
    Find parent of a node by its id (aux function).

    :param node: search from node.
    :param target_id: node id to be found.
    :return: parent node containing target_id.
    """
    logging.info('nodes utils - find parent')

    for child in node["children"]:
        if child["id"] == target_id: return node
        n = find_parent(child, target_id)
        if n: return n
    return None


def get_parent(p, child_id):
    """
    Find parent of a node by its id.

    :param p: project dict.
    :param child_id: id of child.
    :return: parent node containing child_id.
    """
    logging.info('nodes utils - get parent')
    
    for document in p["documents"]:
        n = find_parent(document, child_id)
        if n: return n