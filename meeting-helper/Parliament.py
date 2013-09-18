#!/usr/bin/python

# imports required by mcmillan installer
#import rro_default_ruleset

####

import types, re, imp, sys
import Transitions
import Initiative
import Action
import Motion

import Default_initial_state


# maybe the word "transition" should be changed to "event"
# but then what do we call "event", as in, "meeting event history"?
# wait, maybe that's the same thing; because the difference between
# two states is called an "event" iff the "newTransitionAdded" argument to
# appendNewState was TRUE
#
# or, maybe we should call transitions "major events", but to call all
# differences between states "transitions".

class Parliament:


    #########################################
    #########################################
    ##
    ## Initialization
    ##
    #########################################
    #########################################


# todo: make a "init" compile if it has to
    
    def __init__(self, compiledRuleFilepath = None):
        """Takes one argument, the path to the compiled ruleset"""

        global rules

        if compiledRuleFilepath:
            path = sys.path
        
            m = re.search(r'^(.*/)?(.*?)(\..*)?$', compiledRuleFilepath)
            moduleName = m.group(2)
            if m.group(1):
                path.insert(0, m.group(1))
            (file, filename, description) = imp.find_module(moduleName, path)
            try:
                rules = imp.load_module(moduleName, file, filename, description)
                #print 'succ'
          #  except:
          #      pass
          #      #todo: throw errors here
            finally:
                file.close()
        else:
            import default_ruleset as rules

        
        self.RootInitiative = Initiative.RootInitiative



    def initState(self, args = None):
        """Reset everything to a new initial state"""
        self.curState = self.getInitialState(args)
        self.currentBackPosition = 0
        self.backButtonHistory = [self.curState]
        #self.meetingEventHistory = []
        self.newInitiativeTimes = [False]
        return True


    #########################################
    ## Hypothetical init methods
    #########################################


    def getInitialState(self, args = None):
        """Returns a new initial state"""
        if 'initial_state' in dir(rules): 
            return rules.initial_state(args)
        else:
            return Default_initial_state.initial_state(args) 


    #########################################
    #########################################
    ##
    ## Available initiatives, "get" methods
    ##
    #########################################
    #########################################


    def nonAbstractActInternalNames(self):
        """Returns a list of all non abstract action names in the current ruleset
        """
        
        # currently some "class names" are fake class names, i.e. the names of class factory functions. currently these are members of conditional_typed_classnames_list

        nonAbstractClasses = [getattr(rules,c)
                              for c in rules.nonabstract_classnames_list
                              if type(getattr(rules,c)) == types.ClassType]

        


        result = [c.__name__ for c in nonAbstractClasses
                               if issubclass(c, rules.action)]

        conditionalTypedActNames = [c for (c,b) in rules.conditional_typed_classnames_list
                                    if issubclass(getattr(rules,b), rules.action)
                                    ]
        # note: this will crash if the "base class of last resort" given for the conditional typed class is itself conditional typed, i.e. a fake class/class factory function!

        result.extend(conditionalTypedActNames)

        
        return result;
        
        
    def validActs(self, state):
        """Returns a list of all valid actions from the given state"""
        nonAbstractActs = [getattr(rules,c) for c in self.nonAbstractActInternalNames()]
        # includes "fake classes"

        result = [c.__name__ for c in nonAbstractActs
                  if c(state).isValid(state)]

        return result



    def currentValidActs(self):
        """Returns a list of all valid actions from the current state"""
        return self.validActs(self.curState)


    def getCurrentState(self):
        """Get the current state."""
        return self.curState

    def getOpenInitiatives(self):
        """Get the pending motion in the current state."""
        return self.curState.getOpenInitiatives()


    def getTransition(self, internalNameOfTransition):
        """Get an instance of the transition of the given name, as if it were made in the current state"""

        transitionClass = getattr(rules, internalNameOfTransition)
        transition = transitionClass(self.curState)
        return transition

    def getTransitionClass(self, internalNameOfTransition):
        """Get a class object for the transition of the given name"""

        transitionClass = getattr(rules, internalNameOfTransition)
        return transitionClass


    def getTransitionName(self, internalNameOfTransition):
        """Get the name of the transition with the given internal name."""
        transitionClass = getattr(rules, internalNameOfTransition)
        transition = transitionClass(self.curState)
        return transition.name

    def getInitiativeTreeRoot(self):
        """Get the root of the initiative tree."""
        return self.curState.root

    def getInitiativeTree(self):
        """Get the initiative tree."""
        return self.curState.initiativeTree
    
    def getValidTargets(self, initiative):
        if initiative in types.StringTypes:
            initiative = getTransition(initiative)

        return initiative.find_targets(self)

    def getDefaultTarget(self, initiative):
        targets = self.getValidTargets(initiative)

        if targets:
            return targets[0]
        else:
            return None
        # TODO: test getValidTargets and getDefaultTarget


    def isAction(self, object):
        return isinstance(object, Action.action)
    # TODO: others
        


    #########################################
    #########################################
    ##
    ## Append new states, initiatives, take action
    ##
    #########################################
    #########################################



