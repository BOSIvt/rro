from State import *


class initial_state(state):
    def __init__(self, args):
        state.__init__(self,args)
        self.beginning_of_meeting = True

    name = 'INITIAL STATE'

    def type(self, state):
        return r'state'
    
    def previous_question_pending(self):
        return False	
    
    def initialStateAllowsApplicationOf(self, state, initiative):    
        return True 

    def openForPrincipalMotion(self):
        return isinstance(self.getPendingMotion(), RootInitiative)
