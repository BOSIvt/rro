#!/usr/bin/python


# to fix a bug in Debian
import sys
sys.path.insert(0, '/usr/lib/python2.3/site-packages/wx-2.5.3-gtk2-unicode')

# imports required by mcmillan installer
from PythonCard.components import button,  statictext, imagebutton, textfield,  textarea, multicolumnlist, checkbox, tree
####

import customDialogs

from time import *
from calendar import *
from string import *

import Action
import Parliament
from PythonCard import dialog, model
import wx
import pickle
from re import *

import meeting_helper_displayOnly

class Preferences:
    pass

class ParliamentGUI(model.Background):

    #########################################
    #########################################
    ##
    ## Event Handlers
    ##
    #########################################
    #########################################

    def do_initialize(self,event):

        self.selectedAction = None
        self.ignoreTheRules = False
        self.showUnimplemented = False
        self.mainWindowIsUpdating = False
        self.currentSavePath = None

        self.prefs = Preferences()
        self.init_gui_prefs()

        self.initializeList()
        self.hideTargetFields()
        #self.components.actionInfo.SetEditable(True)
        self.statusChanged()

    def init_gui_prefs(self):
        self.prefs.showMoverField = True
        self.prefs.showTargetField = True
        self.prefs.showMeetingHistory = True
        self.prefs.displayInterruptColumn = True
        self.prefs.displaySecondColumn = True
        self.prefs.displayCategoryColumn = False
        self.prefs.displayPurposeColumn = False



    #########################################
    #########################################
    ##
    ## Subroutines
    ##
    #########################################
    #########################################

    #########################################
    ## Initialization subroutines
    #########################################

    def initializeList(self):
        list = self.components.list

        self.preferredListSortColumn = 1 

        list.InsertColumn(0, "motions now in order")
        list.InsertColumn(1, "class")
        if self.prefs.displayInterruptColumn:
            list.InsertColumn(2, "w/o floor")
        if self.prefs.displaySecondColumn:
            list.InsertColumn(3, "second")
        if self.prefs.displayCategoryColumn:
            list.InsertColumn(4, "category")
        if self.prefs.displayPurposeColumn:
            list.InsertColumn(5, "purpose")  

        list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        if self.prefs.displayInterruptColumn:
            list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        if self.prefs.displaySecondColumn:
            list.SetColumnWidth(3, wx.LIST_AUTOSIZE)
        if self.prefs.displayCategoryColumn:
            list.SetColumnWidth(4, wx.LIST_AUTOSIZE)
        if self.prefs.displayPurposeColumn:
            list.SetColumnWidth(5, wx.LIST_AUTOSIZE)

        # show how to select an item
#        list.SetItemState(5, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)

        # these are still needed if you want the events
        #wx.EVT_LIST_ITEM_ACTIVATED(self.panel, -1, self.on_list_itemActivated)
        #wx.EVT_LIST_COL_CLICK(self.panel, -1, self.on_list_columnClick)

    #########################################
    ## Update subroutines
    #########################################

    def statusChanged(self):
        self.updateThisWindow()

    def updateThisWindow(self):
        # print 'DBG5'

        list = self.components.list
        global validActs
        validActs = self.p.currentValidActs()
        if self.ignoreTheRules:
            validActs = self.p.nonAbstractActInternalNames()

        if not self.showUnimplemented:
            validActs = filter(lambda act: not self.p.getTransition(act).unimplemented(self.p.curState), validActs)

