# this class has a lowercase name because the ruleset can refer to it

from time import *
import copy

import Tree
from Transitions import *
from Initiative import *

class motion(initiative):
    # members:
    #   motionResult
    

    def __init__(self, state):
        initiative.__init__(self, state)
        self.motionResult = None
        self.affirmativeVotes = None
        self.negativeVotes = None

    # TODO (maybe): we've duplicated information here, violating
    # OnceAndOnlyOnce. The adopted/rejected state of motions is both in
    # the last instance of the motion, and in whether it is stored
    # in the adopted or the rejected list. Decide if this should not be
    # duplicated (actually, I think maybe this duplication is OK).
    
    def calculateVote(self, state):
        dm = self.decision_mode(state)
        if dm == True:
            return True
        if dm == "vote":
            vr = self.vote_required(state)
            if vr == "majority":
                return self.affirmativeVotes > self.negativeVotes
            if vr == "two-thirds":
                return self.affirmativeVotes >= 2 * self.negativeVotes
            raise Exception("unknown vote_required: " + `vr`)
        raise Exception("unknown decision_mode: " + `dm`)

    def motionRejected(self, state):
        newState = self.assignResultAndRemove(state, 'reject', motionRejectedTransition(self))
        return newState
        
    def motionAdopted(self, state):
        newState = self.assignResultAndRemove(state, 'adopt', motionAdoptedTransition(self))
        return newState

    def assignResultAndDetach(self, state, result, transition = None, descendentLabel = 'discard'):
        newMotion = copy.deepcopy(self)
        newMotion.motionResult = result
        newMotion.youAreCurrent()
        (newState, subtree) = state.detach_initiative(self, descendentLabel)
        if transition:
            newState.prevTransition = transition
        newState.motionTables[result].append(newMotion)
        return (newState, subtree)
    

    def assignResultAndRemove(self, state, result, transition = None):
        if self.motionResult == result:
            # the result is already what we want; no change
            return state

        newMotion = copy.deepcopy(self)
        newMotion.motionResult = result
        newMotion.youAreCurrent()
        newState = state.unapply_initiative(self)
        if transition:
            newState.prevTransition = transition
        newState.motionTables[result].append(newMotion)
        return newState
    #TODO: maybe replace with assignResultAndDetach

        

    def getCurrentMotionResult(self):
        return self.motionResult
    
    def getMotionResult(self):
        return self.fate.latest().motionResult

    def getCurrentMotionResultInPastTense(self):        
        return self.motionResultTextToPastTense(self.getMotionResult())

    def getMotionResultInPastTense(self):
        return self.motionResultTextToPastTense(self.fate.latest().getMotionResult())


    def motionResultTextToPastTense(self, text):
        d = {'adopt' : 'adopted', \
             'reject' : 'rejected', \
             'withdraw' : 'withdrawn', \
             'discard' : 'discarded',
             'table' : 'tabled'}
        result = d.get(text)
        if not result: #fail gracefully
            result = text

        return result


