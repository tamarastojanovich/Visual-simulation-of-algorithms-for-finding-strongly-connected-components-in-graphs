import graph_
import random
import networkx as nx

class Tarjan_DjikstraAlgorithm:
    
    stack_S=[]
    stack_P=[]
    preorder_number={}
    scss=[]
    C=1
    graph={}
    interface=graph_.GraphInterface()
    found_scc=[]
    g=0
    b=0
    
    
  
    
    def __init__(self,grap:nx.DiGraph,interface):
        self.graph=grap
        for i in grap.nodes:
            self.preorder_number[i]=0
        self.interface=graph_.GraphInterface()
        self.interface.copy_graph(grap)
        self.interface.set_Tarjan_Djikstra()
        self.interface.draw_graph()
        
        
    
    @classmethod
    def find_SCSS(self,node):
        self.preorder_number[node] = self.C
        self.C = self.C + 1
        
        self.interface.push_on_stack(node)
        self.stack_S.append(node)
        self.interface.change_color_of_node(node,'aquamarine2',5)
        self.interface.push_on_stack_P(node)
        self.stack_P.append(node)
        
        for edges in list(self.interface.graph.neighbors(node)):
                if self.preorder_number[edges]==0:
                    self.interface.change_color_of_node(node,'aquamarine2',0)
                    self.interface.write_to_log("INFO:   VISITING NODE "+str(edges)+" FROM NODE "+str(node))
                    self.find_SCSS(edges)
                else:
                    self.interface.write_to_log("ERROR:   CANNOT VISIT NODE "+str(edges)+" SINCE IT IS ALREADY VISITED")
                    if self.stack_S.count(edges)>0:
                        while len(self.stack_P)>0:
                            
                            p=self.stack_P.pop()
                            self.interface.write_to_log("INFO:  POPPING OFF NODES FROM STACK P UNTIL WE FIND A NODE THAT HAS BEEN VISITED BEFORE NODE "+str(edges))
                            if self.preorder_number[p]<=self.preorder_number[edges]:
                                self.stack_P.append(p)
                                self.interface.write_to_log("INFO: NODE " +str(p)+" HAS BEEN VISITED BEFORE NODE "+str(edges))
                                break
                            else:
                                self.interface.pop_off_stack_P(p)
        if self.stack_P[-1]==node:
            r=random.randint(200,255)
            self.g=(self.g+50)%256
            self.b=(self.b+60)%256
            scss_path=[]
            while len(self.stack_S)>0:
                
                s=self.stack_S.pop()
                self.interface.pop_off_stack(s)
                self.interface.change_color_of_node(s,(r,self.g,self.b),0)
                scss_path.append(s)
                if(s==node):
                    self.scss.append(scss_path)
                    break
            self.found_scc.append(scss_path)
            p=self.stack_P.pop()
            self.interface.pop_off_stack_P(p)
    @classmethod
    def write_SCC(self):
        self.interface.write_to_log("INFO: THE FOUND SCCS ARE:")
        for scc in self.found_scc:
            text=""
            for node in scc:
                text+=str(node)+" "
            self.interface.write_to_log("INFO:"+text)
            