#        print self.p.getTransition('motion_related_to_voting').unimplemented(self.p.curState)

        list.DeleteAllItems()
        for actIndex in range(len(validActs)):
            act = validActs[actIndex]
            actName = self.p.getTransition(act).name
            actTypeInternal = self.p.getTransition(act).type(self.p.getCurrentState())
            # todo: soon, that wont need an argument
            actType = self.p.getTransitionName(actTypeInternal)
            actType = sub(r' motion',r'',actType)
            actInterrupt = {True: "may interrupt", False: ""}[self.p.getTransition(act).may_interrupt(self.p.curState)]
            actSecond = {True: "", False: "no second"}[self.p.getTransition(act).must_be_seconded(self.p.curState)]
            actCategory = self.p.getTransition(act).category(self.p.getCurrentState())
            actPurpose = self.p.getTransition(act).purpose(self.p.getCurrentState())

            list.itemDataMap[actIndex] = {}
            list.InsertStringItem(actIndex, actName)
            list.SetStringItem(actIndex, 0, actName)
            list.itemDataMap[actIndex][0] = actName
            list.SetStringItem(actIndex, 1, actType)
            list.itemDataMap[actIndex][1] = self.p.getTransition(act).type_precedence(self.p.getCurrentState()) + self.p.getTransition(act).motion_precedence(self.p.getCurrentState())
            if self.prefs.displayInterruptColumn:
                list.SetStringItem(actIndex, 2, actInterrupt)
                list.itemDataMap[actIndex][2] = actInterrupt
            if self.prefs.displaySecondColumn:
                list.SetStringItem(actIndex, 3, actSecond)
                list.itemDataMap[actIndex][3] = actSecond
            if self.prefs.displayCategoryColumn:
                list.SetStringItem(actIndex, 4, actCategory)
                list.itemDataMap[actIndex][4] = actCategory
            if self.prefs.displayPurposeColumn:
                list.SetStringItem(actIndex, 5, actPurpose)
                list.itemDataMap[actIndex][5] = actPurpose
            list.SetItemData(actIndex, actIndex)
# doesn't work #            list.GetItem(actIndex).SetTextColour(wx.RED)

        list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        list.SetColumnWidth(3, wx.LIST_AUTOSIZE)

        list.SortListItems(self.preferredListSortColumn)

        self.updateInitiativeTree()
        self.updateHistoryView()
        self.updateFields()

    def updateHistoryView(self):
        guiHistory = self.components.history
        historyNamesString = self.getHistoryString()
        guiHistory.SetValue(historyNamesString)
#       guiHistory.SetInsertionPointEnd()
        guiHistory.SetInsertionPoint(guiHistory.GetLastPosition())

    def updateFields(self):
        #print 'DBG: ENTERED updateFields'
        guiSelectionObj = self.components.initiativeTree.GetSelection()
        if guiSelectionObj:
            sel = self.components.initiativeTree.GetItemData(guiSelectionObj).GetData()
            #print "DBG: sel="+ `sel`
            if sel:
                self.selectedAction = sel
                self.components.actionInfo.SetValue(sel.notes)
                self.components.actionInfo.SetEditable(True)
                #print 'value='+sel.notes
                self.updateMoverField()
                self.updateTargetFields()
                self.updateMotionRules()
                self.updateVoteFields()

    def updateVoteFields(self):
        pass

    def updateMoverField(self):
        action = self.selectedAction
        if action and not isinstance(action, self.p.RootInitiative):
            if action.actor:
                self.components.moverField.text = action.actor
            else:
                self.components.moverField.text = ''
            self.showMoverField()
        else:
            self.hideMoverField()

    def updateTargetFields(self):
        action = self.selectedAction
        if self.p.isAction(action) and action.canHaveTarget:
            if action.target:
                self.components.TargetText.text = self.textIDOfAction(action.target)
            else:
                self.components.TargetText.text = ''
            self.showTargetFields()
            if len(action.targetChoicesAtTimeOfApplicationOrNow(self.p.curState)) > 1:
                self.components.TargetChangeButton.visible = True
        else:
            self.hideTargetFields()

    def updateMotionRules(self):
        action = self.selectedAction
        d = {True: "debatable; ", False: "undebatable; "}
        rules = ""
