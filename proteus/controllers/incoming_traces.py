# ==========================================================================
# File: incoming_traces.py
# Description: File where is located de logic of the state of files.
# Date: 11/07/22
# Version: 1.0.0
# Author: Pablo Rivera Jiménez
# ==========================================================================

class IncomingTraces():
    """
    The purpose is to find out which objects have
    associated traces coming from other objects.
    """
    #Key -> id of the object,
    #Value -> id of the objects that have an incoming trace to the key object.
    incoming_traces = {}
    def __init__(self, id= None):
        self.id = id
    
    def get_traces(self):
        """
        Return the list with the incoming traces.
        """
        if(self.id in self.incoming_traces):
            return self.incoming_traces[self.id]
        else:
            return

    def remove_trace(self, id)-> None:
        """
        Removes a incoming trace from the value list
        of an object.
        """
        del self.incoming_traces[self.id][id]

    def add_trace(self, id) -> None:
        """
        Adds a new trace to the list value.
        """
        if(self.id in self.incoming_traces):
            self.incoming_traces[self.id].append(id)
        else:
            self.incoming_traces[self.id] = [id]
