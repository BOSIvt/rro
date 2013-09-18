from Action import *
from InitiativeFate import *

# this class has a lowercase name because the ruleset can refer to it

class initiative(action):
    # todo: maybe change to "action"

    # members:
    #   fate
    #   prevCurPosition
    #   target_choices_at_time_of_application
    
    def __init__(self, state):
        action.__init__(self, state)
        self.fate = InitiativeFate(self)
        self.prevCurPosition = state.position
        self.target_choices_at_time_of_application = None

        ##
        ## get default target, if there are any
        ##
        targets = self.find_targets(state)

        if targets:
            self.canHaveTarget = True
            self.target = targets[0]


    def parentInitiative(self):
        return self.prevCurPosition.contents
    #TODO: this isn't quite correct

    def youAreCurrent(self):
        self.fate.current = self

    def applyTo(self, state, args):
        self.rememberCurrentTargetChoices(state)
        state.addInitiativeTo(self, state.prevMotion())

        

    def rememberCurrentTargetChoices(self, state):
        self.target_choices_at_time_of_application = self.find_targets(state)


    def targetChoicesAtTimeOfApplicationOrNow(self, state):
        if self.target_choices_at_time_of_application != None:
            return self.target_choices_at_time_of_application
        else:
            return self.find_targets(state)

        #TODO: move to Parliament, remove state argument

class RootInitiative(initiative):
    pass