#       if "must_be_seconded" in dir(action):
#           rules += "second: " + yn[action.must_be_seconded(self.p.curState)]
        if "debatable" in dir(action) and action.debatable(self.p.curState) in d.keys():
            rules += str(d.get(action.debatable(self.p.curState)))
        if "vote_required" in dir(action):
            try:
                rules += str(action.vote_required(self.p.curState)) + " vote"
            except ValueError:
                pass
        self.components.motionRules.SetLabel(rules)

    def updateInitiativeTree(self):
        tree = self.p.getInitiativeTree()
        guiTree = self.components.initiativeTree
        guiTree.DeleteAllItems()

        root = self.p.getInitiativeTreeRoot()
        guiRoot = guiTree.AddRoot("Beginning of meeting")

        self.guiTreePendingInitiative = guiRoot # default

        self.updateInitiativeSubTree(tree, root,guiRoot)

        guiTree.SelectItem(self.guiTreePendingInitiative)
        guiTree.ScrollTo(self.guiTreePendingInitiative)
          # unnecessary: implicit in SelectItem, and doesn't do
          # horizontal scrolling, anyway
          # todo: horizontal scrolling?
          # todo: only makes sense for serial rulesets

    def updateInitiativeSubTree(self, tree, subroot, guiSubroot):
        guiTree = self.components.initiativeTree

        guiTree.GetItemData(guiSubroot).SetData(subroot.contents)

        if subroot.contents in self.p.getOpenInitiatives(): 
            self.guiTreePendingInitiative = guiSubroot

        children = tree.children(subroot)

        if children:
            guiTree.SetItemHasChildren(guiSubroot, 1)
            for child in children:
                guiChild = guiTree.AppendItem(guiSubroot, self.textIDOfAction(child.contents))
                self.updateInitiativeSubTree(tree, child, guiChild)
            guiTree.Expand(guiSubroot)

    #########################################
    ## Helper subroutines
    #########################################

    def selectedActionIsCurrentlyPendingMotion(self):
        #print 'DBG: S.A.I.C.P.M'
        #print '  '+`self.selectedAction`
        #print '  '+`self.p.getOpenInitiatives()[0]`
        return self.selectedAction == self.p.getOpenInitiatives()[0]

    def saveAs(self):
        wildcard = "*.mtg"
        result = dialog.saveFileDialog(wildcard=wildcard)

        if result.accepted:
            path = result.paths[0]
            if not match(r'.*\.mtg$', path):
                path = path + '.mtg'
                # note (todo?): since this isn't integrated into
                # saveFileDialog, weird stuff can happen like if you
                # type /tmp/test, and there's already a /tmp/test, it'll
                # ask you if you want to overwrite it, but then if you confirm
                # it'll save to /tmp/test.mtg
            self.currentSavePath = path
            pickle.dump(self.p,open(path,'w'))

    def getColumnText(self, index, col):
        item = self.components.list.GetItem(index, col)
        return item.GetText()



    def getInitiativeMeetingMinutesTextEntry(self, initiative):
        initiative = initiative.fate.latest()
        #result = strftime('%H:%M',localtime(timegm(initiative.timeInitiated))) + ': '
        result = ''
        

        if isinstance(initiative, self.p.getTransitionClass('RootInitiative')):
            result += "Meeting date: " + strftime(r'%F',localtime(timegm(initiative.timeInitiated))) + '\n\n' + "Called to order at " + strftime('%H:%M',localtime(timegm(initiative.timeInitiated))) + '\n'




        if isinstance(initiative, self.p.getTransitionClass('initiative')):
            if isinstance(initiative, self.p.getTransitionClass('motion')): 

                if (
                        isinstance(initiative, self.p.getTransitionClass('main_motion')) 
                        or

                        isinstance(initiative, self.p.getTransitionClass('point_of_order'))
                        or
                        isinstance(initiative, self.p.getTransitionClass('appeal_from_decision_of_chair'))
                        or
                        (initiative.getMotionResult() == 'adopt')
                    ):
                        
                        result += '\n' + initiative.name

                        if initiative.actor:
                            result += ', moved by ' + initiative.actor

                        if initiative.getMotionResultInPastTense():
                            result += ', ' + initiative.getMotionResultInPastTense()
                            if getattr(initiative,"affirmativeVotes") \
                                   and initiative.affirmativeVotes:
                                a = initiative.affirmativeVotes
                                n = initiative.negativeVotes
                                result += " %d-%d" % (a,n)

                        result += '.'

                        #moverText = initiative.actor or '[name?]'
                        #resultText =  initiative.getMotionResultInPastTense() or '[no result]'
                        #if initiative.getMotionResultInPastTense():
                        

                        #textOfMotion = initiative.notes or '[nothing recorded]'


                        #result += '%s, moved by %s, %s.' % (initiative.name, moverText, resultText) 

                        if initiative.notes:
                            result += ' As proposed:\n%s' % initiative.notes


