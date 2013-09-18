from PythonCard.model import CustomDialog
from PythonCard import resource
import wx
from re import *

class TreeSelectDialog(CustomDialog):
    """Select an item from a tree."""

# based on examples in PythonCard distro

    def __init__(self, aBg, name, text, tree) :
        """Initialize the defaults for the input boxes."""


        
        # build the resource which describes this particular preferences window
        aDialogRsrc = self.buildResource(name, text)

        CustomDialog.__init__(self, aBg, aDialogRsrc)

        #populate our tree with a copy of the tree passed in
        self.copyTree(tree, self.components.tree)
        

        self.parent = aBg
        self.accepted = False
        self.showModal()
        self.destroy()
        
        
    def buildResource(self, name, text):
        """This builds a string containing a resource description as you find in a .rsrc files"""

        text = text.replace("\n", "\\n")
        text = text.replace("'", "\\'")
        
        # build the body of the dialog resource string.  done first so we know the
        # total height of the whole window when we write out the main string at the end.
        bodyRSRC = " {'type':'StaticText', 'name':'labelDesc', 'position':(10,10)," + \
                  "'alignment':'center','size':(360,30),'text':'" + text + "'},"
#        bodyRSRC = bodyRSRC + " {'type':'TextArea', 'name':'labelDesc', 'position':(10,40)," + \
#                   "'size':(360,80),'text':'" + text + "'},"

        vert = 30

        bodyRSRC = bodyRSRC + \
                  "{'type':'Tree', 'name':'tree', 'position':(50, %d), " % vert + "'size':(400,400)" + " }," 
        # TREE GUI OBJ 

        vert += 420

        bodyRSRC = bodyRSRC + \
                  "{'type':'Button', 'name':'btnNone', 'position':(150, %d), " % vert + \
                  "'label':'None', 'id':5100 },"

        vert += 40

        bodyRSRC = bodyRSRC + \
                  "{'type':'Button', 'name':'btnOK', 'position':(10, %d), " % vert + \
                  "'label':'OK', 'id':5100 }," 
        
        bodyRSRC = bodyRSRC + \
                  "{'type':'Button', 'name':'btnCancel', 'position':(250, %d), " % vert + \
                  "'label':'Cancel', 'id':5100 }" + \
                  " ] } "

        vert += 60
        # construct the final resource string.
        dlgRSRC = "{'type':'CustomDialog','name':'dlgAbout'," + \
                  " 'name':'" + name + "','position':(-1,-1),'size':(500, %d),\n\n'components': [" % vert
        
        dlgRSRC += bodyRSRC
        
        # eval the resource string, pass it to Resource() and return it.
        return resource.Resource( eval(dlgRSRC) )
        

    def on_btnCancel_mouseClick(self, event):
        event.skip()

    def on_btnNone_mouseClick(self, event):
        #self.components.tree.SelectItem(self.components.tree.GetSelection(), False)
        self.components.tree.Unselect()
        pass

 
    def on_btnOK_mouseClick(self, event):
        self.selection = self.components.tree.GetItemData(self.components.tree.GetSelection()).GetData()
        #print self.selection.name
        #print self.components.tree.GetItemText(self.components.tree.GetSelection())
        self.accepted = True
        event.skip()

    def copyTree(self, oldTree,  newTree):
        oldRoot = oldTree.GetRootItem()
        newRoot = newTree.AddRoot(oldTree.GetItemText(oldRoot))

        newTree.SetPyData(newRoot, oldTree.GetItemData(oldRoot).GetData())
        self.copyTreeChildren(oldTree,  newTree, oldRoot, newRoot)
        

    def copyTreeChildren(self, oldTree,  newTree, oldTreeParent, newTreeParent):
        childCount = oldTree.GetChildrenCount(oldTreeParent, False)
        if childCount:
            (curOldChild, cookie) = oldTree.GetFirstChild(oldTreeParent)
            for curChildCount in range(childCount): 
                newItem = newTree.appendItem(newTreeParent, oldTree.GetItemText(curOldChild))
                newTree.SetPyData(newItem, oldTree.GetItemData(curOldChild).GetData())
                        
                if oldTree.GetSelection() == curOldChild:
                    newTree.selectItem(newItem)
                    newTree.ScrollTo(newItem)

                self.copyTreeChildren(oldTree, newTree, curOldChild, newItem)
                (curOldChild, cookie) = oldTree.GetNextChild(oldTreeParent, cookie)
                



