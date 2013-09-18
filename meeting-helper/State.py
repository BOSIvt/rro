# this class has a lowercase name because the ruleset can refer to it

from time import *
import copy

import Tree
from Transitions import *
from Initiative import *
from InitiativeFate import *
from Motion import *

class state:

    
    def __init__(self, args):
        self.initiativeTree = Tree.Tree()

        self.topID = 0

        self.root = self.initiativeTree.add_vertex()
        self.position = self.root
        self.root.contents = self.initInitiativeTreeRoot(args)
        self.prevTransition = None

        self.motionTables = {}
        self.motionTables['adopt'] = []
        self.motionTables['reject'] = []
        self.motionTables['withdraw'] = []
        self.motionTables['discard'] = []
        self.motionTables['table'] = []

        self.subtreeTables = {}
        self.subtreeTables['table'] = []

        self.currently_voting = False

    def initInitiativeTreeRoot(self, args):
        newroot = RootInitiative(self)
        newroot.setID(self.topID)
        self.topID += 1
        return newroot
        # this fn is just so that subclasses can override

    def initialStateAllowsApplicationOf(self, state, initiative):
        return True
    
#    def openForPrincipalMotion(self):
#        return True

    def motionAt(self, position):
        return position.contents

    def addInitiativeAtPosition(self, initiativeClass, position, args):
        initiative = initiativeClass(self)
        self.position = position
        initiative.applyTo(self, args)        
        initiative.fate = InitiativeFate(initiative)
        initiative.timeInitiated = gmtime()
          # have to set manually here to distinguish from automated deepcopy "creation"
        initiative.setID(self.topID)
        self.topID += 1

        return initiative
        
    def apply(self, initiativeClass, position, args):
        newState = copy.deepcopy(self)        
        initiative = newState.addInitiativeAtPosition(initiativeClass, position, args)
        newState.prevTransition = initiative
        self.beginning_of_meeting = False
        return newState

    def prevMotion(self):
        return self.getPendingMotion()
        #todo: this fn should be made obsolete and removed

    def getLiveInitiatives(self):
        return [node.contents for node in self.initiativeTree.all_nodes()
                if not isinstance(node.contents, RootInitiative)]

    def getPendingMotion(self):
        return self.motionAt(self.position)
#       if not isinstance(motion, RootInitiative):
#           return motion
#       else:
#           return None

    def getOpenInitiatives(self):
         #TODO: return self.initiativeTree.leaves() (generalized for parallel)
        return [self.motionAt(self.position)]


    def positionOfPrevMotion(self):
        return self.position

# TODO: confusing name
    def addInitiativeTo(self, initiative, position):
        newVertex = self.initiativeTree.add_vertex(initiative)
        newArc = self.initiativeTree.add_edge(self.position, newVertex)

        self.position = newVertex
        
        
    def askUser(self, trueOrFalseQuestion):
        #todo: call handler or throw exception
        return True
        # true by default

    def motionRejected(self):
        if isinstance(self.getPendingMotion(), motion):
            return self.getPendingMotion().motionRejected(self)
        else:
            # todo: throw err?
            return self

    def motionAdopted(self):
        if isinstance(self.getPendingMotion(), motion):
            return self.getPendingMotion().motionAdopted(self)
        else:
            # todo: throw err?
            return self

    def detach_initiative(self, initiative, descendentLabel = 'discard', args = None):
        newState = copy.deepcopy(self)
        position = newState.findPositionOf(initiative)
        parents = self.initiativeTree.parents(position)
        subtree = newState.detachSubtreeAtPosition(position, descendentLabel, args)
        newState.position = parents[0] #only 1 parent here
        return (newState, subtree)
        
    
    def unapply_initiative(self, initiative, descendentLabel = 'discard', args = None):
        newState = copy.deepcopy(self)
        position = newState.findPositionOf(initiative)
        prevCurPos = newState.findPositionOf(initiative.prevCurPosition.contents)
        parents = self.initiativeTree.parents(position)
        newState.removeSubtreeAtPosition(position, descendentLabel, args)
        newState.position = prevCurPos
        return newState
    #TODO: maybe make this a special case of detach_initiative

    def findPositionOf(self, initiative):
        return self.initiativeTree.find_vertex_with_contents(initiative)
        

    def removeSubtreeAtPosition(self, position, descendentLabel, args = None):
        deletednodes = self.initiativeTree.delete_subtree(position)

        discardedInitiatives = [node.contents for node in deletednodes]
        discardedInitiatives.remove(position.contents)
        [self.markAs(initiative, descendentLabel) for initiative in discardedInitiatives]
            
        #TODO: don't we need a real delete?

    def detachSubtreeAtPosition(self, position, descendentLabel,  args = None):
        c = position.contents
        subtree = self.initiativeTree.detach_subtree(position)

        discardedInitiatives = [node.contents for node in subtree.all_nodes()]
        discardedInitiatives.remove(c)
        [self.markAs(initiative, descendentLabel) for initiative in discardedInitiatives]
        

        return subtree

    def appendSubtreeAtPosition(self, subtree, subtreeRoot, position, args = None):
         return self.initiativeTree.append_subtree(position, subtree, subtreeRoot)


    def reparent(self, initiative, newParentInitiative):
        childPos = self.findPositionOf(initiative)
        newParentPos = self.findPositionOf(newParentInitiative)
        self.initiativeTree.reparent(childPos, newParentPos)


    def markAs(self, initiative, label):
        newInitiative = copy.deepcopy(initiative)
        newInitiative.motionResult = label
        newInitiative.youAreCurrent()        
        self.motionTables['discard'].append(newInitiative)

        

    def youAreCurrent(self):
        # tell all initiatives to tell their fates that they
        # are the most current versions

        allNodesInTree = self.initiativeTree.all_nodes()
        allInitiativesInTree = [n.contents for n in allNodesInTree]
        [t.youAreCurrent() for t in allInitiativesInTree]

        for key in self.motionTables.keys():
            [motion.youAreCurrent() for motion in self.motionTables[key]]