#        if isinstance(initiative, self.p.getTransitionClass('initiative')):
#            if initiative.target:
#                result += '; target=' + self.textIDOfAction(initiative.target)



        return result


    def getInitiativeHistoryTextEntry(self, initiative):
        initiative = initiative.fate.latest()
        result = strftime('%H:%M',localtime(timegm(initiative.timeInitiated))) + ': '
        result += initiative.name
        if isinstance(initiative, self.p.getTransitionClass('RootInitiative')):
            result += "Meeting began"

        if isinstance(initiative, self.p.getTransitionClass('initiative')):
            if initiative.target:
                result += '; target=' + self.textIDOfAction(initiative.target)

        if isinstance(initiative, self.p.getTransitionClass('initiative')):
            if isinstance(initiative, self.p.getTransitionClass('motion')): 
                r = initiative.getMotionResultInPastTense()
                if r:
                    if getattr(initiative,"affirmativeVotes") \
                       and initiative.affirmativeVotes:
                        a = initiative.affirmativeVotes
                        n = initiative.negativeVotes
                        result += " (%s %d-%d)" % (r,a,n)
                    else:
                        result += " (%s)" % (r)

            if initiative.notes:
                result += ': ' + initiative.notes

        return result

    def getHistoryString(self):
        history = self.p.getMeetingEventHistory()

        historyNames = [self.getInitiativeHistoryTextEntry(self.p.getInitiativeTreeRoot().contents)] + [self.getInitiativeHistoryTextEntry(initiative) for initiative in history]

        historyNamesString = join(historyNames, '\n')
#       historyNamesString = 'Meeting history\n-----------------\n\n' + historyNamesString

        return historyNamesString
#        return self.getMeetingMinutesString() # for debugging
    
    def getMeetingMinutesString(self):
        history = self.p.getMeetingEventHistory()

        historyNames = [self.getInitiativeMeetingMinutesTextEntry(self.p.getInitiativeTreeRoot().contents)] + [self.getInitiativeMeetingMinutesTextEntry(initiative) for initiative in history]

        historyNamesString = join(historyNames, '\n')
#       historyNamesString = 'Meeting history\n-----------------\n\n' + historyNamesString

        return historyNamesString



    def hideMoverField(self):
        self.components.moverField.visible = False
        self.components.moverLabel.visible = False

    def showMoverField(self):
         if self.prefs.showMoverField:
             self.components.moverField.visible = True
             self.components.moverLabel.visible = True

    def hideTargetFields(self):
        self.components.TargetText.visible = False
        self.components.targetLabel.visible = False
        self.components.TargetChangeButton.visible = False

    def showTargetFields(self):
        if self.prefs.showTargetField:
            self.components.TargetText.visible = True
            self.components.targetLabel.visible = True

    def textIDOfAction(self, action):
        if self.p.isAction(action):
            result = action.name + ' (' + strftime('%H:%M',localtime(timegm(action.timeInitiated))) + ')'
        else:
            return ''
        return result

    def showActionInfo(self, action):
        #print 'DBG: entered showActionInfo'

        actionInfo = self.components.actionInfo
        summary = self.p.getTransition(action).summary(self.p.getCurrentState())
            # todo: soon, that wont need an argument
        if summary:
            self.components.actionInfo.SetEditable(False)
            actionInfo.SetValue(summary)
        else:
            self.components.actionInfo.SetEditable(False)
            actionInfo.SetValue('')
            pass

        

    def featureNotImplementedYet(self):
        result = dialog.messageDialog(self, 'This feature not implemented yet.', 'Not implemented',
                               wx.ICON_EXCLAMATION |
                               wx.OK)

