class InitiativeFate:
    def __init__(self, birth):
        self.birth = birth
        birth.fate = self
        self.current = None
        
    #public member: birth
    #public member: current 

    def latest(self):
        if self.current:
            return self.current
        else:
            return self.birth
        
    def __deepcopy__(self, memo):
        return self
        # i.e. an InitiativeFate can never be deepcopied
        # This is because when you deepcopy a transition, you
        # don't want to deepcopy its fate
        
        # It would be cleaner to alter the semantics of deepcopy on
        # transitions. But in order to do that, you must define a
        # __deepcopy__, which means that all of "transition"'s subclasses
        # must also define a __deepcopy__; you no longer get to take advantage
        # of the built-in version, as far as i can tell.
        
        # Which would make things hard on the compiler, since it automatically
        # creates a bunch of motions depending on the ruleFile, and motions
        # are subclasses of transitions.

        # So, I figured this is the simpler solution, even if it is dirtier.