class TreeSelectAncestorDialog(TreeSelectDialog):
    """Select an item from the subtree generated from the ancestors of the selected item."""

# based on examples in PythonCard distro

    def __init__(self, aBg, name, text, tree) :
        """Initialize the defaults for the input boxes."""


        
        # build the resource which describes this particular preferences window
        aDialogRsrc = self.buildResource(name, text)

        CustomDialog.__init__(self, aBg, aDialogRsrc)

        #populate our tree with a copy of the tree passed in
        #print `dir(self.components.tree.GetRootItem())`
        self.makeAncestralTree(tree, self.components.tree)
        

        self.parent = aBg
        self.accepted = False
        self.showModal()
        self.destroy()
        
        
    def makeAncestralTree(self, oldTree,  newTree):
        oldRoot = oldTree.GetRootItem()
        newRoot = newTree.AddRoot(oldTree.GetItemText(oldRoot))

        newTree.SetPyData(newRoot, oldTree.GetItemData(oldRoot).GetData())
        self.makeTreeChildren(oldTree,  newTree, oldRoot, newRoot)
        

    def makeTreeChildren(self, oldTree,  newTree, oldTreeParent, newTreeParent):
        childCount = oldTree.GetChildrenCount(oldTreeParent, False)
        if childCount:
            (curOldChild, cookie) = oldTree.GetFirstChild(oldTreeParent)
            for curChildCount in range(childCount):
                #print curChildCount
                #print childCount
                #print oldTree.GetSelection()
                #print curOldChild
                #print
                
                if oldTree.GetSelection() == curOldChild:
                    # we've hit the end of the line
                    newTree.selectItem(newTreeParent)
                    newTree.ScrollTo(newTreeParent)
                    (curOldChild, cookie) = oldTree.GetNextChild(oldTreeParent, cookie)
                else:
                    
                    newItem = newTree.appendItem(newTreeParent, oldTree.GetItemText(curOldChild))
                    newTree.SetPyData(newItem, oldTree.GetItemData(curOldChild).GetData())
                        

                    self.makeTreeChildren(oldTree, newTree, curOldChild, newItem)
                    (curOldChild, cookie) = oldTree.GetNextChild(oldTreeParent, cookie)
                





class SingleChoiceInitiativeListDialog(CustomDialog):
    """Select an initiative from a list."""

# based on examples in PythonCard distro

    def __init__(self, aBg, name, text, items, parliamentInstance) :
        """Initialize the defaults for the input boxes."""


        self.p = parliamentInstance
        
        # build the resource which describes this particular preferences window
        aDialogRsrc = self.buildResource(name, text)

        CustomDialog.__init__(self, aBg, aDialogRsrc)

        #populate our tree with a copy of the tree passed in
        #print `dir(self.components.tree.GetRootItem())`
        self.populateList(items, self.components.list)
        

        self.parent = aBg
        self.accepted = False
        self.showModal()
        self.destroy()
        
        
    def buildResource(self, name, text):
        """This builds a string containing a resource description as you find in a .rsrc files"""

        text = text.replace("\n", "\\n")
        text = text.replace("'", "\\'")
        
        # build the body of the dialog resource string.  done first so we know the
        # total height of the whole window when we write out the main string at the end.
        bodyRSRC = " {'type':'StaticText', 'name':'labelDesc', 'position':(10,10)," + \
                  "'alignment':'center','size':(360,30),'text':'" + text + "'},"