class ParliamentMainWindow(ParliamentGUI):

    def on_initialize(self,event):
        self.displayOnlyWindow = model.childWindow(self, meeting_helper_displayOnly.ParliamentDisplayOnlyWindow)

        self.setParliamentInstance(Parliament.Parliament())
        self.p.initState()

        self.displayOnlyWindow.setParliamentInstance(self.p)
        ParliamentGUI.do_initialize(self,event)

    #########################################
    ## Event handlers: available actions list
    #########################################

    def on_list_select(self, event):
        event.skip()
        self.currentItem = event.m_itemIndex
        item = self.components.list.GetItem(self.currentItem)
        action = validActs[self.components.list.GetItemData(self.currentItem)]
        self.selectedAction = self.p.getTransition(action)
        #print 'DBG: on_list_select: '+`self.selectedAction`
        self.showActionInfo(action)
        self.hideMoverField()
        self.updateTargetFields()

    def on_list_mouseDoubleClick(self, event):
        event.skip()

    def on_list_itemActivated(self, event):
        event.skip()
        self.currentItem = event.m_itemIndex
        item = self.components.list.GetItem(self.currentItem)
        action = validActs[self.components.list.GetItemData(self.currentItem)]
        self.p.applyToDefaultPosition(action)
        #TODO: doesn't quite make sense for non-initiatives
        self.statusChanged()

    def on_list_columnClick(self, event):
        event.skip()
        self.preferredListSortColumn = event.GetColumn()
        self.components.list.SortListItems(self.preferredListSortColumn)

    def on_list_keyDown(self, event):
        event.skip()

    #########################################
    ## Event handlers: menus
    #########################################

    def on_menuFileExit_select(self, event):
        event.skip()
        self.Close()

    def on_menuFileStartOver_select(self, event):
        event.skip()
        result = dialog.messageDialog(self, 'Clear all? Are you sure?', 'Are you sure?',
                               wx.ICON_INFORMATION |
                               wx.YES_NO | wx.NO_DEFAULT)
        if result.accepted:
            self.p.initState()
            self.statusChanged()

    def on_menuLoadRuleset_select(self, event):
        event.skip()
        result = dialog.messageDialog(self, 'Currently, loading a new ruleset will CLEAR ALL MEETING HISTORY AND STATUS, just like Start Over. Are you sure you want to clear all?', 'Are you sure?',
                               wx.ICON_EXCLAMATION |
                               wx.YES_NO | wx.NO_DEFAULT)

        if result.accepted:
            wildcard = "Ruleset files (*_ruleset.py)|*_ruleset.py|All Files (*.*)|*.*"
            result = dialog.openFileDialog(wildcard=wildcard)

            if result.accepted:
                path = result.paths[0]
                global p
                self.setParliamentInstance(Parliament.Parliament(path))
                self.p.initState()
                self.statusChanged()

    def on_menuLoadMeetingState_select(self, event):
        event.skip()
        wildcard = "Meeting files (*.mtg)|*.*"
        result = dialog.openFileDialog(wildcard=wildcard)


        if result.accepted:
            path = result.paths[0]
            self.currentSavePath = path
            global p
            self.setParliamentInstance(pickle.load(open(path)))
            self.statusChanged()


    def on_menuSave_select(self, event):
        event.skip()
        if self.currentSavePath:
            pickle.dump(self.p,open(self.currentSavePath,'w'))
        else:
            self.saveAs()

    def on_menuSaveAs_select(self, event):
        event.skip()
        self.saveAs()

    def on_menuSaveMeetingMinutesAsFile_select(self, event):
        event.skip()
        wildcard = "*.txt"
        result = dialog.saveFileDialog(wildcard=wildcard)

        if result.accepted:
            path = result.paths[0]
#           apparently the Windows GUI appends .txt too, so this is redundant
#           if not match(r'\.txt$', path):
#              path = path + '.txt'
                # note (todo?): since this isn't integrated into
                # saveFileDialog, weird stuff can happen like if you
                # type /tmp/test, and there's already a /tmp/test, it'll
                # ask you if you want to overwrite it, but then if you confirm
                # it'll save to /tmp/test.txt

            f = open(path,'w')
            f.write(self.getMeetingMinutesString())
            f.close()

    def on_menuNavigationGoBack_select(self, event):
        event.skip()
        self.p.goBack()
        self.statusChanged()

    def on_menuNavigationGoFwd_select(self, event):
        event.skip()
        self.p.goFwd()
        self.statusChanged()

    def on_menuNavigationMotionAdopted_select(self, event):
        event.skip()
        self.p.motionAdopted()
        self.statusChanged()

    def on_menuNavigationMotionRejected_select(self, event):
        event.skip()
        self.p.motionRejected()
        self.statusChanged()

    #########################################
    ## Event handlers: initiative tree stuff
    #########################################

    def on_initiativeTree_gainFocus(self, event):
        event.skip()
        self.on_initiativeTree_selectionChanged(event)

    def on_initiativeTree_selectionChanged(self, event):
        event.skip()
        self.updateFields()

    #########################################
    ## Event handlers: action attributes
    #########################################

    def on_moverField_loseFocus(self, event):
        event.skip()

        obj = self.selectedAction
        obj.actor = self.components.moverField.GetValue()

    def on_TargetChangeButton_mouseClick(self, event):
        event.skip()
