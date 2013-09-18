class UncopyableStatePointer:

    #public member: state

    def __init__(self, state):
        self.state = state



        
    def __deepcopy__(self, memo):
        return self
        # i.e. an UncopyableStatePointer can never be deepcopied
        # This is because when you deepcopy a transition, you
        # don't want to deepcopy its state pointers
        
        # It would be cleaner to alter the semantics of deepcopy on
        # transitions. But in order to do that, you must define a
        # __deepcopy__, which means that all of "transition"'s subclasses
        # must also define a __deepcopy__; you no longer get to take advantage
        # of the built-in version, as far as i can tell.
        
        # Which would make things hard on the compiler, since it automatically
        # creates a bunch of motions depending on the ruleFile, and motions
        # are subclasses of transitions.

        # So, I figured this is the simpler solution, even if it is dirtier.

