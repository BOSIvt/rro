class Vertex:
    def __init__(self, id, contents = None):
        self.id = id
        self.contents = contents
        #print 'added ' + `self` 
        
class Arc:
    def __init__(self, src, target, contents = None):
        self.src = src
        self.target = target
        self.contents = contents

class Graph:
    

    def __init__(self):
        self.nodes = []
        self.arcs = []
        self.topID = 0
    
    def add_vertex(self, contents = None):
        newVertex = Vertex(self.topID, contents)
        self.topID += 1
        self.nodes.append(newVertex)
        return newVertex
        
    def add_edge(self, src, target, contents = None):
        newArc = Arc(src.id,target.id, contents)
        self.arcs.append(newArc)
        return newArc

    def delete_node(self, node):
        self.remove_in_edges(node)
        self.remove_out_edges(node)
        self.nodes.remove(node)
        
    def delete_edge(self, src, target):
        arcs = [a for a in self.arcs
         if not (a.src == src.id) and (a.target == target.id)]

    def traverse(self, startingNode, arc):
        return arc.target

    def followPath(self, startingNode, path):
        position = startingNode
        
        for arc in path:
            position = self.traverse(position, arc)

        return position

    def setNodeContents(self, node, newContents):
        node.contents = newContents

    def find_vertex_with_contents(self, contents):
        for node in self.nodes:
            if node.contents == contents:
                return node

    def find_vertex_with_id(self, id):
        for node in self.nodes:
            if node.id == id:
                return node
            
    
    def out_edges(self, vertex):
        return [a for a in self.arcs
                if (a.src == vertex.id)]

    def in_edges(self, vertex):
        return [a for a in self.arcs
                if (a.target == vertex.id)]        

    def children(self, vertex):
        return [self.target(e) for e in self.out_edges(vertex)]

    def parents(self, vertex):
        return [self.source(e) for e in self.in_edges(vertex)]

    def target(self, e):
        return self.find_vertex_with_id(e.target)

    def source(self, e):
        return self.find_vertex_with_id(e.src)

    def remove_in_edges(self, vertex):
        self.arcs = [a for a in self.arcs
                if not a in self.in_edges(vertex)]
        
    def remove_out_edges(self, vertex):
        self.arcs = [a for a in self.arcs
                if not a in self.out_edges(vertex)]

    def all_nodes(self):
        return self.nodes
