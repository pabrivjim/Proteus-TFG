# ==========================================================================
# File: ribons_logic.py
# Description: File where is located de logic of Ribbons.
# Date: 30/06/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================ç
from functools import partial
from PyQt5.QtGui import (QIcon)
from PyQt5.QtWidgets import (QToolButton)
from proteus.model.archetype_manager import ArchetypeManager
from proteus.model.archetype_proxys import ObjectArchetypeProxy
from proteus.utils.config import CONFIG_FOLDER 
from proteus.utils.i18n import trans
import proteus

class RibbonsLogic():
    """
    Class that contains the ribbon logic.
    """

    def __init__(self, parent) -> None:
        proteus.logger.info('Init RibbonsLogic')
        self.parent = parent
    
    def set_archetypes(self):
        """
        Set archetypes to ribbon from object archetypes.
        """
        proteus.logger.info('RibbonsLogic - set archetypes')
        self.init_tabs(ArchetypeManager.load_object_archetypes())

    def init_tabs(self, content: dict) -> None:
        """
        Add tabs to ribbon and adds archetypes buttons.
        """
        proteus.logger.info('RibbonsLogic - init tabs')
        tab_label = trans("archetypes")
        self.parent.buttons = {}
        actions = {}
        tab_content = self.parent.add_tab(tab_label)
        for group_name, group_archetypes  in content.items():            
            button_group = tab_content.add_group(group_name)
            archetype: ObjectArchetypeProxy
            for archetype in group_archetypes:
                archetype_id = archetype.id
                archetype_type = trans(archetype.classes)
                icon_path = f"{CONFIG_FOLDER}/assets/icons/{archetype.classes}.svg"
                tool_button = QToolButton()
                tool_button.setText(archetype_type)
                tool_button.setToolTip(archetype_type)
                tool_button.setEnabled(False)
                tool_button.setIcon(QIcon(icon_path))
                tool_button.setObjectName(archetype_id)
                if(not(archetype_id in self.parent.buttons)):
                    actions[archetype_id] = partial(self.parent.parent.add_object, archetype)
                    self.parent.buttons[archetype_id] = [tool_button, archetype, "archetype"]
                    button_group.add_button(tool_button)

        for key in self.parent.buttons:
            tb, _, _ = self.parent.buttons[key]
            tb.clicked.connect(actions[key])
    

