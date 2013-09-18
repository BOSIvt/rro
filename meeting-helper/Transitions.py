from time import *

# members:
#   notes
#   timeInitiated


class transition:
    def __init__(self, state):
    #    self.state = state
        if not hasattr(self, 'notes'):
            self.notes = ''
        if not hasattr(self, 'timeInitiated'):
            self.timeInitiated = gmtime()
        

    def __cmp__(self, y):
        if hasattr(self,'id') and hasattr(y,'id') :
            return cmp(self.id, y.id)
        
        else:
            return cmp(id(self), id(y))
        

    def setID(self,id):
        self.id = id



class motionAdoptedTransition(transition):
    def __init__(self, theMotion):
        self.theMotion = theMotion

class motionRejectedTransition(transition):
    def __init__(self, theMotion):
        self.theMotion = theMotion

class UnknownTransition(transition):
    pass
