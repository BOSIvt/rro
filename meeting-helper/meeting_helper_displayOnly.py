#!/usr/bin/python


# to fix a bug in Debian
import sys
sys.path.insert(0, '/usr/lib/python2.3/site-packages/wx-2.5.3-gtk2-unicode')

# imports required by mcmillan installer
#from PythonCard.components import button,  statictext, imagebutton, textfield,  textarea, multicolumnlist, checkbox, tree
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

from meeting_helper import *




class ParliamentDisplayOnlyWindow(ParliamentGUI):


    def on_initialize(self,event):
        self.displayWindowIsUpdating = False

        self.parent = self.GetParent()
        ParliamentGUI.do_initialize(self,event)


    def on_close(self, event):
        self.parent.menuBar.setChecked('menuViewDisplayOnlyWindow', False)
        self.visible = False

    def setParliamentInstance(self, p):
        self.p = p

    def statusChanged(self):
        self.updateThisWindow()
        self.parent.updateThisWindow()

    def hideTargetFields(self):
        pass
    
    def showTargetFields(self):
        pass

    def updateTargetFields(self):
        pass

    def updateThisWindow(self):
        # print 'DBG'
        self.ignoreTheRules = self.parent.ignoreTheRules
        print self.ignoreTheRules
        ParliamentGUI.updateThisWindow(self)

    def init_gui_prefs(self):
        ParliamentGUI.init_gui_prefs(self)
        self.prefs.showMoverField = False
        self.prefs.showTargetField = False
        self.prefs.showMeetingHistory = False
        self.prefs.displayInterruptColumn = False
        self.prefs.displaySecondColumn = False
        self.prefs.displayCategoryColumn = False
        self.prefs.displayPurposeColumn = False
        

    def updateMoverField(self):
        pass

    def updateThisWindow(self):
        if self.displayWindowIsUpdating:
            #print 'entered loop'
#            while self.displayWindowIsUpdating:
#                pass
            return
            
        self.displayWindowIsUpdating = True
        ParliamentGUI.updateThisWindow(self)

        self.displayWindowIsUpdating = False

#    def initializeList(self):
#        """inserts only 2 columns instead of 4"""
#
#        list = self.components.list
#
#        list.InsertColumn(0, "motions now in order")
#        list.InsertColumn(1, "class")
#
#        list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
#        list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
