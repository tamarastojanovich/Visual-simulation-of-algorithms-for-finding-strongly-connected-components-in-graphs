import networkx as nx
import random
import graph_


class KosarajuAlgorithm:
    
    stack=[]
    visited={}
    graph=nx.DiGraph()
    interface=graph_.GraphInterface()
    curr_scc=[]
    g=0
    b=0
    
    def __init__(self,grap:nx.DiGraph,interface):
        self.graph=interface.graph
        for i in grap.nodes:
            self.visited[i]=False
        self.interface=graph_.GraphInterface()
        self.interface.copy_graph(grap)
        print(self.interface.graph)
        self.interface.draw_graph()
    
    @classmethod
    def dfs(self,node):
        self.visited[node]=True
        self.interface.change_color_of_node(node,"aquamarine2",5)
        for e in list(self.interface.graph.neighbors(node)):
                if not self.visited[e]:
                    self.interface.write_to_log("INFO:   VISITING NODE "+str(e)+" FROM NODE "+str(node))
                    self.interface.change_color_of_node(node,"aquamarine2",0)
                    self.dfs(e)
                    self.interface.change_color_of_node(node,"aquamarine2",5)
                
                else:
                    self.interface.write_to_log("ERROR:   CANNOT VISIT NODE "+str(e)+" SINCE IT IS ALREADY VISITED")
        self.stack.append(node)
        self.interface.push_on_stack(node)

    @classmethod
    def findSCC(self,node,color):
        self.visited[node]=True
        self.interface.change_color_of_node(node,color,0)
        self.curr_scc.append(node)
        for n in list(self.interface.graph.neighbors(node)):
            if not self.visited[n]:
                self.findSCC(n,color)

    @classmethod
    def transponed_dfs(self):
        self.interface.write_to_log("INFO: SCC FOUND")
        while len(self.stack)!=0:
            node=self.stack.pop()
            self.interface.pop_off_stack(node)
            
            if not self.visited[node]:
                r=random.randint(200,255)
                self.g=(self.g+60)%256
                self.b=(self.b+60)%256
                self.findSCC(node,(r,self.g,self.b))
                text=""
                for node in self.curr_scc:
                    text +=node+"  "
                self.interface.write_to_log("INFO: "+text)
                self.curr_scc.clear()
                    

    @classmethod
    def transpone_graph(self):
        self.interface.remove_edges_with_fade()
        self.interface.change_graph(self.interface.graph)
        self.interface.add_edges_with_fade()
            
            
            
    @classmethod
    def reset_keys(self):
        for i in self.interface.graph.nodes:
            self.visited[i]=False
