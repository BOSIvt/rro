from time import *

from Transitions import *

from UncopyableStatePointer import *


# this class has a lowercase name because the ruleset can refer to it

class action(transition):
    

    # members:
    #   target
    #   actor
    #   canHaveTarget
    #   name
    #   internal_name
    #   stateWhenCreated
    
    def __init__(self, state):
        transition.__init__(self, state)
        if not hasattr(self, 'target'):
            self.target = None
        if not hasattr(self, 'actor'):
            self.actor = None
        if not hasattr(self, 'canHaveTarget'):
            self.canHaveTarget = False
        if not hasattr(self, 'name'):
            self.name = ''
        if not hasattr(self, 'internal_name'):
            self.internal_name = self.name

        self.stateWhenCreatedPointer = UncopyableStatePointer(state)
        #print self.stateWhenCreated.getPendingMotion()
    
    def summary(self, state):
        pass

    def getTargetType(self):
        return None
        # deprecated

    def find_targets(self, state):
        return []