#
# newInitiativeAdded is boolean; it will be appended to newInitiativeTimes
#
    def appendNewState(self, newState, newInitiativeAdded):
        """Append the given state to the state history; newInitiativeAdded is boolean and should be True if there was a new initiative added in this state transition."""

        if newState == self.curState:
            return

        self.curState = newState

        toBeDeletedLen = len(self.backButtonHistory) - self.currentBackPosition - 1
        if toBeDeletedLen:
            self.backButtonHistory = self.backButtonHistory[0:(self.currentBackPosition+1)]
            self.newInitiativeTimes = self.newInitiativeTimes[0:(self.currentBackPosition+1)]
        
            #print self.backButtonHistory
        

#            self.meetingEventHistory = self.meetingEventHistory[0:-toBeDeletedLen]

        self.currentBackPosition += 1
        self.backButtonHistory.append(self.curState)

        self.newInitiativeTimes.append(newInitiativeAdded)

        newState.youAreCurrent()


    def apply(self, initiativeInternalName, position, args = None):
        """Apply the specified initiative to the current state at the given position."""
        self.appendNewState(
            self.curState.apply(getattr(rules, initiativeInternalName), position, args)
            , True)
            

    def applyToDefaultPosition(self, initiativeName, args = None):
        """Apply the specified initiative to the current state at the default position. Deprecated."""
        if self.getTransition(initiativeName).requires_target(self.curState):
            try:
                initiative = self.getTransition(initiativeName)
                parent = initiative.find_targets(self.curState)[0]
                parent_pos = self.curState.findPositionOf(parent)
                self.apply(initiativeName, parent_pos, args)
            except ValueError:
                raise ParliamentError()
        else:
            self.apply(initiativeName,
                       self.curState.root, args)
        # TODO: just use default args in "apply"


    def reparent(self, initiative, newParentInitiative):
        self.curState.reparent(initiative, newParentInitiative)

    # TODO: should take a motion as an argument
    def motionRejected(self):
        """Reject the pending motion, and add the appropriate new state and state transition to the state history."""
        self.appendNewState(self.curState.motionRejected(), False)

    # TODO: should take a motion as an argument
    def motionAdopted(self):
        """Adopt the pending motion, and add the appropriate new state and state transition to the state history."""
        self.appendNewState(self.curState.motionAdopted(), False)

    def finalizeVote(self, motion, affirmativeVotes, negativeVotes, abstainVotes = None):
        """Determine the fate of a motion based on its affirmative and negative votes and the vote required."""

        motion.affirmativeVotes = affirmativeVotes
        motion.negativeVotes = negativeVotes

        #TODO: record abstain

#        if motion.calculateVote(self.curState, affirmativeVotes, negativeVotes, abstainVotes):
        if motion.calculateVote(self.curState):
            self.motionAdopted()
        else:
            self.motionRejected()


    #########################################
    #########################################
    ##
    ## Handle history
    ##
    #########################################
    #########################################


    def canGoBack(self):
        """Returns True if it's possible to go farther back in the history."""
        return self.currentBackPosition > 0

    def goBack(self):
        """Go back in the history (undo)."""
        if self.canGoBack():
            self.currentBackPosition += -1
            self.curState = self.backButtonHistory[self.currentBackPosition]
            self.curState.youAreCurrent()

    def canGoFwd(self):
        """Returns True if it's possible to go farther forwards in the history."""
        return self.currentBackPosition < len(self.backButtonHistory) - 1

    def goFwd(self):
        """Go forwards in the history (redo)."""
        if self.canGoFwd():
            self.currentBackPosition += 1
            self.curState = self.backButtonHistory[self.currentBackPosition]
            self.curState.youAreCurrent()
            # TODO: setting a new curState should be a member function

    def getMeetingEventHistory(self):
        """Returns the history of initiatives which were made in the meeting (as a list ordered by the times at which the initiatives were made)."""
        return  [self.backButtonHistory[index].getPendingMotion() for index in range(self.currentBackPosition + 1) if self.newInitiativeTimes[index]]

        


