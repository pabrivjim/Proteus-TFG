# ==========================================================================
# File: save_state_machine.py
# Description: File where is located de logic of the state of files.
# Date: 11/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================

from enum import Enum

class States(Enum):
    """
    This class is used to set the different types of states that
    can be find in the different documents.
    """
    FRESH = 0               # NEW
    DIRTY = 1               # EDIT
    CLEAN = 2               # SAVED
    DELETED = 3             # DELETED

class SaveMachine():
    """
    The purpouse of this class is to save and set the different States
    of the different documents. Using clase, we can know if a document
    is dirty, clean, fresh or deleted.
    """

    states = {}
    def __init__(self, id= None):
        self.id = id
    
    def set_state(self,state: States) -> None:
        """
        Sets the state of the document.
        """
        self.states[self.id] = state

    def remove_state(self)-> None:
        """
        Removes a state from the dictionary.
        """
        del self.states[self.id]

    def add_state(self, id, state) -> None:
        """
        Adds a new state to the dictionary.
        """
        self.states[id] = state
    
    def is_dirty(self) -> bool:
        """
        Returns True if the document is dirty.
        """
        return self.states[self.id] == States.DIRTY
    
    def is_fresh(self) -> bool:
        """
        Returns True if the document is deleted.
        """
        return self.states[self.id] == States.FRESH
    
    def is_deleted(self) -> bool:
        """
        Returns True if the document is deleted.
        """
        return self.states[self.id] == States.DELETED

    def get_state(self) -> States:
        """
        Returns the state of the document.
        """
        if(self.id not in self.states):
            self.states[self.id] = States.FRESH
        return self.states[self.id]

    def all_states_clean(self) -> bool:
        """
        Returns True if all the documents are clean.
        """
        for id, state in self.states.items():
            if state != States.CLEAN:
                return False
        return True
    
    @staticmethod
    def set_document_objects_to_deleted(doc) -> None:
        """
        Sets all objects in document to DELETED.
        """

        doc_obj = SaveMachine(doc["id"])
        doc_obj.set_state(States.DELETED)

        # we get all the children of a doc and set to deleted.
        def get_objects(nodes):
            for node in nodes:
                obj = SaveMachine(node["id"])
                obj.set_state(States.DELETED)
                get_objects(node["children"])
        
        get_objects(doc["children"])

def set_all_states_clean() -> None:
        """
        Sets all the documents to clean.
        """
        for state in SaveMachine.states:
            SaveMachine.states[state] = States.CLEAN