#        bodyRSRC = bodyRSRC + " {'type':'TextArea', 'name':'labelDesc', 'position':(10,40)," + \
#                   "'size':(360,80),'text':'" + text + "'},"

        vert = 30

        bodyRSRC = bodyRSRC + \
                  "{'type':'MultiColumnList', 'name':'list', 'position':(50, %d), " % vert + "'size':(400,400)" + " }," 
        # LIST GUI OBJ 

        vert += 420

        bodyRSRC = bodyRSRC + \
                  "{'type':'Button', 'name':'btnNone', 'position':(150, %d), " % vert + \
                  "'label':'None', 'id':5100 },"

        vert += 40

        bodyRSRC = bodyRSRC + \
                  "{'type':'Button', 'name':'btnOK', 'position':(10, %d), " % vert + \
                  "'label':'OK', 'id':5100 }," 
        
        bodyRSRC = bodyRSRC + \
                  "{'type':'Button', 'name':'btnCancel', 'position':(250, %d), " % vert + \
                  "'label':'Cancel', 'id':5100 }" + \
                  " ] } "

        vert += 60
        # construct the final resource string.
        dlgRSRC = "{'type':'CustomDialog','name':'dlgAbout'," + \
                  " 'name':'" + name + "','position':(-1,-1),'size':(500, %d),\n\n'components': [" % vert
        
        dlgRSRC += bodyRSRC
        
        # eval the resource string, pass it to Resource() and return it.
        return resource.Resource( eval(dlgRSRC) )
        

    def on_btnCancel_mouseClick(self, event):
        event.skip()

    def on_btnNone_mouseClick(self, event):
        #self.components.tree.SelectItem(self.components.tree.GetSelection(), False)
        self.components.list.Unselect()
        pass


    def on_list_select(self, event):
        self.currentItemDisplayIndex = event.m_itemIndex
        item = self.components.list.GetItem(self.currentItemDisplayIndex)
        realItemIndex = self.components.list.GetItemData(self.currentItemDisplayIndex)
        self.selection = self.components.list.itemDataMap[realItemIndex][0]
 
    def on_btnOK_mouseClick(self, event):
        self.accepted = True
        event.skip()

    def populateList(self, items, list):
        

        self.preferredListSortColumn = 0 
        
        list.InsertColumn(0, "Motion")
        #list.InsertColumn(1, "Type")
        #list.InsertColumn(2, "Category")
        #list.InsertColumn(3, "Purpose")  

        list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        #list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        #list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        #list.SetColumnWidth(3, wx.LIST_AUTOSIZE)


        for itemIndex in range(len(items)):
            item = items[itemIndex]
            actName = item.name
            actTypeInternal = item.type(self.p.getCurrentState())
            # todo: soon, that wont need an argument
            actType = self.p.getTransitionName(actTypeInternal)
            actType = sub(r' motion',r'',actType)
            actCategory = item.category(self.p.getCurrentState())
            actPurpose = item.purpose(self.p.getCurrentState())

            list.itemDataMap[itemIndex] = {}
            list.InsertStringItem(itemIndex, actName)
            list.SetStringItem(itemIndex, 0, actName)
            #list.itemDataMap[itemIndex][0] = actName
            list.itemDataMap[itemIndex][0] = item 
            #list.SetStringItem(itemIndex, 1, actType)
            #list.itemDataMap[itemIndex][1] = actType
            #list.SetStringItem(itemIndex, 2, actCategory)
            #list.itemDataMap[itemIndex][2] = actCategory
            #list.SetStringItem(itemIndex, 3, actPurpose)
            #list.itemDataMap[itemIndex][3] = actPurpose
            list.SetItemData(itemIndex, itemIndex)
            

        list.SetColumnWidth(0, wx.LIST_AUTOSIZE)
        #list.SetColumnWidth(1, wx.LIST_AUTOSIZE)
        #list.SetColumnWidth(2, wx.LIST_AUTOSIZE)
        #list.SetColumnWidth(3, wx.LIST_AUTOSIZE)

#        list.SortListItems(self.preferredListSortColumn)
