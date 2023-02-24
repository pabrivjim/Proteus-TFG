# ==========================================================================
# File: ribons_logic.py
# Description: File where is located de logic of Ribbons.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================ç
from functools import partial
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QToolButton, QMenu)
from proteus.model.archetype_manager import ArchetypeManager
from proteus.model.archetype_proxys import ObjectArchetypeProxy
from proteus.utils.config import Config, CONFIG_FOLDER 
from proteus.utils.i18n import trans
import logging

class RibbonsLogic():
    """
    Class that contains the ribbon logic.
    """

    def __init__(self, parent) -> None:
        logging.info('Init RibbonsLogic')
        self.parent = parent
    
    def set_archetypes(self):
        """
        Set archetypes to ribbon from object archetypes.
        """
        logging.info('RibbonsLogic - set archetypes')
        # Archetypes
        archetypes_groups = []
        print(ArchetypeManager.load_object_archetypes())

        # for group_name, group_buttons in Config.load_object_archetypes().items():
        #     archetypes_groups.append({
        #         "name": trans(group_name),
        #         "buttons": list(map(lambda archetype: {
        #             "text": trans(archetype),
        #             "tooltip": trans(archetype),
        #             "enabled": False,
        #             "icon": f"{CONFIG_FOLDER}/assets/icons/{archetype}.svg",
        #             "action": partial(self.parent.parent.add_object, group_buttons[archetype][0]),
        #             "type": "archetype",
        #             "objects": group_buttons[archetype]
        #         }, group_buttons.keys()))
        #     })

        # self.init_tabs({
        #     "tabs": [
        #         {
        #             "name": trans("archetypes"),
        #             "groups": archetypes_groups
        #         }
        #     ]
        # })

        self.init_tabs(ArchetypeManager.load_object_archetypes())

    def init_tabs(self, content: dict) -> None:
        """
        Add tabs to ribbon and adds archetypes buttons.
        """
        logging.info('RibbonsLogic - init tabs')
        tab_label = trans("archetypes")
        self.parent.buttons = {}
        actions = {}
        for group_name, group_archetypes  in content.items():
            tab_content = self.parent.add_tab(tab_label)
            button_group = tab_content.add_group(group_name)
            archetype: ObjectArchetypeProxy
            for archetype in group_archetypes:
                archetype_type = trans(archetype.classes)
                icon_path = f"{CONFIG_FOLDER}/assets/icons/{archetype.classes}.svg"
                tool_button = QToolButton()
                tool_button.setText(archetype_type)
                tool_button.setToolTip(archetype_type)
                tool_button.setEnabled(False)
                tool_button.setIcon(QIcon(icon_path))
                tool_button.setObjectName(archetype_type)
                actions[archetype_type] = partial(self.parent.parent.add_object, archetype)
                self.parent.buttons[archetype_type] = [tool_button, archetype, "archetype"]
                button_group.add_button(tool_button)

        for key in self.parent.buttons:
            tb, _, _ = self.parent.buttons[key]
            tb.clicked.connect(actions[key])


        # for tab in content["tabs"]:
        #     name, groups = tab["name"], tab["groups"]
        #     tab_content = self.parent.add_tab(name)
        #     for group in groups:
        #         group_name, buttons = group["name"], group["buttons"]
        #         button_group = tab_content.add_group(group_name)
        #         for button in buttons:
        #             tool_button = QToolButton()
        #             tool_button.setText(button["text"])
        #             tool_button.setToolTip(button["tooltip"])
        #             tool_button.setEnabled(button["enabled"])
        #             tool_button.setIcon(QIcon(button["icon"]))
        #             tool_button.setObjectName(button["text"])

        #             if "objects" in button and len(button["objects"]) > 1:
        #                 tool_button.setPopupMode(QToolButton.MenuButtonPopup)
        #                 menu = QMenu(tool_button)
        #                 for arch_obj in button["objects"]:
        #                     obj_name = arch_obj["properties"].get(
        #                         "name", {"value": "Untitled"})["value"]
        #                     action = menu.addAction(QIcon(button["icon"]), obj_name)
        #                     action.triggered.connect(partial(self.parent.parent.add_object, arch_obj))
        #                 tool_button.setMenu(menu)

        #             self.parent.buttons[button["text"]] = [tool_button, button]
        #             button_group.add_button(tool_button)

        # for key in self.parent.buttons:
        #     tb, b = self.parent.buttons[key]
        #     tb.clicked.connect(b["action"])

    

