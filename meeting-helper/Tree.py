from Graph import *
import copy

class Tree(Graph):

    def delete_subtree(self, node, deletedNodeListSoFar = None):
        if not deletedNodeListSoFar:
            deletedNodeListSoFar = []

        self.remove_in_edges(node)
        for out_edge in self.out_edges(node):
            deletednodes = self.delete_subtree(self.target(out_edge))
            deletedNodeListSoFar.extend(deletednodes)
        self.delete_node(node)
        deletedNodeListSoFar.append(node)

        return deletedNodeListSoFar


    def detach_subtree(self, node, subtree = None, subtreePosition = None):
        if not subtree:
            self.remove_in_edges(node)
            subtree = Tree()
            newVertex = subtree.add_vertex(node.contents)
        else:
            newVertex = subtree.add_vertex(node.contents)
            subtree.add_edge(subtreePosition, newVertex)
            
        for out_edge in self.out_edges(node):
            self.detach_subtree(self.target(out_edge), subtree, newVertex)
        self.delete_node(node)

        #print subtree.all_nodes()
        return subtree

    def append_subtree(self, targetNode, subtree, subtreeRoot):
        newVertex = self.add_vertex(subtreeRoot.contents)    
        for out_edge in subtree.out_edges(subtreeRoot):    
            self.insert_subtree(newVertex, subtree, subtree.target(out_edge))
        
        return newVertex

    def reparent(self, childNode, newParentNode):
        self.remove_in_edges(childNode)
        self.add_edge(newParentNode, childNode)