#        result = customDialogs.TreeSelectAncestorDialog(self, 'Choose target motion', 'Please select a target for "' + self.selectedAction.name + '"', self.components.initiativeTree)
        # more generally, this is a target INITIATIVE. However, since we made that term up, we can say "motion" here

#        choiceList = [self.textIDOfAction(target) for target in self.selectedAction.targetChoicesAtTimeOfApplicationOrNow(self.p.curState)])
        targetList = self.selectedAction.targetChoicesAtTimeOfApplicationOrNow(self.p.curState)
#        for target in targetList:
#            target.__str__ = self.textIDOfAction(target)

#        result = dialog.singleChoiceDialog(self, 'Please select a target for "' + self.selectedAction.name + '"', 'Choose target motion', targetList)
        result = customDialogs.SingleChoiceInitiativeListDialog(self, 'Choose target motion', 'Please select a target for "' + self.selectedAction.name + '"',  targetList, p)

        if result.accepted:
            self.selectedAction.target = result.selection
            self.statusChanged()

        # TODO: better selector

    #########################################
    ## Event handlers: misc stuff
    #########################################

    def on_BackBtn_mouseClick(self, event):
        event.skip()
        self.p.goBack()
        self.statusChanged()

    def on_FwdBtn_mouseClick(self, event):
        event.skip()
        self.p.goFwd()
        self.statusChanged()

    def on_AdoptedBtn_mouseClick(self, event):
        event.skip()
        self.p.motionAdopted()
        self.statusChanged()

    def on_RejectedBtn_mouseClick(self, event):
        event.skip()
        self.p.motionRejected()
        self.statusChanged()

    def on_recordVoteButton_mouseClick(self, event):
        event.skip()
        motion = self.p.getOpenInitiatives()[0]
        try:
            self.p.finalizeVote(motion, int(self.components.affirmativeVotes.GetValue()), int(self.components.negativeVotes.GetValue()))
            self.statusChanged()
        except ValueError, AttributeError:
            pass

    def on_IgnoreRulesCheckBox_mouseClick(self, event):
        event.skip()
        self.ignoreTheRules = self.components.IgnoreRulesCheckBox.checked
        self.statusChanged()

    def on_ShowUnimplementedCheckbox_mouseClick(self, event):
        event.skip()
        self.showUnimplemented = self.components.ShowUnimplementedCheckbox.checked
        self.statusChanged()

    def setParliamentInstance(self, p):
        self.p = p
        self.displayOnlyWindow.setParliamentInstance(self.p)

    def updateThisWindow(self):
        if self.mainWindowIsUpdating:
            #print 'entered loop'
#            while self.mainWindowIsUpdating:
#                pass
            return

        self.mainWindowIsUpdating = True
        ParliamentGUI.updateThisWindow(self)

        self.mainWindowIsUpdating = False

    def updateVoteFields(self):
        self.components.affirmativeVotes.SetValue('')
        self.components.negativeVotes.SetValue('')

    def on_menuViewDisplayOnlyWindow_select(self, event):
        if self.menuBar.getChecked('menuViewDisplayOnlyWindow'):
            self.displayOnlyWindow.updateThisWindow()
            self.displayOnlyWindow.visible = True
        else:
            self.displayOnlyWindow.visible = False

    def statusChanged(self):
        # print 'DBG3'
        self.updateThisWindow()
        if self.displayOnlyWindow.visible:
            # print 'DBG4'
            # print `self.displayOnlyWindow`
            self.displayOnlyWindow.updateThisWindow()


    def on_actionInfo_textUpdate(self, event):
        event.skip()
        #print 'DBG111'
        #print `dir(self.displayOnlyWindow.components.actionInfo)`
        #print 'DBG222'
        if self.components.actionInfo.editable:
            if self.selectedActionIsCurrentlyPendingMotion():
                self.displayOnlyWindow.components.actionInfo.SetValue(self.components.actionInfo.GetValue())
                self.displayOnlyWindow.components.actionInfo.SetInsertionPoint(self.components.actionInfo.GetInsertionPoint())
            obj = self.selectedAction
            #print obj
            if obj.notes != self.components.actionInfo.GetValue():
                obj.notes = self.components.actionInfo.GetValue()
                #print "DBG: WROTE NOTE " + obj.notes

if __name__ == '__main__':
    app = model.Application(ParliamentMainWindow)    
    app.MainLoop()
